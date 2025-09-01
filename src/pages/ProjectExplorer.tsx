import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Sparkles, 
  Lightbulb, 
  Target, 
  Zap, 
  Clock, 
  Code, 
  Database, 
  Users, 
  Star, 
  ArrowRight,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Link,
  Copy,
  ExternalLink,
  Box
} from 'lucide-react'
import { 
  dataLoader, 
  Project, 
  IdeaAnalysis, 
  ProjectMatch, 
  SystemCombination 
} from '@/utils/dataLoader'
import ProjectCard from '@/components/ProjectCard'
import ProjectModal from '@/components/ProjectModal'
import ThreeDIdeaVisualizer from '@/components/3DIdeaVisualizer'
import toast from 'react-hot-toast'

const ProjectExplorer = () => {
  const [userIdea, setUserIdea] = useState('')
  const [ideaAnalysis, setIdeaAnalysis] = useState<IdeaAnalysis | null>(null)
  const [projectMatches, setProjectMatches] = useState<ProjectMatch[]>([])
  const [systemCombinations, setSystemCombinations] = useState<SystemCombination[]>([])
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [activeTab, setActiveTab] = useState<'analysis' | 'matches' | 'combinations' | '3d'>('analysis')

  const handleAnalyzeIdea = async () => {
    if (!userIdea.trim()) {
      toast.error('Please enter your idea first')
      return
    }

    setIsAnalyzing(true)
    try {
      const analysis = await dataLoader.analyzeUserIdea(userIdea)
      const matches = await dataLoader.findSimilarProjects(userIdea, 5)
      
      setIdeaAnalysis(analysis)
      setProjectMatches(matches)
      
      // Get system combinations for the top match
      if (matches.length > 0) {
        const combinations = await dataLoader.suggestProjectCombinations(matches[0].project.id)
        setSystemCombinations(combinations)
      }
      
      toast.success('Idea analyzed successfully!')
    } catch (error) {
      console.error('Error analyzing idea:', error)
      toast.error('Failed to analyze idea')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleProjectClick = (project: Project) => {
    setSelectedProject(project)
    setIsModalOpen(true)
  }

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'low': return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/30'
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/30'
      case 'high': return 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/30'
      default: return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/30'
    }
  }

  const getIntegrationComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'low': return 'text-green-600'
      case 'medium': return 'text-yellow-600'
      case 'high': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast.success('Copied to clipboard!')
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
                  Project Explorer
                </h1>
              </div>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Describe your idea and discover the perfect AI projects to build it. 
                Get intelligent matches, system combinations, and integration roadmaps.
              </p>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Idea Input */}
          <div className="glass-card p-8 mb-8">
            <div className="flex items-center space-x-2 mb-6">
              <Lightbulb className="w-6 h-6 text-primary-400" />
              <h2 className="text-2xl font-bold text-white">Describe Your Idea</h2>
            </div>
            
            <div className="space-y-4">
              <textarea
                value={userIdea}
                onChange={(e) => setUserIdea(e.target.value)}
                placeholder="e.g., I want to build a CRM tool for real estate agents with AI-powered lead scoring and automated follow-ups..."
                className="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                rows={4}
              />
              
              <div className="flex justify-end">
                <button
                  onClick={handleAnalyzeIdea}
                  disabled={isAnalyzing || !userIdea.trim()}
                  className="btn-primary flex items-center space-x-2"
                >
                  {isAnalyzing ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      <span>Analyze Idea</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Results */}
          {ideaAnalysis && (
            <div className="space-y-8">
              {/* Analysis Results */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-card p-8"
              >
                <div className="flex items-center space-x-2 mb-6">
                  <Target className="w-6 h-6 text-primary-400" />
                  <h2 className="text-2xl font-bold text-white">Idea Analysis</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {/* Category */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-medium text-gray-400">Category</h3>
                    <p className="text-lg font-semibold text-white">{ideaAnalysis.category}</p>
                  </div>

                  {/* Complexity */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-medium text-gray-400">Complexity</h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getComplexityColor(ideaAnalysis.complexity)}`}>
                      {ideaAnalysis.complexity.charAt(0).toUpperCase() + ideaAnalysis.complexity.slice(1)}
                    </span>
                  </div>

                  {/* Estimated Time */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-medium text-gray-400">Estimated Time</h3>
                    <div className="flex items-center space-x-2">
                      <Clock className="w-4 h-4 text-gray-400" />
                      <span className="text-lg font-semibold text-white">{ideaAnalysis.estimatedTime}</span>
                    </div>
                  </div>

                  {/* Technologies */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-medium text-gray-400">Technologies</h3>
                    <div className="flex flex-wrap gap-2">
                      {ideaAnalysis.technologies.map((tech, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-xs rounded-full"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Features */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-medium text-gray-400">Features</h3>
                    <div className="flex flex-wrap gap-2">
                      {ideaAnalysis.features.map((feature, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-sundai-100 dark:bg-sundai-900/30 text-sundai-700 dark:text-sundai-300 text-xs rounded-full"
                        >
                          {feature}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Key Components */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-medium text-gray-400">Key Components</h3>
                    <div className="flex flex-wrap gap-2">
                      {ideaAnalysis.keyComponents.map((component, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs rounded-full"
                        >
                          {component}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Navigation Tabs */}
              <div className="flex border-b border-white/20">
                <button
                  onClick={() => setActiveTab('matches')}
                  className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-colors ${
                    activeTab === 'matches'
                      ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
                      : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                  }`}
                >
                  <Target className="w-4 h-4" />
                  <span>Project Matches ({projectMatches.length})</span>
                </button>
                <button
                  onClick={() => setActiveTab('combinations')}
                  className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-colors ${
                    activeTab === 'combinations'
                      ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
                      : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                  }`}
                >
                  <Zap className="w-4 h-4" />
                  <span>System Combinations ({systemCombinations.length})</span>
                </button>
                <button
                  onClick={() => setActiveTab('3d')}
                  className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-colors ${
                    activeTab === '3d'
                      ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
                      : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                  }`}
                >
                  <Box className="w-4 h-4" />
                  <span>3D Visualization</span>
                </button>
              </div>

              {/* Project Matches */}
              {activeTab === 'matches' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-6"
                >
                  <div className="flex items-center space-x-2 mb-6">
                    <Target className="w-6 h-6 text-primary-400" />
                    <h2 className="text-2xl font-bold text-white">Best Project Matches</h2>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {projectMatches.map((match, index) => (
                      <motion.div
                        key={match.project.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="glass-card p-6 cursor-pointer hover:shadow-xl hover:shadow-primary-500/20 transition-all duration-300"
                        onClick={() => handleProjectClick(match.project)}
                      >
                        {/* Match Score */}
                        <div className="flex items-center justify-between mb-4">
                          <div className="flex items-center space-x-2">
                            <div className="w-12 h-12 rounded-full bg-gradient-to-r from-primary-500 to-sundai-500 flex items-center justify-center">
                              <span className="text-white font-bold text-sm">{match.similarityScore}%</span>
                            </div>
                            <div>
                              <h3 className="text-lg font-bold text-white">{match.project.name}</h3>
                              <p className="text-sm text-gray-400">Match Score</p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className={`text-sm font-medium ${getIntegrationComplexityColor(match.integrationComplexity)}`}>
                              {match.integrationComplexity} integration
                            </span>
                            {match.integrationComplexity === 'low' && <CheckCircle className="w-4 h-4 text-green-500" />}
                            {match.integrationComplexity === 'high' && <AlertCircle className="w-4 h-4 text-red-500" />}
                          </div>
                        </div>

                        {/* Project Description */}
                        <p className="text-gray-300 text-sm mb-4 line-clamp-2">
                          {match.project.description}
                        </p>

                        {/* Match Reason */}
                        <div className="mb-4">
                          <h4 className="text-sm font-medium text-gray-400 mb-2">Why this matches:</h4>
                          <p className="text-sm text-gray-300">{match.matchReason}</p>
                        </div>

                        {/* Project Stats */}
                        <div className="flex items-center space-x-4 text-sm text-gray-400">
                          {match.project.github_stars > 0 && (
                            <div className="flex items-center space-x-1">
                              <Star className="w-4 h-4 fill-current text-sundai-400" />
                              <span>{match.project.github_stars}</span>
                            </div>
                          )}
                          {match.project.contributors && (
                            <div className="flex items-center space-x-1">
                              <Users className="w-4 h-4" />
                              <span>{match.project.contributors.split('|').length} contributors</span>
                            </div>
                          )}
                        </div>

                        {/* Action Buttons */}
                        <div className="flex items-center space-x-2 mt-4 pt-4 border-t border-white/20">
                          <button
                            onClick={(e) => {
                              e.stopPropagation()
                              handleProjectClick(match.project)
                            }}
                            className="flex items-center space-x-1 text-primary-400 hover:text-primary-300 transition-colors"
                          >
                            <ExternalLink className="w-4 h-4" />
                            <span className="text-sm">View Details</span>
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation()
                              copyToClipboard(match.project.github_url || match.project.project_url)
                            }}
                            className="flex items-center space-x-1 text-gray-400 hover:text-gray-300 transition-colors"
                          >
                            <Copy className="w-4 h-4" />
                            <span className="text-sm">Copy URL</span>
                          </button>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )}

              {/* 3D Visualization */}
              {activeTab === '3d' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-6"
                >
                  <div className="flex items-center space-x-2 mb-6">
                    <Box className="w-6 h-6 text-primary-400" />
                    <h2 className="text-2xl font-bold text-white">3D Idea Ecosystem</h2>
                  </div>

                  {ideaAnalysis && projectMatches.length > 0 ? (
                    <div className="space-y-6">
                      {/* 3D Visualization Component */}
                      <ThreeDIdeaVisualizer
                        ideaAnalysis={ideaAnalysis}
                        projectMatches={projectMatches}
                        onNodeClick={(node) => {
                          if (node.type === 'project') {
                            handleProjectClick(node.data)
                          }
                        }}
                      />

                      {/* 3D Visualization Info */}
                      <div className="glass-card p-6">
                        <h3 className="text-lg font-bold text-white mb-4">How to Use the 3D Visualization</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div>
                            <h4 className="font-semibold text-white mb-2">Interactive Controls</h4>
                            <ul className="space-y-2 text-sm text-gray-300">
                              <li>• <strong>Drag:</strong> Rotate the view around your idea</li>
                              <li>• <strong>Scroll:</strong> Zoom in and out</li>
                              <li>• <strong>Click nodes:</strong> View project details</li>
                              <li>• <strong>Hover:</strong> Highlight connections</li>
                            </ul>
                          </div>
                          <div>
                            <h4 className="font-semibold text-white mb-2">Visual Elements</h4>
                            <ul className="space-y-2 text-sm text-gray-300">
                              <li>• <strong>💡 Blue Node:</strong> Your idea (center)</li>
                              <li>• <strong>🔗 Colored Nodes:</strong> Project matches</li>
                              <li>• <strong>🚀 Green Nodes:</strong> AI suggestions</li>
                              <li>• <strong>Dashed Lines:</strong> Project relationships</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="glass-card p-8 text-center">
                      <Box className="w-16 h-16 text-primary-400 mx-auto mb-4" />
                      <h3 className="text-xl font-bold text-white mb-2">No Data to Visualize</h3>
                      <p className="text-gray-300 mb-4">
                        Analyze your idea first to see the interactive 3D visualization of your project ecosystem.
                      </p>
                      <button
                        onClick={() => setActiveTab('analysis')}
                        className="btn-primary"
                      >
                        Go to Analysis
                      </button>
                    </div>
                  )}
                </motion.div>
              )}

              {/* System Combinations */}
              {activeTab === 'combinations' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-6"
                >
                  <div className="flex items-center space-x-2 mb-6">
                    <Zap className="w-6 h-6 text-primary-400" />
                    <h2 className="text-2xl font-bold text-white">System Combinations</h2>
                  </div>

                  <div className="space-y-6">
                    {systemCombinations.map((combination, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="glass-card p-6"
                      >
                        {/* Combination Header */}
                        <div className="flex items-center justify-between mb-6">
                          <div>
                            <h3 className="text-xl font-bold text-white mb-2">
                              {combination.primaryProject.name} + {combination.complementaryProjects[0].name}
                            </h3>
                            <p className="text-gray-400">
                              Build your solution by combining these complementary projects
                            </p>
                          </div>
                          <div className="text-right">
                            <div className="text-2xl font-bold text-primary-400">{combination.totalScore.toFixed(0)}</div>
                            <div className="text-sm text-gray-400">Combination Score</div>
                          </div>
                        </div>

                        {/* Projects Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                          {/* Primary Project */}
                          <div className="p-4 bg-white/5 rounded-lg">
                            <h4 className="font-semibold text-white mb-2">Primary Project</h4>
                            <ProjectCard
                              project={combination.primaryProject}
                              onClick={() => handleProjectClick(combination.primaryProject)}
                              className="!p-4 !bg-transparent"
                            />
                          </div>

                          {/* Complementary Project */}
                          <div className="p-4 bg-white/5 rounded-lg">
                            <h4 className="font-semibold text-white mb-2">Complementary Project</h4>
                            <ProjectCard
                              project={combination.complementaryProjects[0]}
                              onClick={() => handleProjectClick(combination.complementaryProjects[0])}
                              className="!p-4 !bg-transparent"
                            />
                          </div>
                        </div>

                        {/* Integration Details */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          {/* Integration Steps */}
                          <div>
                            <h4 className="font-semibold text-white mb-3 flex items-center space-x-2">
                              <TrendingUp className="w-4 h-4 text-primary-400" />
                              <span>Integration Steps</span>
                            </h4>
                            <ol className="space-y-2">
                              {combination.integrationSteps.map((step, stepIndex) => (
                                <li key={stepIndex} className="flex items-start space-x-2 text-sm text-gray-300">
                                  <span className="w-5 h-5 rounded-full bg-primary-500 text-white text-xs flex items-center justify-center flex-shrink-0 mt-0.5">
                                    {stepIndex + 1}
                                  </span>
                                  <span>{step}</span>
                                </li>
                              ))}
                            </ol>
                          </div>

                          {/* Additional Info */}
                          <div className="space-y-4">
                            {/* Development Time */}
                            <div>
                              <h4 className="font-semibold text-white mb-2 flex items-center space-x-2">
                                <Clock className="w-4 h-4 text-primary-400" />
                                <span>Development Time</span>
                              </h4>
                              <p className="text-gray-300">{combination.estimatedDevelopmentTime}</p>
                            </div>

                            {/* Missing Components */}
                            <div>
                              <h4 className="font-semibold text-white mb-2 flex items-center space-x-2">
                                <Code className="w-4 h-4 text-primary-400" />
                                <span>Missing Components</span>
                              </h4>
                              <div className="flex flex-wrap gap-2">
                                {combination.missingComponents.map((component, compIndex) => (
                                  <span
                                    key={compIndex}
                                    className="px-2 py-1 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 text-xs rounded-full"
                                  >
                                    {component}
                                  </span>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )}
            </div>
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

export default ProjectExplorer
