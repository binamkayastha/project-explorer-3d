
export interface Project {
  title: string;
  description: string;
  tags: string;
  category: string;
  subcategory_1: string;
  subcategory_2: string;
  subcategory_3: string;
  launch_date: string;
  launch_year: number;
  team: string;
  project_url: string;
  github_url: string;
  x: number;
  y: number;
  z: number;
  category_label: string;
  text: string;
}

export interface ProjectFilter {
  category?: string;
  subcategory?: string;
  yearRange?: [number, number];
  searchTerm?: string;
}

export interface SimilarityResult {
  project: Project;
  similarity: number;
}
