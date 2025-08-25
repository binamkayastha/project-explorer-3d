
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
    if (meshRef.current) {
      // Gentle floating animation
      meshRef.current.position.y = (project.y || 0) + Math.sin(state.clock.elapsedTime + (project.x || 0)) * 0.1;
      
      // Pulsing for recent projects or highlighted ones
      if (isRecent || isHighlighted) {
        const material = meshRef.current.material as THREE.MeshStandardMaterial;
        if (material) {
          material.emissiveIntensity = 0.2 + Math.sin(state.clock.elapsedTime * 3) * 0.15;
        }
      }
    }
  });

  const scale = useMemo(() => {
    if (isSelected) return 3;
    if (isHighlighted) return 2.2;
    if (hovered) return 1.8;
    return 1.5; // Increased base scale for better visibility
  }, [isSelected, isHighlighted, hovered]);

  // Ensure we have valid coordinates with better fallbacks
  const position: [number, number, number] = [
    (project.x !== undefined && !isNaN(project.x)) ? project.x : Math.random() * 20 - 10,
    (project.y !== undefined && !isNaN(project.y)) ? project.y : Math.random() * 20 - 10,
    (project.z !== undefined && !isNaN(project.z)) ? project.z : Math.random() * 20 - 10
  ];

  // Debug logging for first few projects
  if (Math.random() < 0.1) { // Only log 10% of projects to avoid spam
    console.log(`ProjectNode "${project.title}" position:`, position, 'scale:', scale);
  }

  // Render different geometries based on category
  const renderGeometry = () => {
    const baseSize = 0.8; // Increased base size for better visibility
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
        console.log('Clicked project:', project.title, 'at position:', position);
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
          opacity={0.9}
          emissive={isHighlighted ? color : '#000000'}
          emissiveIntensity={isHighlighted ? 0.3 : 0.1}
          roughness={0.3}
          metalness={0.2}
        />
      </mesh>
      
      {/* Glowing outline for selected projects */}
      {isSelected && (
        <mesh scale={1.1}>
          {renderGeometry()}
          <meshBasicMaterial
            color={color}
            transparent={true}
            opacity={0.3}
            side={THREE.BackSide}
          />
        </mesh>
      )}
      
      {/* Add a small glow effect for all projects to make them more visible */}
      <mesh scale={1.3}>
        {renderGeometry()}
        <meshBasicMaterial
          color={color}
          transparent={true}
          opacity={0.1}
          side={THREE.BackSide}
        />
      </mesh>
      
      {isSelected && (
        <Html distanceFactor={6} position={[0, 1, 0]}>
          <div className="animate-scale-in">
            <ProjectCard project={project} />
          </div>
        </Html>
      )}
      
      {hovered && !isSelected && (
        <Html distanceFactor={8} position={[0, 0.8, 0]}>
          <div className="cosmic-tooltip animate-fade-in max-w-xs pointer-events-none">
            <div className="font-medium truncate text-white">{project.title}</div>
            <div className="text-xs opacity-80 text-cosmic-aurora">{project.category_label}</div>
            <div className="text-xs opacity-60 mt-1 line-clamp-2 text-gray-300">
              {project.description || 'No description available'}
            </div>
          </div>
        </Html>
      )}
    </group>
  );
};

// Coordinate system indicators with better visibility
const CoordinateSystem: React.FC<{ visible: boolean }> = ({ visible }) => {
  if (!visible) return null;

  return (
    <>
      {/* X Axis - Red */}
      <mesh position={[15, 0, 0]}>
        <cylinderGeometry args={[0.1, 0.1, 30]} />
        <meshBasicMaterial color="#ff4444" />
      </mesh>
      <Text
        position={[18, 0, 0]}
        fontSize={1.5}
        color="#ff4444"
        anchorX="left"
        anchorY="middle"
      >
        X (UMAP Dim 1)
      </Text>

      {/* Y Axis - Green */}
      <mesh position={[0, 15, 0]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.1, 0.1, 30]} />
        <meshBasicMaterial color="#44ff44" />
      </mesh>
      <Text
        position={[0, 18, 0]}
        fontSize={1.5}
        color="#44ff44"
        anchorX="center"
        anchorY="bottom"
      >
        Y (UMAP Dim 2)
      </Text>

      {/* Z Axis - Blue */}
      <mesh position={[0, 0, 15]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.1, 0.1, 30]} />
        <meshBasicMaterial color="#4444ff" />
      </mesh>
      <Text
        position={[0, 0, 18]}
        fontSize={1.5}
        color="#4444ff"
        anchorX="center"
        anchorY="middle"
      >
        Z (UMAP Dim 3)
      </Text>
    </>
  );
};

