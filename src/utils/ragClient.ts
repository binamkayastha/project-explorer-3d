/**
 * RAG Client for connecting to Python RAG Service
 * Step 1: Basic API client for similarity search
 */

export interface RAGProjectMatch {
  id: number
  name: string
  description: string
  ai_summary: string
  github_url: string
  project_url: string
  demo_url: string
  github_stars: number
  similarity_score: number
  match_reason: string
  integration_complexity: 'low' | 'medium' | 'high'
}

export interface RAGResponse {
  success: boolean
  matches: RAGProjectMatch[]
  total_found: number
  error?: string
}

class RAGClient {
  private baseUrl = 'http://localhost:5001'

  async findSimilarProjects(userIdea: string, limit: number = 5): Promise<RAGProjectMatch[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/similar-projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          idea: userIdea,
          limit: limit
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data: RAGResponse = await response.json()
      
      if (!data.success) {
        throw new Error(data.error || 'Unknown error')
      }

      return data.matches
    } catch (error) {
      console.error('RAG API Error:', error)
      throw new Error(`Failed to find similar projects: ${error}`)
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/health`)
      const data = await response.json()
      return data.status === 'healthy'
    } catch (error) {
      console.error('RAG Health Check Error:', error)
      return false
    }
  }
}

export const ragClient = new RAGClient()
