import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Star,
  Lightbulb,
  Target,
  Sparkles
} from 'lucide-react'
import { Project, IdeaAnalysis, ProjectMatch } from '@/utils/dataLoader'

interface ThreeDIdeaVisualizerProps {
  ideaAnalysis: IdeaAnalysis | null
  projectMatches: ProjectMatch[]
  onNodeClick: (node: any) => void
}

const ThreeDIdeaVisualizer = ({ 
  ideaAnalysis, 
  projectMatches, 
  onNodeClick 
}: ThreeDIdeaVisualizerProps) => {
  const [rotation, setRotation] = useState({ x: 0, y: 0 })
  const [selectedNode, setSelectedNode] = useState<string | null>(null)

  const handleNodeClick = (node: any) => {
    setSelectedNode(node.id)
    onNodeClick(node)
  }

  const nodes = [
    // Center idea node
    {
      id: 'idea',
      type: 'idea',
      name: 'Your Idea',
      category: ideaAnalysis?.category || 'AI Project',
      position: { x: 0, y: 0, z: 0 },
      color: '#3B82F6',
      icon: Lightbulb,
      data: ideaAnalysis
    },
    // Project nodes around the center
    ...projectMatches.slice(0, 6).map((match, index) => ({
      id: `project-${index}`,
      type: 'project',
      name: match.project.name,
      position: {
        x: Math.cos(index * Math.PI / 3) * 200,
        y: Math.sin(index * Math.PI / 3) * 200,
        z: 0
      },
      color: `hsl(${index * 60}, 70%, 60%)`,
      icon: Target,
      data: match.project,
      similarity: match.similarityScore
    }))
  ]

  return (
    <div className="relative w-full h-96 bg-gradient-to-br from-dark-800 to-dark-900 rounded-2xl overflow-hidden">
      {/* 3D Container */}
      <div 
        className="relative w-full h-full"
        style={{
          perspective: '1000px',
          transformStyle: 'preserve-3d'
        }}
      >
        <motion.div
          className="absolute inset-0"
          animate={{
            rotateX: rotation.x,
            rotateY: rotation.y
          }}
          transition={{ type: "spring", stiffness: 100, damping: 20 }}
          style={{
            transformStyle: 'preserve-3d'
          }}
        >
          {/* Connection Lines */}
          <svg className="absolute inset-0 w-full h-full" style={{ transform: 'translateZ(-100px)' }}>
            {nodes.slice(1).map((node, index) => (
              <line
                key={`connection-${index}`}
                x1="50%"
                y1="50%"
                x2={`${50 + (node.position.x / 400) * 50}%`}
                y2={`${50 + (node.position.y / 400) * 50}%`}
                stroke="#3B82F6"
                strokeWidth="2"
                strokeDasharray="5,5"
                opacity="0.6"
              />
            ))}
          </svg>

          {/* Nodes */}
          {nodes.map((node, index) => {
            const Icon = node.icon
            const isSelected = selectedNode === node.id
            const isIdea = node.type === 'idea'
            
            return (
              <motion.div
                key={node.id}
                className={`absolute cursor-pointer group ${
                  isIdea ? 'z-20' : 'z-10'
                }`}
                style={{
                  left: `${50 + (node.position.x / 400) * 50}%`,
                  top: `${50 + (node.position.y / 400) * 50}%`,
                  transform: `translate(-50%, -50%) translateZ(${isIdea ? '50px' : '0px'})`
                }}
                whileHover={{ scale: 1.1, z: 100 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleNodeClick(node)}
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                {/* Node Circle */}
                <div
                  className={`w-16 h-16 rounded-full flex items-center justify-center shadow-lg transition-all duration-300 ${
                    isSelected 
                      ? 'ring-4 ring-primary-400 ring-offset-2 ring-offset-dark-800' 
                      : 'ring-2 ring-white/20'
                  }`}
                  style={{
                    backgroundColor: node.color,
                    boxShadow: isSelected 
                      ? `0 0 30px ${node.color}80` 
                      : `0 4px 20px ${node.color}40`
                  }}
                >
                  <Icon className="w-6 h-6 text-white" />
                </div>

                {/* Node Label */}
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2">
                  <div className="bg-black/90 text-white px-3 py-1 rounded-lg text-sm font-medium whitespace-nowrap">
                    {isIdea ? '💡 Your Idea' : node.name}
                  </div>
                  {!isIdea && (
                    <div className="text-center mt-1">
                      <span className="text-xs text-primary-400 font-bold">
                        {node.similarity}% match
                      </span>
                    </div>
                  )}
                </div>

                {/* Hover Info */}
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="bg-dark-700 text-white p-3 rounded-lg shadow-xl max-w-xs">
                    <h4 className="font-semibold text-sm mb-1">{node.name}</h4>
                    {isIdea ? (
                      <p className="text-xs text-gray-300">{node.category}</p>
                    ) : (
                      <p className="text-xs text-gray-300 line-clamp-2">
                        {node.data.description}
                      </p>
                    )}
                  </div>
                </div>
              </motion.div>
            )
          })}
        </motion.div>
      </div>

      {/* Controls */}
      <div className="absolute bottom-4 left-4 flex space-x-2">
        <button
          onClick={() => setRotation(prev => ({ ...prev, y: prev.y - 45 }))}
          className="p-2 bg-white/10 rounded-lg hover:bg-white/20 transition-colors"
        >
          <Sparkles className="w-4 h-4 text-white" />
        </button>
        <button
          onClick={() => setRotation(prev => ({ ...prev, y: prev.y + 45 }))}
          className="p-2 bg-white/10 rounded-lg hover:bg-white/20 transition-colors"
        >
          <Star className="w-4 h-4 text-white" />
        </button>
      </div>

      {/* Legend */}
      <div className="absolute top-4 right-4 bg-black/50 p-3 rounded-lg">
        <h4 className="text-white text-sm font-semibold mb-2">Legend</h4>
        <div className="space-y-1 text-xs">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span className="text-white">Your Idea</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-white">Project Matches</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ThreeDIdeaVisualizer
