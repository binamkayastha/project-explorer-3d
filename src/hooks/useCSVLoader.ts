import { useState, useCallback } from 'react';
import Papa from 'papaparse';
import { Project } from '@/types/project';

export const useCSVLoader = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadCSV = useCallback((file: File) => {
    setLoading(true);
    setError(null);

    Papa.parse(file, {
      header: true,
      complete: (results) => {
        try {
          console.log('Raw CSV data sample:', results.data[0]);
          
          const parsedProjects = results.data
            .filter((row: any) => {
              // Check if we have the essential fields
              const hasName = row.name || row.title;
              const hasCoords = (row.umap_dim_1 !== undefined && row.umap_dim_1 !== '') || 
                              (row.x !== undefined && row.x !== '');
              return hasName && hasCoords;
            })
            .map((row: any) => {
              // Map your CSV columns to our Project interface
              const project: Project = {
                // Primary mappings
                title: row.name || row.title || '',
                description: row.detailed_description || row.description || '',
                tags: row.tags || '',
                category: row.category || '',
                subcategory_1: row.subcategory_1 || '',
                subcategory_2: row.subcategory_2 || '',
                subcategory_3: row.subcategory_3 || '',
                launch_date: row.launch_date || '',
                launch_year: parseInt(row.launch_year) || new Date().getFullYear(),
                team: row.team || '',
                project_url: row.project_url || '',
                github_url: row.github_url || '',
                
                // UMAP coordinates with scaling
                x: parseFloat(row.umap_dim_1 || row.x || '0') * 10, // Scale UMAP coordinates
                y: parseFloat(row.umap_dim_2 || row.y || '0') * 10,
                z: parseFloat(row.umap_dim_3 || row.z || '0') * 10,
                
                category_label: row.cleaned_tag_category || row.category_label || row.category || 'Uncategorized',
                text: row.text || row.detailed_description || row.description || row.name || '',
                
                // Keep original fields for reference
                name: row.name,
                detailed_description: row.detailed_description,
                umap_dim_1: parseFloat(row.umap_dim_1) || 0,
                umap_dim_2: parseFloat(row.umap_dim_2) || 0,
                umap_dim_3: parseFloat(row.umap_dim_3) || 0,
                cleaned_tag_category: row.cleaned_tag_category,
              };

              return project;
            }) as Project[];

          console.log(`Successfully parsed ${parsedProjects.length} projects from CSV`);
          console.log('Sample parsed project:', parsedProjects[0]);
          
          // Log coordinate ranges for debugging
          if (parsedProjects.length > 0) {
            const xRange = [
              Math.min(...parsedProjects.map(p => p.x)),
              Math.max(...parsedProjects.map(p => p.x))
            ];
            const yRange = [
              Math.min(...parsedProjects.map(p => p.y)),
              Math.max(...parsedProjects.map(p => p.y))
            ];
            const zRange = [
              Math.min(...parsedProjects.map(p => p.z)),
              Math.max(...parsedProjects.map(p => p.z))
            ];
            
            console.log('Coordinate ranges:');
            console.log('X:', xRange);
            console.log('Y:', yRange);
            console.log('Z:', zRange);
          }

          setProjects(parsedProjects);
        } catch (err) {
          setError('Failed to parse CSV file');
          console.error('CSV parsing error:', err);
        } finally {
          setLoading(false);
        }
      },
      error: (error) => {
        setError(`CSV loading error: ${error.message}`);
        setLoading(false);
      }
    });
  }, []);

  return {
    projects,
    loading,
    error,
    loadCSV,
    setProjects
  };
};
