

import Papa from 'papaparse'
import { ragClient, RAGProjectMatch } from './ragClient'

export interface Project {
  id: number
  name: string
  description: string
  project_url: string
  demo_url: string
  github_url: string
  detailed_description: string
  ai_summary: string
  architecture: string
  components_list: string
  dependencies_list: string
  features_list: string
  technologies_list: string
  github_stars: number
  repo_license: string
  contributors: string
  ai_models_inferred: string
  vector_db_inferred: string
  frameworks_inferred: string
  infrastructure_inferred: string
  top_risks: string
  setup_steps: string
  integration_plan: string
  deployment_notes: string
  security_notes: string
  testing_notes: string
  api_endpoints_list: string
  env_vars_list: string
  services_list: string
  date: string
}

export interface SearchFilters {
  technologies: string[]
  frameworks: string[]
  aiModels: string[]
  categories: string[]
  minStars: number
  maxStars?: number
}

export interface IdeaAnalysis {
  category: string
  technologies: string[]
  features: string[]
  complexity: 'low' | 'medium' | 'high'
  estimatedTime: string
  keyComponents: string[]
}

export interface ProjectMatch {
  project: Project
  similarityScore: number
  matchReason: string
  integrationComplexity: 'low' | 'medium' | 'high'
}

export interface SystemCombination {
  primaryProject: Project
  complementaryProjects: Project[]
  totalScore: number
  integrationSteps: string[]
  estimatedDevelopmentTime: string
  missingComponents: string[]
}

export interface AnalyticsData {
  technologyTrends: {
    frameworks: { name: string; count: number; percentage: number }[]
    aiModels: { name: string; count: number; percentage: number }[]
    vectorDBs: { name: string; count: number; percentage: number }[]
    infrastructure: { name: string; count: number; percentage: number }[]
  }
  projectStats: {
    totalProjects: number
    totalStars: number
    avgStars: number
    topCategories: { name: string; count: number }[]
    recentProjects: number
  }
  marketInsights: {
    gaps: string[]
    opportunities: string[]
    trendingTechnologies: string[]
    emergingCategories: string[]
  }
}

class DataLoader {
  private projects: Project[] = []
  private isLoaded = false

  async loadProjects(): Promise<Project[]> {
    if (this.isLoaded) {
      return this.projects
    }

    try {
      const response = await fetch('/df_out.csv')
      const csvText = await response.text()
      
      const result = Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true,
        transform: (value) => {
          // Clean up the data
          if (typeof value === 'string') {
            value = value.trim()
            // Remove quotes and extra whitespace
            value = value.replace(/^["']|["']$/g, '')
          }
          return value
        }
      })

      this.projects = result.data.map((row: any, index: number) => ({
        id: index,
        name: row.name || 'Unknown Project',
        description: row.description || '',
        project_url: row.project_url || '',
        demo_url: row.demo_url || '',
        github_url: row.github_url || '',
        detailed_description: row.detailed_description || '',
        ai_summary: row.ai_summary || '',
        architecture: row.architecture || '',
        components_list: row.components_list || '',
        dependencies_list: row.dependencies_list || '',
        features_list: row.features_list || '',
        technologies_list: row.technologies_list || '',
        github_stars: parseInt(row.github_stars) || 0,
        repo_license: row.repo_license || '',
        contributors: row.contributors || '',
        ai_models_inferred: row.ai_models_inferred || '',
        vector_db_inferred: row.vector_db_inferred || '',
        frameworks_inferred: row.frameworks_inferred || '',
        infrastructure_inferred: row.infrastructure_inferred || '',
        top_risks: row.top_risks || '',
        setup_steps: row.setup_steps || '',
        integration_plan: row.integration_plan || '',
        deployment_notes: row.deployment_notes || '',
        security_notes: row.security_notes || '',
        testing_notes: row.testing_notes || '',
        api_endpoints_list: row.api_endpoints_list || '',
        env_vars_list: row.env_vars_list || '',
        services_list: row.services_list || '',
        date: row.date || ''
      }))

      this.isLoaded = true
      return this.projects
    } catch (error) {
      console.error('Error loading projects:', error)
      return []
    }
  }

