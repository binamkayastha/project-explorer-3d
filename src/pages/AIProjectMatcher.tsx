import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Filter, Sparkles, Database, Star, Users, Zap } from 'lucide-react'
import { dataLoader, Project, SearchFilters } from '@/utils/dataLoader'
import ProjectCard from '@/components/ProjectCard'
import ProjectModal from '@/components/ProjectModal'
import toast from 'react-hot-toast'

const AIProjectMatcher = () => {
  const [filteredProjects, setFilteredProjects] = useState<Project[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState<SearchFilters>({
    technologies: [],
    frameworks: [],
    aiModels: [],
    categories: [],
    minStars: 0,
    maxStars: 0
  })
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [stats, setStats] = useState<any>(null)
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  useEffect(() => {
    performSearch()
  }, [searchQuery, filters])

  const loadData = async () => {
    try {
      setIsLoading(true)
      const [projectsData, statsData] = await Promise.all([
        dataLoader.loadProjects(),
        dataLoader.getProjectStats()
      ])
      setFilteredProjects(projectsData)
      setStats(statsData)
    } catch (error) {
      console.error('Error loading data:', error)
      toast.error('Failed to load projects')
    } finally {
      setIsLoading(false)
    }
  }

  const performSearch = async () => {
    try {
      const results = await dataLoader.searchProjects(searchQuery, filters)
      setFilteredProjects(results)
    } catch (error) {
      console.error('Error searching projects:', error)
    }
  }

  const handleProjectClick = (project: Project) => {
    setSelectedProject(project)
    setIsModalOpen(true)
  }

  const handleFilterChange = (filterType: keyof SearchFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }))
  }

  const clearFilters = () => {
    setFilters({
      technologies: [],
      frameworks: [],
      aiModels: [],
      categories: [],
      minStars: 0,
      maxStars: 0
    })
    setSearchQuery('')
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
      {/* Header */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-500/20 via-sundai-500/20 to-primary-600/20" />
        <div className="relative px-6 py-12">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center"
            >
              <div className="flex items-center justify-center space-x-2 mb-4">
                <Sparkles className="w-8 h-8 text-primary-400" />
                <h1 className="text-4xl font-bold gradient-text">
                  AI Project Matcher
                </h1>
              </div>
                             <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                 Discover the perfect AI projects from our curated collection of 300+ innovative solutions. 
                 Find projects that match your ideas, technology stack, and development goals.
               </p>
            </motion.div>

            {/* Stats */}
            {stats && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-12"
              >
                <div className="glass-card p-6 text-center">
                  <Database className="w-8 h-8 text-primary-400 mx-auto mb-2" />
                                     <div className="text-2xl font-bold text-white">{stats.totalProjects}</div>
                   <div className="text-gray-300">Total Projects</div>
                 </div>
                 <div className="glass-card p-6 text-center">
                   <Star className="w-8 h-8 text-sundai-400 mx-auto mb-2" />
                   <div className="text-2xl font-bold text-white">{stats.totalStars}</div>
                   <div className="text-gray-300">Total Stars</div>
                 </div>
                 <div className="glass-card p-6 text-center">
                   <Users className="w-8 h-8 text-green-400 mx-auto mb-2" />
                   <div className="text-2xl font-bold text-white">{stats.avgStars}</div>
                   <div className="text-gray-300">Avg Stars</div>
                 </div>
                 <div className="glass-card p-6 text-center">
                   <Zap className="w-8 h-8 text-purple-400 mx-auto mb-2" />
                   <div className="text-2xl font-bold text-white">{stats.topTechnologies.length}</div>
                   <div className="text-gray-300">Technologies</div>
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          <div className="glass-card p-6 mb-8">
            {/* Search Bar */}
            <div className="flex items-center space-x-4 mb-6">
              <div className="flex-1 relative">
                                 <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                 <input
                   type="text"
                   placeholder="Search projects by name, description, technologies..."
                   value={searchQuery}
                   onChange={(e) => setSearchQuery(e.target.value)}
                   className="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                 />
              </div>
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center space-x-2 px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white hover:bg-white/20 transition-colors"
              >
                <Filter className="w-5 h-5" />
                <span>Filters</span>
              </button>
            </div>

            {/* Filters Panel */}
            <AnimatePresence>
              {showFilters && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-6 border-t border-white/20">
                    {/* Technology Filter */}
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Technologies
                      </label>
                      <select
                        multiple
                        value={filters.technologies}
                        onChange={(e) => {
                          const values = Array.from(e.target.selectedOptions, option => option.value)
                          handleFilterChange('technologies', values)
                        }}
                        className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                      >
                        {stats?.topTechnologies.map((tech: string) => (
                          <option key={tech} value={tech} className="bg-dark-800">
                            {tech}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Framework Filter */}
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Frameworks
                      </label>
                      <select
                        multiple
                        value={filters.frameworks}
                        onChange={(e) => {
                          const values = Array.from(e.target.selectedOptions, option => option.value)
                          handleFilterChange('frameworks', values)
                        }}
                        className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                      >
                        {stats?.topFrameworks.map((framework: string) => (
                          <option key={framework} value={framework} className="bg-dark-800">
                            {framework}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* AI Models Filter */}
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        AI Models
                      </label>
                      <select
                        multiple
                        value={filters.aiModels}
                        onChange={(e) => {
                          const values = Array.from(e.target.selectedOptions, option => option.value)
                          handleFilterChange('aiModels', values)
                        }}
                        className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                      >
                        {stats?.topAIModels.map((model: string) => (
                          <option key={model} value={model} className="bg-dark-800">
                            {model}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Stars Range */}
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Min Stars
                      </label>
                      <input
                        type="number"
                        value={filters.minStars || ''}
                        onChange={(e) => handleFilterChange('minStars', parseInt(e.target.value) || 0)}
                        className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                        placeholder="0"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Max Stars
                      </label>
                      <input
                        type="number"
                        value={filters.maxStars || ''}
                        onChange={(e) => handleFilterChange('maxStars', parseInt(e.target.value) || 0)}
                        className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                        placeholder="∞"
                      />
                    </div>

                    <div className="flex items-end">
                      <button
                        onClick={clearFilters}
                        className="w-full px-4 py-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-400 hover:bg-red-500/30 transition-colors"
                      >
                        Clear Filters
                      </button>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Results */}
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-white">
                {filteredProjects.length} Projects Found
              </h2>
                             {searchQuery && (
                 <p className="text-gray-300">
                   Results for "{searchQuery}"
                 </p>
               )}
            </div>
          </div>

          {/* Loading State */}
          {isLoading && (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
          )}

          {/* Projects Grid */}
          {!isLoading && (
            <motion.div
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              <AnimatePresence>
                {filteredProjects.map((project) => (
                  <motion.div
                    key={project.id}
                    variants={itemVariants}
                    layout
                  >
                    <ProjectCard
                      project={project}
                      onClick={() => handleProjectClick(project)}
                    />
                  </motion.div>
                ))}
              </AnimatePresence>
            </motion.div>
          )}

          {/* No Results */}
          {!isLoading && filteredProjects.length === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-12"
            >
              <div className="glass-card p-8 max-w-md mx-auto">
                                 <Search className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                 <h3 className="text-xl font-semibold text-white mb-2">No projects found</h3>
                 <p className="text-gray-300 mb-4">
                   Try adjusting your search terms or filters to find more projects.
                 </p>
                <button
                  onClick={clearFilters}
                  className="btn-primary"
                >
                  Clear Filters
                </button>
              </div>
            </motion.div>
          )}
        </div>
      </div>

      {/* Project Modal */}
      <ProjectModal
        project={selectedProject}
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false)
          setSelectedProject(null)
        }}
      />
    </div>
  )
}

export default AIProjectMatcher
