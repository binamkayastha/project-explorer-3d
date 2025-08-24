
export interface Project {
  title: string; // mapped from 'name'
  description: string; // mapped from 'detailed_description'
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
  x: number; // mapped from 'umap_dim_1'
  y: number; // mapped from 'umap_dim_2'
  z: number; // mapped from 'umap_dim_3'
  category_label: string; // mapped from 'cleaned_tag_category'
  text: string;
  // Additional fields from your dataset
  name?: string; // original name field
  detailed_description?: string; // original description field
  umap_dim_1?: number;
  umap_dim_2?: number;
  umap_dim_3?: number;
  cleaned_tag_category?: string;
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
