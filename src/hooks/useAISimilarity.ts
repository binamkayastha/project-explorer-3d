
import { useState } from 'react';
import { pipeline } from '@huggingface/transformers';
import { Project, SimilarityResult } from '@/types/project';

let embeddingModel: any = null;

export const useAISimilarity = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const initializeModel = async () => {
    if (embeddingModel) return embeddingModel;
    
    try {
      console.log('Loading embedding model...');
      embeddingModel = await pipeline(
        'feature-extraction', 
        'Xenova/all-MiniLM-L6-v2',
        { device: 'webgpu' }
      );
      console.log('Model loaded successfully');
      return embeddingModel;
    } catch (err) {
      console.warn('WebGPU not available, falling back to CPU');
      embeddingModel = await pipeline(
        'feature-extraction', 
        'Xenova/all-MiniLM-L6-v2'
      );
      return embeddingModel;
    }
  };

  const cosineSimilarity = (a: number[], b: number[]): number => {
    const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
    const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
    const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
    return dotProduct / (magnitudeA * magnitudeB);
  };

  const findSimilarProjects = async (
    userIdea: string, 
    projects: Project[], 
    topK: number = 5
  ): Promise<SimilarityResult[]> => {
    setLoading(true);
    setError(null);

    try {
      const model = await initializeModel();
      
      // Get embedding for user idea
      const userEmbedding = await model(userIdea, { pooling: 'mean', normalize: true });
      const userVector = Array.from(userEmbedding.data);

      // Calculate similarities
      const similarities: SimilarityResult[] = [];
      
      for (const project of projects) {
        if (!project.text) continue;
        
        // Get embedding for project text
        const projectEmbedding = await model(project.text, { pooling: 'mean', normalize: true });
        const projectVector = Array.from(projectEmbedding.data);
        
        const similarity = cosineSimilarity(userVector, projectVector);
        similarities.push({ project, similarity });
      }

      // Sort by similarity and return top K
      const topSimilar = similarities
        .sort((a, b) => b.similarity - a.similarity)
        .slice(0, topK);

      setLoading(false);
      return topSimilar;
    } catch (err: any) {
      setError(`AI similarity error: ${err.message}`);
      setLoading(false);
      return [];
    }
  };

  return {
    findSimilarProjects,
    loading,
    error
  };
};
