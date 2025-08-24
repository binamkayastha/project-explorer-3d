
import React, { useRef, useState, useMemo } from 'react';
import { Canvas, useFrame, MeshProps } from '@react-three/fiber';
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

// Color palette for categories
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
  ];
  
  const hash = categoryLabel.split('').reduce((acc, char) => {
    return char.charCodeAt(0) + ((acc << 5) - acc);
  }, 0);
  
  return colors[Math.abs(hash) % colors.length];
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
  const isRecent = project.launch_year >= 2023;

  useFrame((state) => {
    if (meshRef.current && isRecent) {
      const material = meshRef.current.material as THREE.MeshStandardMaterial;
      if (material) {
        material.opacity = 0.7 + Math.sin(state.clock.elapsedTime * 2) * 0.3;
      }
    }
  });

  const scale = useMemo(() => {
    if (isSelected) return 3;
    if (isHighlighted) return 2.5;
    if (hovered) return 2;
    return 1;
  }, [isSelected, isHighlighted, hovered]);

  return (
    <group
      position={[project.x * 10, project.y * 10, project.z * 10]}
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
        <sphereGeometry args={[0.1, 16, 16]} />
        <meshStandardMaterial
          color={color}
          transparent={true}
          opacity={isRecent ? 0.8 : 0.7}
          emissive={isHighlighted ? color : '#000000'}
          emissiveIntensity={isHighlighted ? 0.3 : 0}
        />
      </mesh>
      
      {isSelected && (
        <Html distanceFactor={10}>
          <div className="animate-scale-in">
            <ProjectCard project={project} />
          </div>
        </Html>
      )}
      
      {hovered && !isSelected && (
        <Html distanceFactor={15}>
          <div className="cosmic-tooltip animate-fade-in">
            <div className="font-medium">{project.title}</div>
            <div className="text-xs opacity-80">{project.category_label}</div>
          </div>
        </Html>
      )}
    </group>
  );
};

const Scene3DContent: React.FC<Scene3DProps> = ({
  projects,
  selectedProject,
  onProjectClick,
  highlightedProjects = []
}) => {
  return (
    <>
      <ambientLight intensity={0.4} />
      <pointLight position={[10, 10, 10]} intensity={0.8} />
      <pointLight position={[-10, -10, -10]} intensity={0.4} color="#00D4AA" />
      
      {projects.map((project, index) => (
        <ProjectNode
          key={`${project.title}-${index}`}
          project={project}
          isSelected={selectedProject?.title === project.title}
          isHighlighted={highlightedProjects.some(h => h.title === project.title)}
          onClick={onProjectClick}
        />
      ))}

      {/* Axis labels */}
      <Text
        position={[15, 0, 0]}
        fontSize={1}
        color="#00D4AA"
        anchorX="center"
        anchorY="middle"
      >
        X Axis
      </Text>
      <Text
        position={[0, 15, 0]}
        fontSize={1}
        color="#D946EF"
        anchorX="center"
        anchorY="middle"
      >
        Y Axis
      </Text>
      <Text
        position={[0, 0, 15]}
        fontSize={1}
        color="#3B82F6"
        anchorX="center"
        anchorY="middle"
      >
        Z Axis
      </Text>

      <OrbitControls
        enableZoom={true}
        enablePan={true}
        enableRotate={true}
        maxDistance={50}
        minDistance={5}
      />
    </>
  );
};

export const Scene3D: React.FC<Scene3DProps> = (props) => {
  return (
    <div className="w-full h-full">
      <Canvas
        camera={{ position: [15, 15, 15], fov: 60 }}
        style={{ background: 'transparent' }}
      >
        <Scene3DContent {...props} />
      </Canvas>
    </div>
  );
};
