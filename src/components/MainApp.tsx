
import React, { useState, useEffect } from 'react';
import { toast } from 'sonner';
import { Scene3D } from './Scene3D';
import { Sidebar } from './Sidebar';
import { useCSVLoader } from '@/hooks/useCSVLoader';
import { useProjectFilters } from '@/hooks/useProjectFilters';
import { useAISimilarity } from '@/hooks/useAISimilarity';
import { Project, SimilarityResult } from '@/types/project';

interface MainAppProps {
  initialProjects: Project[];
}

export const MainApp: React.FC<MainAppProps> = ({ initialProjects }) => {
  const { projects, setProjects } = useCSVLoader();
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [similarityResults, setSimilarityResults] = useState<SimilarityResult[]>([]);
  
  const { findSimilarProjects, loading: aiLoading } = useAISimilarity();
  
  // Initialize projects
  useEffect(() => {
    if (initialProjects.length > 0) {
      setProjects(initialProjects);
    }
  }, [initialProjects, setProjects]);

  const {
    filters,
    filteredProjects,
    updateFilter,
    clearFilters,
    filterOptions
  } = useProjectFilters(projects);

  const handleProjectClick = (project: Project) => {
    setSelectedProject(selectedProject?.title === project.title ? null : project);
  };

  const handleAISearch = async (query: string) => {
    try {
      const results = await findSimilarProjects(query, projects, 5);
      setSimilarityResults(results);
      
      if (results.length > 0) {
        setSelectedProject(results[0].project);
        toast.success(`Found ${results.length} similar projects!`);
      } else {
        toast.info('No similar projects found. Try a different description.');
      }
    } catch (error) {
      toast.error('Failed to find similar projects. Please try again.');
      console.error('AI search error:', error);
    }
  };

  const handleCanvasClick = () => {
    setSelectedProject(null);
  };

  const highlightedProjects = similarityResults.map(result => result.project);

  return (
    <div className="h-screen flex bg-cosmic-deep">
      {/* Sidebar */}
      <Sidebar
        filters={filters}
        onFilterChange={updateFilter}
        onClearFilters={clearFilters}
        filterOptions={filterOptions}
        onAISearch={handleAISearch}
        aiSearchLoading={aiLoading}
        projectCount={filteredProjects.length}
      />

      {/* 3D Scene */}
      <div 
        className="flex-1 relative"
        onClick={handleCanvasClick}
      >
        <Scene3D
          projects={filteredProjects}
          selectedProject={selectedProject}
          onProjectClick={handleProjectClick}
          highlightedProjects={highlightedProjects}
        />
        
        {/* Loading overlay */}
        {aiLoading && (
          <div className="absolute inset-0 bg-cosmic-deep/50 backdrop-blur-sm flex items-center justify-center z-10">
            <div className="glass-panel p-6 text-center space-y-4">
              <div className="cosmic-spinner mx-auto" />
              <div className="text-sm text-muted-foreground">
                AI is analyzing similarities...
              </div>
            </div>
          </div>
        )}

        {/* Stats overlay */}
        <div className="absolute top-4 right-4 glass-panel p-3">
          <div className="text-sm text-muted-foreground">
            Showing {filteredProjects.length} of {projects.length} projects
          </div>
          {similarityResults.length > 0 && (
            <div className="text-sm text-cosmic-aurora">
              {similarityResults.length} AI matches found
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