  // Enhanced search with better similarity scoring
  async searchProjects(query: string, filters: SearchFilters = {
    technologies: [],
    frameworks: [],
    aiModels: [],
    categories: [],
    minStars: 0,
    maxStars: undefined
  }): Promise<Project[]> {
    const projects = await this.loadProjects()
    
    if (!query.trim() && Object.keys(filters).length === 0) {
      return projects
    }

    return projects.filter(project => {
      // Text search
      const searchText = query.toLowerCase()
      const projectText = [
        project.name,
        project.description,
        project.detailed_description,
        project.ai_summary,
        project.features_list,
        project.technologies_list
      ].join(' ').toLowerCase()

      const textMatch = !query.trim() || projectText.includes(searchText)

      // Filter by technologies
      const techMatch = !filters.technologies?.length || 
        filters.technologies.some(tech => 
          project.technologies_list.toLowerCase().includes(tech.toLowerCase())
        )

      // Filter by frameworks
      const frameworkMatch = !filters.frameworks?.length || 
        filters.frameworks.some(framework => 
          project.frameworks_inferred.toLowerCase().includes(framework.toLowerCase())
        )

      // Filter by AI models
      const aiModelMatch = !filters.aiModels?.length || 
        filters.aiModels.some(model => 
          project.ai_models_inferred.toLowerCase().includes(model.toLowerCase())
        )

      // Filter by GitHub stars
      const starsMatch = !filters.minStars && !filters.maxStars || 
        (project.github_stars >= (filters.minStars || 0) && 
         project.github_stars <= (filters.maxStars || Infinity))

      return textMatch && techMatch && frameworkMatch && aiModelMatch && starsMatch
    })
  }

  // New: Analyze user idea and extract key components
  async analyzeUserIdea(idea: string): Promise<IdeaAnalysis> {
    const ideaLower = idea.toLowerCase()
    
    // Extract category based on keywords
    let category = 'General'
    if (ideaLower.includes('crm') || ideaLower.includes('customer') || ideaLower.includes('management')) {
      category = 'CRM/Business Tools'
    } else if (ideaLower.includes('ai') || ideaLower.includes('machine learning') || ideaLower.includes('chatbot')) {
      category = 'AI/ML Applications'
    } else if (ideaLower.includes('web') || ideaLower.includes('website') || ideaLower.includes('app')) {
      category = 'Web Applications'
    } else if (ideaLower.includes('mobile') || ideaLower.includes('app')) {
      category = 'Mobile Applications'
    } else if (ideaLower.includes('game') || ideaLower.includes('gaming')) {
      category = 'Gaming'
    } else if (ideaLower.includes('education') || ideaLower.includes('learning')) {
      category = 'Education'
    }

    // Extract technologies
    const technologies: string[] = []
    if (ideaLower.includes('react') || ideaLower.includes('frontend')) technologies.push('React')
    if (ideaLower.includes('node') || ideaLower.includes('backend')) technologies.push('Node.js')
    if (ideaLower.includes('python') || ideaLower.includes('ai')) technologies.push('Python')
    if (ideaLower.includes('database') || ideaLower.includes('data')) technologies.push('Database')
    if (ideaLower.includes('ai') || ideaLower.includes('openai')) technologies.push('OpenAI')

    // Extract features
    const features: string[] = []
    if (ideaLower.includes('user') || ideaLower.includes('authentication')) features.push('User Management')
    if (ideaLower.includes('api') || ideaLower.includes('integration')) features.push('API Integration')
    if (ideaLower.includes('real-time') || ideaLower.includes('live')) features.push('Real-time Updates')
    if (ideaLower.includes('analytics') || ideaLower.includes('dashboard')) features.push('Analytics')
    if (ideaLower.includes('mobile') || ideaLower.includes('responsive')) features.push('Mobile Support')

    // Determine complexity
    let complexity: 'low' | 'medium' | 'high' = 'medium'
    if (technologies.length > 4 || features.length > 5) complexity = 'high'
    else if (technologies.length < 2 && features.length < 3) complexity = 'low'

    // Estimate development time
    let estimatedTime = '2-4 weeks'
    if (complexity === 'high') estimatedTime = '8-12 weeks'
    else if (complexity === 'low') estimatedTime = '1-2 weeks'

    // Key components needed
    const keyComponents = ['Frontend', 'Backend', 'Database']
    if (technologies.includes('AI')) keyComponents.push('AI Service')
    if (features.includes('Real-time Updates')) keyComponents.push('WebSocket Service')
    if (features.includes('Analytics')) keyComponents.push('Analytics Service')

    return {
      category,
      technologies,
      features,
      complexity,
      estimatedTime,
      keyComponents
    }
  }

