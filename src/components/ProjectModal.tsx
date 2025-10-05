import { motion, AnimatePresence } from 'framer-motion'
import { X, ExternalLink, Github, Star, Calendar, Users, Code, Shield, AlertTriangle, BookOpen, TrendingUp } from 'lucide-react'
import { Project } from '@/utils/dataLoader'
import { useState } from 'react'

interface ProjectModalProps {
  project: Project | null
  onClose: () => void
  isOpen: boolean
}

const ProjectModal = ({ project, onClose, isOpen }: ProjectModalProps) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'technology' | 'engagement'>('overview')

  if (!project) return null

  const formatDate = (dateString: string) => {
    if (!dateString) return 'Unknown'
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    } catch {
      return dateString
    }
  }

  const getTechnologies = () => {
    if (!project.technologies_list) return []
    return project.technologies_list.split('|').filter(t => t.trim())
  }

  const getFrameworks = () => {
    if (!project.frameworks_inferred) return []
    return project.frameworks_inferred.split('|').filter(f => f.trim())
  }

  const getAIModels = () => {
    if (!project.ai_models_inferred) return []
    return project.ai_models_inferred.split('|').filter(m => m.trim())
  }

  const getFeatures = () => {
    if (!project.features_list) return []
    return project.features_list.split('|').filter(f => f.trim())
  }

  const getRisks = () => {
    if (!project.top_risks) return []
    return project.top_risks.split('|').filter(r => r.trim())
  }

  const tabs = [
    { id: 'overview', label: 'Project Overview', icon: BookOpen },
    { id: 'technology', label: 'Technology Analysis', icon: Code },
    { id: 'engagement', label: 'Engagement Strategy', icon: TrendingUp }
  ]

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="glass-card w-full max-w-4xl max-h-[90vh] overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-white/20">
              <div className="flex-1">
                                 <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                   {project.name}
                 </h2>
                 <p className="text-gray-600 dark:text-gray-300">
                   {project.description}
                 </p>
              </div>
                <button
                 onClick={onClose}
                 className="p-2 rounded-full bg-dark-700 text-white hover:bg-dark-600 transition-colors"
                 aria-label="Close project details"
               >
                 <X className="w-6 h-6" />
               </button>
            </div>

                         {/* Stats Bar */}
             <div className="flex items-center space-x-6 p-4 bg-white/5 border-b border-white/10">
               <div className="flex items-center space-x-2">
                 <Calendar className="w-4 h-4 text-gray-500" />
                 <span className="text-sm text-gray-600 dark:text-gray-400">
                   {formatDate(project.date)}
                 </span>
               </div>
               {project.github_stars > 0 && (
                 <div className="flex items-center space-x-2">
                   <Star className="w-4 h-4 text-sundai-600 fill-current" />
                   <span className="text-sm text-gray-600 dark:text-gray-400">
                     {project.github_stars} stars
                   </span>
                 </div>
               )}
               {project.contributors && (
                 <div className="flex items-center space-x-2">
                   <Users className="w-4 h-4 text-gray-500" />
                   <span className="text-sm text-gray-600 dark:text-gray-400">
                     {project.contributors.split('|').length} contributors
                   </span>
                 </div>
               )}
               {project.repo_license && (
                 <div className="flex items-center space-x-2">
                   <Shield className="w-4 h-4 text-gray-500" />
                   <span className="text-sm text-gray-600 dark:text-gray-400">
                     {project.repo_license}
                   </span>
                 </div>
               )}
             </div>

            {/* Tabs */}
            <div className="flex border-b border-white/20">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                                         className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-colors ${
                       activeTab === tab.id
                         ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
                         : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                     }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </div>

            {/* Content */}
            <div className="p-6 max-h-[60vh] overflow-y-auto">
              {activeTab === 'overview' && (
                <div className="space-y-6">
                  <div>
                                         <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                       Detailed Description
                     </h3>
                     <div className="prose prose-sm max-w-none text-gray-700 dark:text-gray-300">
                       {project.detailed_description ? (
                         <div dangerouslySetInnerHTML={{ __html: project.detailed_description }} />
                       ) : (
                         <p className="text-gray-500 dark:text-gray-400 italic">
                           No detailed description available.
                         </p>
                       )}
                     </div>
                  </div>

                  {project.ai_summary && (
                    <div>
                                           <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                       AI Summary
                     </h3>
                     <p className="text-gray-700 dark:text-gray-300">
                       {project.ai_summary}
                     </p>
                    </div>
                  )}

                  {getFeatures().length > 0 && (
                    <div>
                                           <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                       Key Features
                     </h3>
                     <ul className="space-y-2">
                       {getFeatures().map((feature, index) => (
                         <li key={index} className="flex items-start space-x-2">
                           <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0" />
                           <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                         </li>
                       ))}
                     </ul>
                    </div>
                  )}

                  {project.architecture && (
                    <div>
                      <h3 className="text-lg font-semibold text-dark-900 dark:text-white mb-3">
                        Architecture
                      </h3>
                      <p className="text-dark-700 dark:text-dark-300">
                        {project.architecture}
                      </p>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'technology' && (
                <div className="space-y-6">
                                     {getTechnologies().length > 0 && (
                     <div>
                       <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                         Technologies
                       </h3>
                      <div className="flex flex-wrap gap-2">
                        {getTechnologies().map((tech, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm rounded-full"
                          >
                            {tech.trim()}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                                     {getFrameworks().length > 0 && (
                     <div>
                       <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                         Frameworks & Libraries
                       </h3>
                      <div className="flex flex-wrap gap-2">
                        {getFrameworks().map((framework, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-sundai-100 dark:bg-sundai-900/30 text-sundai-700 dark:text-sundai-300 text-sm rounded-full"
                          >
                            {framework.trim()}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                                     {getAIModels().length > 0 && (
                     <div>
                       <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                         AI Models & Tools
                       </h3>
                      <div className="flex flex-wrap gap-2">
                        {getAIModels().map((model, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-sm rounded-full"
                          >
                            {model.trim()}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                                     {project.dependencies_list && (
                     <div>
                       <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                         Dependencies
                       </h3>
                       <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
                         <pre className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                           {project.dependencies_list}
                         </pre>
                       </div>
                     </div>
                   )}

                   {project.setup_steps && (
                     <div>
                       <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                         Setup Instructions
                       </h3>
                       <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
                         <pre className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                           {project.setup_steps}
                         </pre>
                       </div>
                     </div>
                   )}
                </div>
              )}

                               {activeTab === 'engagement' && (
                   <div className="space-y-6">
                     {project.integration_plan && (
                       <div>
                         <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                           Integration Strategy
                         </h3>
                         <p className="text-gray-700 dark:text-gray-300">
                           {project.integration_plan}
                         </p>
                       </div>
                     )}

                     {project.deployment_notes && (
                       <div>
                         <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                           Deployment Notes
                         </h3>
                         <p className="text-gray-700 dark:text-gray-300">
                           {project.deployment_notes}
                         </p>
                       </div>
                     )}

                     {getRisks().length > 0 && (
                       <div>
                         <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center space-x-2">
                           <AlertTriangle className="w-5 h-5 text-red-500" />
                           <span>Top Risks & Considerations</span>
                         </h3>
                         <ul className="space-y-2">
                           {getRisks().map((risk, index) => (
                             <li key={index} className="flex items-start space-x-2">
                               <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0" />
                               <span className="text-gray-700 dark:text-gray-300">{risk}</span>
                             </li>
                           ))}
                         </ul>
                       </div>
                     )}

                     {project.security_notes && (
                       <div>
                         <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                           Security Considerations
                         </h3>
                         <p className="text-gray-700 dark:text-gray-300">
                           {project.security_notes}
                         </p>
                       </div>
                     )}

                     {project.testing_notes && (
                       <div>
                         <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                           Testing Strategy
                         </h3>
                         <p className="text-gray-700 dark:text-gray-300">
                           {project.testing_notes}
                         </p>
                       </div>
                     )}
                   </div>
                 )}
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between p-6 border-t border-white/20 bg-white/5">
                             <div className="flex items-center space-x-4">
                 {project.github_url && (
                   <a
                     href={project.github_url}
                     target="_blank"
                     rel="noopener noreferrer"
                     className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                   >
                     <Github className="w-4 h-4" />
                     <span className="text-sm">View on GitHub</span>
                   </a>
                 )}
                 {project.demo_url && (
                   <a
                     href={project.demo_url}
                     target="_blank"
                     rel="noopener noreferrer"
                     className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                   >
                     <ExternalLink className="w-4 h-4" />
                     <span className="text-sm">Live Demo</span>
                   </a>
                 )}
               </div>
              <button
                onClick={onClose}
                className="btn-secondary"
              >
                Close
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default ProjectModal
