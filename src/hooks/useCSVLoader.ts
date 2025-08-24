
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
          const parsedProjects = results.data
            .filter((row: any) => row.title && row.x && row.y && row.z)
            .map((row: any) => ({
              title: row.title || '',
              description: row.description || '',
              tags: row.tags || '',
              category: row.category || '',
              subcategory_1: row.subcategory_1 || '',
              subcategory_2: row.subcategory_2 || '',
              subcategory_3: row.subcategory_3 || '',
              launch_date: row.launch_date || '',
              launch_year: parseInt(row.launch_year) || 2023,
              team: row.team || '',
              project_url: row.project_url || '',
              github_url: row.github_url || '',
              x: parseFloat(row.x) || 0,
              y: parseFloat(row.y) || 0,
              z: parseFloat(row.z) || 0,
              category_label: row.category_label || '',
              text: row.text || '',
            })) as Project[];

          setProjects(parsedProjects);
          console.log(`Loaded ${parsedProjects.length} projects`);
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