  // New: Find similar projects based on idea analysis
  async findSimilarProjects(idea: string, limit: number = 5): Promise<ProjectMatch[]> {
    const projects = await this.loadProjects()
    const analysis = await this.analyzeUserIdea(idea)
    
    const scoredProjects = projects.map(project => {
      let score = 0
      let matchReason = ''

      // Category match (highest weight)
      if (project.description.toLowerCase().includes(analysis.category.toLowerCase()) ||
          project.ai_summary.toLowerCase().includes(analysis.category.toLowerCase())) {
        score += 40
        matchReason += 'Category match, '
      }

      // Technology overlap
      const projectTechs = project.technologies_list.toLowerCase().split('|')
      const techOverlap = analysis.technologies.filter(tech => 
        projectTechs.some(pt => pt.includes(tech.toLowerCase()) || tech.toLowerCase().includes(pt))
      ).length
      score += techOverlap * 15
      if (techOverlap > 0) matchReason += `${techOverlap} technology matches, `

      // Feature overlap
      const projectFeatures = project.features_list.toLowerCase().split('|')
      const featureOverlap = analysis.features.filter(feature => 
        projectFeatures.some(pf => pf.includes(feature.toLowerCase()) || feature.toLowerCase().includes(pf))
      ).length
      score += featureOverlap * 10
      if (featureOverlap > 0) matchReason += `${featureOverlap} feature matches, `

      // Content similarity
      const ideaWords = idea.toLowerCase().split(' ')
      const projectText = `${project.name} ${project.description} ${project.ai_summary}`.toLowerCase()
      const contentMatch = ideaWords.filter(word => 
        word.length > 3 && projectText.includes(word)
      ).length
      score += contentMatch * 5
      if (contentMatch > 0) matchReason += `${contentMatch} content matches, `

      // GitHub stars bonus
      score += Math.min(project.github_stars / 10, 10)

      // Determine integration complexity
      let integrationComplexity: 'low' | 'medium' | 'high' = 'medium'
      if (techOverlap >= 3 && featureOverlap >= 2) integrationComplexity = 'low'
      else if (techOverlap <= 1 && featureOverlap <= 1) integrationComplexity = 'high'

      return {
        project,
        similarityScore: Math.min(score, 100),
        matchReason: matchReason.slice(0, -2) || 'General similarity',
        integrationComplexity
      }
    })

    return scoredProjects
      .sort((a, b) => b.similarityScore - a.similarityScore)
      .slice(0, limit)
  }