// Interactive grid to help with navigation
const InteractiveGrid: React.FC = () => {
  return (
    <>
      <gridHelper args={[50, 20, '#333333', '#222222']} position={[0, -15, 0]} />
      <gridHelper args={[50, 20, '#333333', '#222222']} position={[0, 0, -15]} rotation={[Math.PI / 2, 0, 0]} />
      <gridHelper args={[50, 20, '#333333', '#222222']} position={[-15, 0, 0]} rotation={[0, 0, Math.PI / 2]} />
    </>
  );
};

const Scene3DContent: React.FC<Scene3DProps> = ({
  projects,
  selectedProject,
  onProjectClick,
  highlightedProjects = []
}) => {
  console.log('=== Scene3D RENDERING ===');
  console.log('Total projects to render:', projects.length);
  console.log('Sample project coordinates:', projects.slice(0, 3).map(p => ({ 
    title: p.title, 
    x: p.x, 
    y: p.y, 
    z: p.z,
    category: p.category_label 
  })));

  // Check if we have valid coordinates
  const validProjects = projects.filter(p => 
    p.x !== undefined && !isNaN(p.x) && 
    p.y !== undefined && !isNaN(p.y) && 
    p.z !== undefined && !isNaN(p.z)
  );

  console.log('Projects with valid coordinates:', validProjects.length);

  if (validProjects.length === 0) {
    console.warn('⚠️ No projects with valid coordinates found!');
    return (
      <>
        <ambientLight intensity={0.6} />
        <pointLight position={[20, 20, 20]} intensity={1.2} color="#ffffff" />
        <InteractiveGrid />
        <Text
          position={[0, 0, 0]}
          fontSize={2}
          color="#ff4444"
          anchorX="center"
          anchorY="middle"
        >
          No data points to display
        </Text>
        <Text
          position={[0, -3, 0]}
          fontSize={1}
          color="#cccccc"
          anchorX="center"
          anchorY="middle"
        >
          Check your CSV file format
        </Text>
        <OrbitControls
          enableZoom={true}
          enablePan={true}
          enableRotate={true}
          maxDistance={150}
          minDistance={3}
          dampingFactor={0.05}
          enableDamping={true}
          zoomSpeed={0.8}
          panSpeed={0.8}
          rotateSpeed={0.5}
        />
      </>
    );
  }

  return (
    <>
      {/* Enhanced lighting setup - Fixed hemisphereLight props */}
      <ambientLight intensity={0.6} />
      <pointLight position={[20, 20, 20]} intensity={1.2} color="#ffffff" />
      <pointLight position={[-20, -20, -20]} intensity={0.8} color="#00D4AA" />
      <pointLight position={[20, -20, 20]} intensity={0.6} color="#D946EF" />
      <hemisphereLight args={["#87CEEB", "#362D59", 0.4]} />
      
      {/* Interactive grid */}
      <InteractiveGrid />
      
      {/* Render all projects */}
      {validProjects.map((project, index) => (
        <ProjectNode
          key={`${project.title}-${index}`}
          project={project}
          isSelected={selectedProject?.title === project.title}
          isHighlighted={highlightedProjects.some(h => h.title === project.title)}
          onClick={onProjectClick}
        />
      ))}

      {/* Coordinate system */}
      <CoordinateSystem visible={validProjects.length > 0} />

      <OrbitControls
        enableZoom={true}
        enablePan={true}
        enableRotate={true}
        maxDistance={150}
        minDistance={3}
        dampingFactor={0.05}
        enableDamping={true}
        zoomSpeed={0.8}
        panSpeed={0.8}
        rotateSpeed={0.5}
      />
    </>
  );
};

