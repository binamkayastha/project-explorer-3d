
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
          console.log('=== CSV LOADING DEBUG ===');
          console.log('Raw CSV data sample:', results.data[0]);
          console.log('Total rows:', results.data.length);
          console.log('CSV headers:', Object.keys(results.data[0] || {}));
          
          const parsedProjects = results.data
            .filter((row: any, index: number) => {
              // More detailed validation
              const hasName = row.name || row.title || row.Name || row.Title;
              const hasCoords = (
                (row.umap_dim_1 !== undefined && row.umap_dim_1 !== '') ||
                (row.x !== undefined && row.x !== '') ||
                (row.X !== undefined && row.X !== '') ||
                (row.umap_1 !== undefined && row.umap_1 !== '') ||
                (row.dim1 !== undefined && row.dim1 !== '')
              );
              
              // More lenient validation - accept any row with a name
              const isValidRow = hasName && Object.keys(row).length > 1;
              
              if (!isValidRow) {
                console.log(`Filtered out invalid row ${index}:`, {
                  hasName,
                  hasCoords,
                  name: hasName,
                  coords: {
                    umap_dim_1: row.umap_dim_1,
                    x: row.x,
                    X: row.X,
                    umap_1: row.umap_1,
                    dim1: row.dim1
                  }
                });
              }
              
              return isValidRow;
            })
            .map((row: any, index: number) => {
              // Enhanced coordinate parsing with multiple possible column names
              const parseCoord = (value: any, defaultVal: number = 0): number => {
                if (value === undefined || value === null || value === '') return defaultVal;
                const parsed = parseFloat(value);
                return isNaN(parsed) ? defaultVal : parsed;
              };

              // Try multiple possible coordinate column names
              const rawX = parseCoord(
                row.umap_dim_1 || row.x || row.X || row.umap_1 || row.dim1 || row.UMAP_1
              );
              const rawY = parseCoord(
                row.umap_dim_2 || row.y || row.Y || row.umap_2 || row.dim2 || row.UMAP_2
              );
              const rawZ = parseCoord(
                row.umap_dim_3 || row.z || row.Z || row.umap_3 || row.dim3 || row.UMAP_3
              );

              // If no coordinates found, generate random ones based on the project name
              let finalX = rawX;
              let finalY = rawY;
              let finalZ = rawZ;

              if (rawX === 0 && rawY === 0) {
                // Generate deterministic random coordinates based on project name
                const nameHash = (row.name || row.title || row.Name || row.Title || `Project ${index}`)
                  .split('')
                  .reduce((acc, char) => char.charCodeAt(0) + ((acc << 5) - acc), 0);
                
                finalX = (nameHash % 40) - 20; // Range: -20 to 20
                finalY = ((nameHash * 2) % 40) - 20; // Range: -20 to 20
                finalZ = ((nameHash * 3) % 20) - 10; // Range: -10 to 10
                
                console.log(`Generated coordinates for "${row.name || row.title}": (${finalX}, ${finalY}, ${finalZ})`);
              } else if (rawZ === 0) {
                // If no Z coordinate, generate one based on X and Y for 2D data
                finalZ = (rawX + rawY) * 0.1;
              }

              // Apply scaling factor for better visualization
              const scaleFactor = 2; // Reduced from 3 to 2 for better visibility
              const x = finalX * scaleFactor;
              const y = finalY * scaleFactor;
              const z = finalZ * scaleFactor;

              const project: Project = {
                // Primary mappings with fallbacks
                title: row.name || row.title || row.Name || row.Title || `Project ${index + 1}`,
                description: row.detailed_description || row.description || row.Description || '',
                tags: row.tags || row.Tags || '',
                category: row.category || row.Category || '',
                subcategory_1: row.subcategory_1 || row.Subcategory_1 || '',
                subcategory_2: row.subcategory_2 || row.Subcategory_2 || '',
                subcategory_3: row.subcategory_3 || row.Subcategory_3 || '',
                launch_date: row.launch_date || row.Launch_Date || '',
                launch_year: parseInt(row.launch_year || row.Launch_Year) || new Date().getFullYear(),
                team: row.team || row.Team || '',
                project_url: row.project_url || row.Project_URL || '',
                github_url: row.github_url || row.Github_URL || '',
                
                // Scaled coordinates
                x: x,
                y: y,
                z: z,
                
                category_label: row.cleaned_tag_category || row.category_label || row.Category_Label || row.category || row.Category || 'Uncategorized',
                text: row.text || row.detailed_description || row.description || row.Description || row.name || row.Name || '',
                
                // Keep original fields for reference
                name: row.name || row.Name,
                detailed_description: row.detailed_description || row.Description,
                umap_dim_1: finalX,
                umap_dim_2: finalY,
                umap_dim_3: finalZ,
                cleaned_tag_category: row.cleaned_tag_category || row.Category_Label,
              };

              console.log(`Project ${index}: "${project.title}" -> coords: (${x.toFixed(2)}, ${y.toFixed(2)}, ${z.toFixed(2)})`);
              return project;
            }) as Project[];

          console.log(`Successfully parsed ${parsedProjects.length} projects from CSV`);
          
          // Enhanced coordinate range analysis
          if (parsedProjects.length > 0) {
            const xCoords = parsedProjects.map(p => p.x).filter(x => !isNaN(x));
            const yCoords = parsedProjects.map(p => p.y).filter(y => !isNaN(y));
            const zCoords = parsedProjects.map(p => p.z).filter(z => !isNaN(z));
            
            if (xCoords.length > 0 && yCoords.length > 0) {
              const xRange = [Math.min(...xCoords), Math.max(...xCoords)];
              const yRange = [Math.min(...yCoords), Math.max(...yCoords)];
              const zRange = zCoords.length > 0 ? [Math.min(...zCoords), Math.max(...zCoords)] : [0, 0];
              
              console.log('=== COORDINATE ANALYSIS ===');
              console.log('X range:', xRange);
              console.log('Y range:', yRange);
              console.log('Z range:', zRange);
              console.log('Coordinate spread:', {
                xSpread: xRange[1] - xRange[0],
                ySpread: yRange[1] - yRange[0],
                zSpread: zRange[1] - zRange[0]
              });
              
              // Check if coordinates are reasonable for 3D visualization
              const maxSpread = Math.max(xRange[1] - xRange[0], yRange[1] - yRange[0], zRange[1] - zRange[0]);
              if (maxSpread < 1) {
                console.warn('⚠️ WARNING: Very small coordinate spread detected. Data points might be too close together.');
              }
              if (maxSpread > 100) {
                console.warn('⚠️ WARNING: Very large coordinate spread detected. Data points might be too far apart.');
              }
            }
            
            // Log sample projects
            console.log('Sample projects:', parsedProjects.slice(0, 5).map(p => ({
              title: p.title,
              coords: [p.x, p.y, p.z],
              category: p.category_label
            })));
          } else {
            console.error('❌ No valid projects found after parsing!');
            setError('No valid data points found in CSV. Please check your file format.');
            setLoading(false);
            return;
          }

          setProjects(parsedProjects);
          console.log('=== CSV LOADING COMPLETE ===');
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