  // New: RAG-based similarity search using Python service
  async findSimilarProjectsRAG(userIdea: string, limit: number = 5): Promise<ProjectMatch[]> {
    try {
      // Check if RAG service is available
      const isHealthy = await ragClient.healthCheck()
      if (!isHealthy) {
        console.warn('RAG service not available, falling back to traditional search')
        return this.findSimilarProjects(userIdea, limit)
      }

      // Use RAG service
      const ragMatches = await ragClient.findSimilarProjects(userIdea, limit)
      
      // Convert RAG matches to ProjectMatch format
      const projectMatches: ProjectMatch[] = ragMatches.map(ragMatch => ({
        project: {
          id: ragMatch.id,
          name: ragMatch.name,
          description: ragMatch.description,
          project_url: ragMatch.project_url,
          demo_url: ragMatch.demo_url,
          github_url: ragMatch.github_url,
          detailed_description: ragMatch.description,
          ai_summary: ragMatch.ai_summary,
          architecture: '',
          components_list: '',
          dependencies_list: '',
          features_list: '',
          technologies_list: '',
          github_stars: ragMatch.github_stars,
          repo_license: '',
          contributors: '',
          ai_models_inferred: '',
          vector_db_inferred: '',
          frameworks_inferred: '',
          infrastructure_inferred: '',
          top_risks: '',
          setup_steps: '',
          integration_plan: '',
          deployment_notes: '',
          security_notes: '',
          testing_notes: '',
          api_endpoints_list: '',
          env_vars_list: '',
          services_list: '',
          date: ''
        },
        similarityScore: ragMatch.similarity_score,
        matchReason: ragMatch.match_reason,
        integrationComplexity: ragMatch.integration_complexity as 'low' | 'medium' | 'high'
      }))

      return projectMatches
    } catch (error) {
      console.error('RAG search failed, falling back to traditional search:', error)
      return this.findSimilarProjects(userIdea, limit)
    }
  }

  // New: Suggest system combinations
  async suggestProjectCombinations(primaryProjectId: number): Promise<SystemCombination[]> {
    const projects = await this.loadProjects()
    const primaryProject = projects.find(p => p.id === primaryProjectId)
    
    if (!primaryProject) return []

    const combinations: SystemCombination[] = []
    
    // Find complementary projects
    const complementaryProjects = projects
      .filter(p => p.id !== primaryProjectId)
      .map(project => {
        let complementarityScore = 0
        const missingComponents: string[] = []

        // Check for complementary technologies
        const primaryTechs = primaryProject.technologies_list.toLowerCase().split('|')
        const projectTechs = project.technologies_list.toLowerCase().split('|')
        
        const uniqueTechs = projectTechs.filter(tech => 
          !primaryTechs.some(pt => pt.includes(tech) || tech.includes(pt))
        )
        complementarityScore += uniqueTechs.length * 10

        // Check for complementary features
        const primaryFeatures = primaryProject.features_list.toLowerCase().split('|')
        const projectFeatures = project.features_list.toLowerCase().split('|')
        
        const uniqueFeatures = projectFeatures.filter(feature => 
          !primaryFeatures.some(pf => pf.includes(feature) || feature.includes(pf))
        )
        complementarityScore += uniqueFeatures.length * 8

        // Identify missing components
        if (!primaryTechs.some(tech => tech.includes('database')) && 
            projectTechs.some(tech => tech.includes('database'))) {
          missingComponents.push('Database')
        }
        if (!primaryTechs.some(tech => tech.includes('auth')) && 
            projectFeatures.some(feature => feature.includes('user'))) {
          missingComponents.push('Authentication')
        }
        if (!primaryFeatures.some(feature => feature.includes('api')) && 
            projectFeatures.some(feature => feature.includes('api'))) {
          missingComponents.push('API Layer')
        }

        return { project, complementarityScore, missingComponents }
      })
      .sort((a, b) => b.complementarityScore - a.complementarityScore)
      .slice(0, 3)

    // Create combination suggestions
    complementaryProjects.forEach(({ project, complementarityScore, missingComponents }) => {
      const totalScore = complementarityScore + (primaryProject.github_stars / 10)
      
      const integrationSteps = [
        `1. Set up ${primaryProject.name} as the core application`,
        `2. Integrate ${project.name} for ${missingComponents.join(', ')} functionality`,
        `3. Configure shared authentication and data flow`,
        `4. Deploy both applications with proper API communication`
      ]

      let estimatedTime = '4-6 weeks'
      if (complementarityScore > 50) estimatedTime = '6-8 weeks'
      else if (complementarityScore < 20) estimatedTime = '2-4 weeks'

      combinations.push({
        primaryProject,
        complementaryProjects: [project],
        totalScore,
        integrationSteps,
        estimatedDevelopmentTime: estimatedTime,
        missingComponents
      })
    })

    return combinations
  }