export const Scene3D: React.FC<Scene3DProps> = (props) => {
  return (
    <div className="w-full h-full relative">
      <Canvas
        camera={{ position: [40, 40, 40], fov: 60 }}
        style={{ background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)' }}
      >
        <Scene3DContent {...props} />
      </Canvas>
      
      {/* Enhanced debug info */}
      <div className="absolute bottom-4 left-4 glass-panel p-4 text-sm space-y-2">
        <div className="font-semibold text-cosmic-aurora">3D Dataset Viewer</div>
        <div>Projects: <span className="text-white">{props.projects.length}</span></div>
        <div>Valid coordinates: <span className="text-white">{props.projects.filter(p => p.x !== undefined && !isNaN(p.x) && p.y !== undefined && !isNaN(p.y) && p.z !== undefined && !isNaN(p.z)).length}</span></div>
        <div>Selected: <span className="text-cosmic-plasma">{props.selectedProject?.title || 'None'}</span></div>
        {props.highlightedProjects && props.highlightedProjects.length > 0 && (
          <div className="text-cosmic-aurora">
            AI Matches: {props.highlightedProjects.length}
          </div>
        )}
        
        {/* Coordinate ranges */}
        {props.projects.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-600">
            <div className="text-xs text-gray-400">Coordinate Ranges:</div>
            {(() => {
              const validProjects = props.projects.filter(p => p.x !== undefined && !isNaN(p.x) && p.y !== undefined && !isNaN(p.y) && p.z !== undefined && !isNaN(p.z));
              if (validProjects.length > 0) {
                const xCoords = validProjects.map(p => p.x);
                const yCoords = validProjects.map(p => p.y);
                const zCoords = validProjects.map(p => p.z);
                const xRange = [Math.min(...xCoords), Math.max(...xCoords)];
                const yRange = [Math.min(...yCoords), Math.max(...yCoords)];
                const zRange = [Math.min(...zCoords), Math.max(...zCoords)];
                return (
                  <div className="text-xs space-y-1">
                    <div>X: {xRange[0].toFixed(1)} to {xRange[1].toFixed(1)}</div>
                    <div>Y: {yRange[0].toFixed(1)} to {yRange[1].toFixed(1)}</div>
                    <div>Z: {zRange[0].toFixed(1)} to {zRange[1].toFixed(1)}</div>
                  </div>
                );
              }
              return <div className="text-xs text-red-400">No valid coordinates</div>;
            })()}
          </div>
        )}
      </div>

      {/* Interactive camera controls help */}
      <div className="absolute top-4 left-4 glass-panel p-4 text-sm space-y-2">
        <div className="font-semibold text-cosmic-aurora">Interactive Controls</div>
        <div className="space-y-1 text-gray-300">
          <div>• <span className="text-white">Left-click drag:</span> Rotate view</div>
          <div>• <span className="text-white">Right-click drag:</span> Pan camera</div>
          <div>• <span className="text-white">Mouse wheel:</span> Zoom in/out</div>
          <div>• <span className="text-white">Click nodes:</span> Select projects</div>
          <div>• <span className="text-white">Hover nodes:</span> Quick preview</div>
        </div>
      </div>

      {/* Performance info */}
      <div className="absolute top-4 right-4 glass-panel p-3 text-sm">
        <div className="text-cosmic-aurora font-semibold">Status</div>
        <div className="text-white">
          Showing {props.projects.length} projects
        </div>
        {props.highlightedProjects && props.highlightedProjects.length > 0 && (
          <div className="text-cosmic-plasma">
            {props.highlightedProjects.length} AI matches highlighted
          </div>
        )}
      </div>
    </div>
  );
};
