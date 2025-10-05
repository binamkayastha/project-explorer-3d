import { motion } from 'framer-motion'
import { ExternalLink, Github, Star, Calendar, Users, Zap, Shield, Code } from 'lucide-react'
import { Project } from '@/utils/dataLoader'

interface ProjectCardProps {
  project: Project
  onClick?: () => void
  className?: string
}

const ProjectCard = ({ project, onClick, className = '' }: ProjectCardProps) => {
  const formatDate = (dateString: string) => {
    if (!dateString) return 'Unknown'
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    } catch {
      return dateString
    }
  }

  const getTechnologies = () => {
    if (!project.technologies_list) return []
    return project.technologies_list.split('|').filter(t => t.trim()).slice(0, 5)
  }

  const getFrameworks = () => {
    if (!project.frameworks_inferred) return []
    return project.frameworks_inferred.split('|').filter(f => f.trim()).slice(0, 3)
  }

  const getAIModels = () => {
    if (!project.ai_models_inferred) return []
    return project.ai_models_inferred.split('|').filter(m => m.trim()).slice(0, 3)
  }

  return (
    <motion.div
      whileHover={{ y: -5, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`glass-card p-6 cursor-pointer transition-all duration-300 hover:shadow-xl hover:shadow-primary-500/20 ${className}`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 line-clamp-2">
            {project.name}
          </h3>
          <p className="text-gray-600 dark:text-gray-300 text-sm line-clamp-2">
            {project.description}
          </p>
        </div>
        <div className="flex items-center space-x-2 ml-4">
          {project.github_stars > 0 && (
            <div className="flex items-center space-x-1 text-sundai-600">
              <Star className="w-4 h-4 fill-current" />
              <span className="text-sm font-medium">{project.github_stars}</span>
            </div>
          )}
        </div>
      </div>

      {/* Stats Row */}
      <div className="flex items-center space-x-4 mb-4 text-sm text-gray-500 dark:text-gray-400">
        <div className="flex items-center space-x-1">
          <Calendar className="w-4 h-4" />
          <span>{formatDate(project.date)}</span>
        </div>
        {project.contributors && (
          <div className="flex items-center space-x-1">
            <Users className="w-4 h-4" />
            <span>{project.contributors.split('|').length} contributors</span>
          </div>
        )}
      </div>

      {/* Technologies */}
      {getTechnologies().length > 0 && (
        <div className="mb-4">
          <div className="flex items-center space-x-2 mb-2">
            <Code className="w-4 h-4 text-primary-500" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Technologies</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {getTechnologies().map((tech, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-xs rounded-full"
              >
                {tech.trim()}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Frameworks */}
      {getFrameworks().length > 0 && (
        <div className="mb-4">
          <div className="flex items-center space-x-2 mb-2">
            <Zap className="w-4 h-4 text-sundai-500" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Frameworks</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {getFrameworks().map((framework, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-sundai-100 dark:bg-sundai-900/30 text-sundai-700 dark:text-sundai-300 text-xs rounded-full"
              >
                {framework.trim()}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* AI Models */}
      {getAIModels().length > 0 && (
        <div className="mb-4">
          <div className="flex items-center space-x-2 mb-2">
            <Shield className="w-4 h-4 text-green-500" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">AI Models</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {getAIModels().map((model, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs rounded-full"
              >
                {model.trim()}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Links */}
      <div className="flex items-center space-x-3 pt-4 border-t border-dark-100 dark:border-white/10">
        {project.github_url && (
          <a
            href={project.github_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
            onClick={(e) => e.stopPropagation()}
          >
            <Github className="w-4 h-4" />
            <span className="text-sm">GitHub</span>
          </a>
        )}
        {project.demo_url && (
          <a
            href={project.demo_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
            onClick={(e) => e.stopPropagation()}
          >
            <ExternalLink className="w-4 h-4" />
            <span className="text-sm">Demo</span>
          </a>
        )}
        {project.project_url && (
          <a
            href={project.project_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
            onClick={(e) => e.stopPropagation()}
          >
            <ExternalLink className="w-4 h-4" />
            <span className="text-sm">Project</span>
          </a>
        )}
      </div>
    </motion.div>
  )
}

export default ProjectCard