  // New: Get comprehensive analytics data
  async getAnalyticsData(): Promise<AnalyticsData> {
    const projects = await this.loadProjects()
    
    // Technology trends
    const frameworkCount: { [key: string]: number } = {}
    const aiModelCount: { [key: string]: number } = {}
    const vectorDBCount: { [key: string]: number } = {}
    const infrastructureCount: { [key: string]: number } = {}

    projects.forEach(project => {
      // Count frameworks
      const frameworks = project.frameworks_inferred.split('|').filter(f => f.trim())
      frameworks.forEach(framework => {
        const cleanFramework = framework.trim().toLowerCase()
        if (cleanFramework) {
          frameworkCount[cleanFramework] = (frameworkCount[cleanFramework] || 0) + 1
        }
      })

      // Count AI models
      const aiModels = project.ai_models_inferred.split('|').filter(m => m.trim())
      aiModels.forEach(model => {
        const cleanModel = model.trim().toLowerCase()
        if (cleanModel) {
          aiModelCount[cleanModel] = (aiModelCount[cleanModel] || 0) + 1
        }
      })

      // Count vector databases
      const vectorDBs = project.vector_db_inferred.split('|').filter(v => v.trim())
      vectorDBs.forEach(db => {
        const cleanDB = db.trim().toLowerCase()
        if (cleanDB) {
          vectorDBCount[cleanDB] = (vectorDBCount[cleanDB] || 0) + 1
        }
      })

      // Count infrastructure
      const infrastructure = project.infrastructure_inferred.split('|').filter(i => i.trim())
      infrastructure.forEach(infra => {
        const cleanInfra = infra.trim().toLowerCase()
        if (cleanInfra) {
          infrastructureCount[cleanInfra] = (infrastructureCount[cleanInfra] || 0) + 1
        }
      })
    })

    // Convert to arrays and calculate percentages
    const frameworks = Object.entries(frameworkCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([name, count]) => ({
        name,
        count,
        percentage: Math.round((count / projects.length) * 100)
      }))

    const aiModels = Object.entries(aiModelCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([name, count]) => ({
        name,
        count,
        percentage: Math.round((count / projects.length) * 100)
      }))

    const vectorDBs = Object.entries(vectorDBCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([name, count]) => ({
        name,
        count,
        percentage: Math.round((count / projects.length) * 100)
      }))

    const infrastructure = Object.entries(infrastructureCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([name, count]) => ({
        name,
        count,
        percentage: Math.round((count / projects.length) * 100)
      }))

    // Project statistics
    const totalStars = projects.reduce((sum, p) => sum + p.github_stars, 0)
    const avgStars = Math.round(totalStars / projects.length)
    
    // Category analysis
    const categoryCount: { [key: string]: number } = {}
    projects.forEach(project => {
      const category = this.categorizeProject(project)
      categoryCount[category] = (categoryCount[category] || 0) + 1
    })

    const topCategories = Object.entries(categoryCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
      .map(([name, count]) => ({ name, count }))

    // Recent projects (last 6 months)
    const sixMonthsAgo = new Date()
    sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6)
    const recentProjects = projects.filter(project => {
      if (!project.date) return false
      const projectDate = new Date(project.date)
      return projectDate > sixMonthsAgo
    }).length

    // Market insights
    const gaps = this.identifyMarketGaps(projects)
    const opportunities = this.identifyOpportunities(projects)
    const trendingTechnologies = this.getTrendingTechnologies(projects)
    const emergingCategories = this.getEmergingCategories(projects)

    return {
      technologyTrends: {
        frameworks,
        aiModels,
        vectorDBs,
        infrastructure
      },
      projectStats: {
        totalProjects: projects.length,
        totalStars,
        avgStars,
        topCategories,
        recentProjects
      },
      marketInsights: {
        gaps,
        opportunities,
        trendingTechnologies,
        emergingCategories
      }
    }
  }

