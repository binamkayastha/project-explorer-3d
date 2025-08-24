
import { useState, useMemo } from 'react';
import { Project, ProjectFilter } from '@/types/project';

export const useProjectFilters = (projects: Project[]) => {
  const [filters, setFilters] = useState<ProjectFilter>({});

  const filteredProjects = useMemo(() => {
    return projects.filter(project => {
      // Category filter
      if (filters.category && project.category !== filters.category) {
        return false;
      }

      // Subcategory filter
      if (filters.subcategory && 
          !project.subcategory_1.includes(filters.subcategory) &&
          !project.subcategory_2.includes(filters.subcategory) &&
          !project.subcategory_3.includes(filters.subcategory)) {
        return false;
      }

      // Year range filter
      if (filters.yearRange) {
        const [minYear, maxYear] = filters.yearRange;
        if (project.launch_year < minYear || project.launch_year > maxYear) {
          return false;
        }
      }

      // Search term filter
      if (filters.searchTerm) {
        const searchLower = filters.searchTerm.toLowerCase();
        return (
          project.title.toLowerCase().includes(searchLower) ||
          project.description.toLowerCase().includes(searchLower) ||
          project.tags.toLowerCase().includes(searchLower) ||
          project.team.toLowerCase().includes(searchLower)
        );
      }

      return true;
    });
  }, [projects, filters]);

  const updateFilter = (key: keyof ProjectFilter, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const clearFilters = () => {
    setFilters({});
  };

  // Get unique values for filter options
  const filterOptions = useMemo(() => ({
    categories: [...new Set(projects.map(p => p.category))].filter(Boolean),
    subcategories: [...new Set([
      ...projects.map(p => p.subcategory_1),
      ...projects.map(p => p.subcategory_2),
      ...projects.map(p => p.subcategory_3)
    ])].filter(Boolean),
    yearRange: projects.length > 0 ? [
      Math.min(...projects.map(p => p.launch_year)),
      Math.max(...projects.map(p => p.launch_year))
    ] : [2020, 2024]
  }), [projects]);

  return {
    filters,
    filteredProjects,
    updateFilter,
    clearFilters,
    filterOptions
  };
};
