
import React, { useRef, useState, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Html } from '@react-three/drei';
import * as THREE from 'three';
import { Project } from '@/types/project';
import { ProjectCard } from './ProjectCard';

interface Scene3DProps {
  projects: Project[];
  selectedProject?: Project | null;
  onProjectClick: (project: Project) => void;
  highlightedProjects?: Project[];
}

// Enhanced color palette for categories
const getCategoryColor = (categoryLabel: string): string => {
  const colors = [
    '#00D4AA', // cosmic-aurora
    '#D946EF', // cosmic-plasma  
    '#3B82F6', // blue
    '#F59E0B', // amber
    '#EF4444', // red
    '#10B981', // emerald
    '#8B5CF6', // violet
    '#F97316', // orange
    '#06B6D4', // cyan
    '#84CC16', // lime
  ];
  
  const hash = categoryLabel.split('').reduce((acc, char) => {
    return char.charCodeAt(0) + ((acc << 5) - acc);
  }, 0);
  
  return colors[Math.abs(hash) % colors.length];
};

// Enhanced shape selection based on category
const getCategoryShape = (categoryLabel: string): 'sphere' | 'box' | 'octahedron' => {
  const shapes = ['sphere', 'box', 'octahedron'];
  const hash = categoryLabel.split('').reduce((acc, char) => {
    return char.charCodeAt(0) + ((acc << 5) - acc);
  }, 0);
  
  return shapes[Math.abs(hash) % shapes.length] as 'sphere' | 'box' | 'octahedron';
};

interface ProjectNodeProps {
  project: Project;
  isSelected: boolean;
  isHighlighted: boolean;
  onClick: (project: Project) => void;
}

const ProjectNode: React.FC<ProjectNodeProps> = ({ 
  project, 
  isSelected, 
  isHighlighted, 
  onClick 
}) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  const color = getCategoryColor(project.category_label);
  const shape = getCategoryShape(project.category_label);
  const isRecent = project.launch_year >= 2023;

  useFrame((state) => {
    if (meshRef.current && (isRecent || isHighlighted)) {
      const material = meshRef.current.material as THREE.MeshStandardMaterial;
      if (material) {
        material.opacity = 0.7 + Math.sin(state.clock.elapsedTime * 2) * 0.2;
      }
    }
  });

  const scale = useMemo(() => {
    if (isSelected) return 2.5;
    if (isHighlighted) return 2;
    if (hovered) return 1.5;
    return 1;
  }, [isSelected, isHighlighted, hovered]);

  // Use project coordinates with fallbacks
  const position: [number, number, number] = [
    project.x || 0,
    project.y || 0,
    project.z || 0
  ];

  // Render different geometries based on category
  const renderGeometry = () => {
    const baseSize = 0.3;
    switch (shape) {
      case 'box':
        return <boxGeometry args={[baseSize, baseSize, baseSize]} />;
      case 'octahedron':
        return <octahedronGeometry args={[baseSize]} />;
      default:
        return <sphereGeometry args={[baseSize, 16, 16]} />;
    }
  };

  return (
    <group
      position={position}
      scale={scale}
      onClick={(e) => {
        e.stopPropagation();
        onClick(project);
      }}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
        document.body.style.cursor = 'pointer';
      }}
      onPointerOut={() => {
        setHovered(false);
        document.body.style.cursor = 'auto';
      }}
    >
      <mesh ref={meshRef}>
        {renderGeometry()}
        <meshStandardMaterial
          color={color}
          transparent={true}
          opacity={isRecent ? 0.9 : 0.7}
          emissive={isHighlighted ? color : '#000000'}
          emissiveIntensity={isHighlighted ? 0.3 : 0}
          roughness={0.4}
          metalness={0.1}
        />
      </mesh>
      
      {isSelected && (
        <Html distanceFactor={8}>
          <div className="animate-scale-in">
            <ProjectCard project={project} />
          </div>
        </Html>
      )}
      
      {hovered && !isSelected && (
        <Html distanceFactor={12}>
          <div className="cosmic-tooltip animate-fade-in max-w-xs">
            <div className="font-medium truncate">{project.title}</div>
            <div className="text-xs opacity-80">{project.category_label}</div>
            <div className="text-xs opacity-60 mt-1 line-clamp-2">{project.description}</div>
          </div>
        </Html>
      )}
    </group>
  );
};