  // Helper methods for analytics
  private categorizeProject(project: Project): string {
    const text = `${project.name} ${project.description} ${project.ai_summary}`.toLowerCase()
    
    if (text.includes('ai') || text.includes('machine learning') || text.includes('chatbot')) {
      return 'AI/ML Applications'
    } else if (text.includes('crm') || text.includes('business') || text.includes('management')) {
      return 'Business Tools'
    } else if (text.includes('web') || text.includes('website') || text.includes('app')) {
      return 'Web Applications'
    } else if (text.includes('mobile') || text.includes('app')) {
      return 'Mobile Applications'
    } else if (text.includes('game') || text.includes('gaming')) {
      return 'Gaming'
    } else if (text.includes('education') || text.includes('learning')) {
      return 'Education'
    } else if (text.includes('developer') || text.includes('tool')) {
      return 'Developer Tools'
    }
    
    return 'Other'
  }

  private identifyMarketGaps(projects: Project[]): string[] {
    const gaps = []
    
    // Check for missing combinations
    const hasAICRM = projects.some(p => 
      p.description.toLowerCase().includes('ai') && 
      p.description.toLowerCase().includes('crm')
    )
    if (!hasAICRM) gaps.push('AI-powered CRM solutions')

    const hasRealTimeAnalytics = projects.some(p => 
      p.description.toLowerCase().includes('real-time') && 
      p.description.toLowerCase().includes('analytics')
    )
    if (!hasRealTimeAnalytics) gaps.push('Real-time analytics platforms')

    const hasMobileAI = projects.some(p => 
      p.description.toLowerCase().includes('mobile') && 
      p.description.toLowerCase().includes('ai')
    )
    if (!hasMobileAI) gaps.push('Mobile AI applications')

    return gaps
  }

  private identifyOpportunities(projects: Project[]): string[] {
    const opportunities = []
    
    // High-star projects indicate market demand
    const highStarProjects = projects.filter(p => p.github_stars > 100)
    if (highStarProjects.length > 0) {
      opportunities.push('High-performing projects show strong market demand')
    }

    // Recent projects indicate emerging trends
    const recentProjects = projects.filter(p => {
      if (!p.date) return false
      const projectDate = new Date(p.date)
      const sixMonthsAgo = new Date()
      sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6)
      return projectDate > sixMonthsAgo
    })
    
    if (recentProjects.length > 50) {
      opportunities.push('High activity in recent months indicates growing market')
    }

