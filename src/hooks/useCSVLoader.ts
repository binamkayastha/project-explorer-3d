
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
          console.log('Total rows:', results.data.length);
          
          const parsedProjects = results.data
            .filter((row: any) => {
              // Check if we have the essential fields
              const hasName = row.name || row.title;
              const hasCoords = (row.umap_dim_1 !== undefined && row.umap_dim_1 !== '') || 
                              (row.x !== undefined && row.x !== '');
              const isValidRow = hasName && hasCoords && Object.keys(row).length > 1;
              
              if (!isValidRow) {
                console.log('Filtered out invalid row:', row);
              }
              
              return isValidRow;
            })
            .map((row: any, index: number) => {
              // Parse coordinates with better error handling
              const parseCoord = (value: any, defaultVal: number = 0): number => {
                if (value === undefined || value === null || value === '') return defaultVal;
                const parsed = parseFloat(value);
                return isNaN(parsed) ? defaultVal : parsed;
              };

              // Get raw UMAP coordinates
              const rawX = parseCoord(row.umap_dim_1 || row.x);
              const rawY = parseCoord(row.umap_dim_2 || row.y); 
              const rawZ = parseCoord(row.umap_dim_3 || row.z);

              // Apply scaling factor for better visualization (UMAP coords are usually between -10 to 10)
              const scaleFactor = 3;
              const x = rawX * scaleFactor;
              const y = rawY * scaleFactor;
              const z = rawZ * scaleFactor;

              const project: Project = {
                // Primary mappings
                title: row.name || row.title || `Project ${index + 1}`,
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
                
                // Scaled UMAP coordinates
                x: x,
                y: y,
                z: z,
                
                category_label: row.cleaned_tag_category || row.category_label || row.category || 'Uncategorized',
                text: row.text || row.detailed_description || row.description || row.name || '',
                
                // Keep original fields for reference
                name: row.name,
                detailed_description: row.detailed_description,
                umap_dim_1: rawX,
                umap_dim_2: rawY,
                umap_dim_3: rawZ,
                cleaned_tag_category: row.cleaned_tag_category,
              };

              console.log(`Project ${index}: "${project.title}" -> coords: (${x.toFixed(2)}, ${y.toFixed(2)}, ${z.toFixed(2)})`);
              return project;
            }) as Project[];

          console.log(`Successfully parsed ${parsedProjects.length} projects from CSV`);
          
          // Log coordinate ranges for debugging
          if (parsedProjects.length > 0) {
            const xCoords = parsedProjects.map(p => p.x).filter(x => !isNaN(x));
            const yCoords = parsedProjects.map(p => p.y).filter(y => !isNaN(y));
            const zCoords = parsedProjects.map(p => p.z).filter(z => !isNaN(z));
            
            const xRange = [Math.min(...xCoords), Math.max(...xCoords)];
            const yRange = [Math.min(...yCoords), Math.max(...yCoords)];
            const zRange = [Math.min(...zCoords), Math.max(...zCoords)];
            
            console.log('Coordinate ranges after scaling:');
            console.log('X:', xRange);
            console.log('Y:', yRange);
            console.log('Z:', zRange);
            
            // Log some sample projects
            console.log('Sample projects:', parsedProjects.slice(0, 5).map(p => ({
              title: p.title,
              coords: [p.x, p.y, p.z],
              category: p.category_label
            })));
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
        console.error('Papa parse error:', error);
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