// Coordinate system indicators
const CoordinateSystem: React.FC<{ visible: boolean }> = ({ visible }) => {
  if (!visible) return null;

  return (
    <>
      {/* X Axis - Red */}
      <mesh position={[20, 0, 0]}>
        <cylinderGeometry args={[0.05, 0.05, 40]} />
        <meshBasicMaterial color="#ff0000" />
      </mesh>
      <Text
        position={[22, 0, 0]}
        fontSize={2}
        color="#ff0000"
        anchorX="left"
        anchorY="middle"
      >
        X (UMAP Dim 1)
      </Text>

      {/* Y Axis - Green */}
      <mesh position={[0, 20, 0]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.05, 0.05, 40]} />
        <meshBasicMaterial color="#00ff00" />
      </mesh>
      <Text
        position={[0, 22, 0]}
        fontSize={2}
        color="#00ff00"
        anchorX="center"
        anchorY="bottom"
      >
        Y (UMAP Dim 2)
      </Text>

      {/* Z Axis - Blue */}
      <mesh position={[0, 0, 20]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.05, 0.05, 40]} />
        <meshBasicMaterial color="#0000ff" />
      </mesh>
      <Text
        position={[0, 0, 22]}
        fontSize={2}
        color="#0000ff"
        anchorX="center"
        anchorY="middle"
      >
        Z (UMAP Dim 3)
      </Text>
    </>
  );
};

const Scene3DContent: React.FC<Scene3DProps> = ({
  projects,
  selectedProject,
  onProjectClick,
  highlightedProjects = []
}) => {
  console.log('Scene3D rendering with projects:', projects.length);

  return (
    <>
      {/* Enhanced lighting setup */}
      <ambientLight intensity={0.4} />
      <pointLight position={[10, 10, 10]} intensity={1} color="#ffffff" />
      <pointLight position={[-10, -10, -10]} intensity={0.6} color="#00D4AA" />
      <pointLight position={[10, -10, 10]} intensity={0.4} color="#D946EF" />
      
      {/* Render all projects */}
      {projects.map((project, index) => (
        <ProjectNode
          key={`${project.title}-${index}`}
          project={project}
          isSelected={selectedProject?.title === project.title}
          isHighlighted={highlightedProjects.some(h => h.title === project.title)}
          onClick={onProjectClick}
        />
      ))}

      {/* Coordinate system */}
      <CoordinateSystem visible={projects.length > 0} />

      <OrbitControls
        enableZoom={true}
        enablePan={true}
        enableRotate={true}
        maxDistance={100}
        minDistance={2}
        dampingFactor={0.05}
        enableDamping={true}
      />
    </>
  );
};

export const Scene3D: React.FC<Scene3DProps> = (props) => {
  return (
    <div className="w-full h-full">
      <Canvas
        camera={{ position: [30, 30, 30], fov: 60 }}
        style={{ background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)' }}
      >
        <Scene3DContent {...props} />
      </Canvas>
      
      {/* Enhanced debug info */}
      <div className="absolute bottom-4 left-4 glass-panel p-3 text-xs space-y-1">
        <div className="font-semibold">3D Dataset Viewer</div>
        <div>Projects: {props.projects.length}</div>
        <div>Selected: {props.selectedProject?.title || 'None'}</div>
        {props.highlightedProjects && props.highlightedProjects.length > 0 && (
          <div className="text-cosmic-aurora">
            AI Matches: {props.highlightedProjects.length}
          </div>
        )}
      </div>

      {/* Camera controls help */}
      <div className="absolute top-4 left-4 glass-panel p-3 text-xs space-y-1">
        <div className="font-semibold">Controls</div>
        <div>• Drag to rotate</div>
        <div>• Scroll to zoom</div>
        <div>• Right-click drag to pan</div>
      </div>
    </div>
  );
};