    return opportunities
  }

  private getTrendingTechnologies(projects: Project[]): string[] {
    const techCount: { [key: string]: number } = {}
    
    projects.forEach(project => {
      const techs = project.technologies_list.split('|').filter(t => t.trim())
      techs.forEach(tech => {
        const cleanTech = tech.trim().toLowerCase()
        if (cleanTech) {
          techCount[cleanTech] = (techCount[cleanTech] || 0) + 1
        }
      })
    })

    return Object.entries(techCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
      .map(([tech]) => tech)
  }

  private getEmergingCategories(projects: Project[]): string[] {
    const recentProjects = projects.filter(p => {
      if (!p.date) return false
      const projectDate = new Date(p.date)
      const threeMonthsAgo = new Date()
      threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3)
      return projectDate > threeMonthsAgo
    })

    const categoryCount: { [key: string]: number } = {}
    recentProjects.forEach(project => {
      const category = this.categorizeProject(project)
      categoryCount[category] = (categoryCount[category] || 0) + 1
    })

    return Object.entries(categoryCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([category]) => category)
  }

  async getSimilarProjects(projectId: number, limit: number = 5): Promise<Project[]> {
    const projects = await this.loadProjects()
    const targetProject = projects.find(p => p.id === projectId)
    
    if (!targetProject) return []

    // Simple similarity scoring based on technologies and features
    const scoredProjects = projects
      .filter(p => p.id !== projectId)
      .map(project => {
        let score = 0
        
        // Technology similarity
        const targetTechs = targetProject.technologies_list.toLowerCase().split('|')
        const projectTechs = project.technologies_list.toLowerCase().split('|')
        const techOverlap = targetTechs.filter(tech => 
          projectTechs.some(pt => pt.includes(tech) || tech.includes(pt))
        ).length
        score += techOverlap * 10

        // Framework similarity
        if (targetProject.frameworks_inferred && project.frameworks_inferred) {
          const targetFrameworks = targetProject.frameworks_inferred.toLowerCase().split('|')
          const projectFrameworks = project.frameworks_inferred.toLowerCase().split('|')
          const frameworkOverlap = targetFrameworks.filter(fw => 
            projectFrameworks.some(pf => pf.includes(fw) || fw.includes(pf))
          ).length
          score += frameworkOverlap * 8
        }

        // AI model similarity
        if (targetProject.ai_models_inferred && project.ai_models_inferred) {
          const targetModels = targetProject.ai_models_inferred.toLowerCase().split('|')
          const projectModels = project.ai_models_inferred.toLowerCase().split('|')
          const modelOverlap = targetModels.filter(model => 
            projectModels.some(pm => pm.includes(model) || model.includes(pm))
          ).length
          score += modelOverlap * 12
        }

        return { project, score }
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)

    return scoredProjects.map(sp => sp.project)
  }

  async getProjectStats() {
    const projects = await this.loadProjects()
    
    const stats = {
      totalProjects: projects.length,
      totalStars: projects.reduce((sum, p) => sum + p.github_stars, 0),
      avgStars: Math.round(projects.reduce((sum, p) => sum + p.github_stars, 0) / projects.length),
      topTechnologies: this.getTopTechnologies(projects),
      topFrameworks: this.getTopFrameworks(projects),
      topAIModels: this.getTopAIModels(projects)
    }

    return stats
  }

  private getTopTechnologies(projects: Project[]): string[] {
    const techCount: { [key: string]: number } = {}
    
    projects.forEach(project => {
      const techs = project.technologies_list.split('|').filter(t => t.trim())
      techs.forEach(tech => {
        const cleanTech = tech.trim().toLowerCase()
        if (cleanTech) {
          techCount[cleanTech] = (techCount[cleanTech] || 0) + 1
        }
      })
    })

    return Object.entries(techCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([tech]) => tech)
  }

  private getTopFrameworks(projects: Project[]): string[] {
    const frameworkCount: { [key: string]: number } = {}
    
    projects.forEach(project => {
      const frameworks = project.frameworks_inferred.split('|').filter(f => f.trim())
      frameworks.forEach(framework => {
        const cleanFramework = framework.trim().toLowerCase()
        if (cleanFramework) {
          frameworkCount[cleanFramework] = (frameworkCount[cleanFramework] || 0) + 1
        }
      })
    })

    return Object.entries(frameworkCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([framework]) => framework)
  }

  private getTopAIModels(projects: Project[]): string[] {
    const modelCount: { [key: string]: number } = {}
    
    projects.forEach(project => {
      const models = project.ai_models_inferred.split('|').filter(m => m.trim())
      models.forEach(model => {
        const cleanModel = model.trim().toLowerCase()
        if (cleanModel) {
          modelCount[cleanModel] = (modelCount[cleanModel] || 0) + 1
        }
      })
    })

    return Object.entries(modelCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([model]) => model)
  }
}

export const dataLoader = new DataLoader()
