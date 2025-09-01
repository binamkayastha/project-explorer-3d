import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  BarChart3, 
  Sparkles, 
  TrendingUp, 
  Database, 
  Star, 
  Users, 
  Zap, 
  Target,
  AlertTriangle,
  CheckCircle,
  ArrowUp,
  ArrowDown,
  Calendar,
  Globe,
  Code,
  Server,
  Brain,
  Cloud
} from 'lucide-react'
import { dataLoader, AnalyticsData } from '@/utils/dataLoader'
import { AnalyticsCharts } from '@/components/AnalyticsCharts'
import toast from 'react-hot-toast'

const Analytics = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'overview' | 'trends' | 'insights'>('overview')

  useEffect(() => {
    loadAnalyticsData()
  }, [])

  const loadAnalyticsData = async () => {
    try {
      setIsLoading(true)
      const data = await dataLoader.getAnalyticsData()
      setAnalyticsData(data)
    } catch (error) {
      console.error('Error loading analytics data:', error)
      toast.error('Failed to load analytics data')
    } finally {
      setIsLoading(false)
    }
  }

  const StatCard = ({ 
    title, 
    value, 
    icon: Icon, 
    trend, 
    trendValue, 
    color = 'primary' 
  }: {
    title: string
    value: string | number
    icon: any
    trend?: 'up' | 'down' | 'neutral'
    trendValue?: string
    color?: string
  }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-400">{title}</p>
          <p className="text-2xl font-bold text-white mt-1">{value}</p>
          {trend && (
            <div className="flex items-center space-x-1 mt-2">
              {trend === 'up' && <ArrowUp className="w-4 h-4 text-green-500" />}
              {trend === 'down' && <ArrowDown className="w-4 h-4 text-red-500" />}
              <span className={`text-sm font-medium ${
                trend === 'up' ? 'text-green-500' : 
                trend === 'down' ? 'text-red-500' : 'text-gray-400'
              }`}>
                {trendValue}
              </span>
            </div>
          )}
        </div>
        <div className={`w-12 h-12 rounded-lg bg-${color}-500/20 flex items-center justify-center`}>
          <Icon className={`w-6 h-6 text-${color}-400`} />
        </div>
      </div>
    </motion.div>
  )

  const TechnologyChart = ({ 
    data, 
    title, 
    icon: Icon 
  }: {
    data: { name: string; count: number; percentage: number }[]
    title: string
    icon: any
  }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-6"
    >
      <div className="flex items-center space-x-2 mb-6">
        <Icon className="w-5 h-5 text-primary-400" />
        <h3 className="text-lg font-semibold text-white">{title}</h3>
      </div>
      
      <div className="space-y-4">
        {data.slice(0, 8).map((item, index) => (
          <div key={item.name} className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-300">{item.name}</span>
              <span className="text-sm text-gray-400">{item.count} projects</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-primary-500 to-sundai-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${item.percentage}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-gray-500">
              <span>{item.percentage}% of projects</span>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  )

  const CategoryCard = ({ 
    name, 
    count, 
    percentage 
  }: {
    name: string
    count: number
    percentage: number
  }) => (
    <div className="glass-card p-4">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-semibold text-white">{name}</h4>
        <span className="text-sm text-gray-400">{count} projects</span>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-2 mb-2">
        <div 
          className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-xs text-gray-500">{percentage.toFixed(1)}% of total</span>
    </div>
  )

  const InsightCard = ({ 
    title, 
    items, 
    icon: Icon, 
    type = 'info' 
  }: {
    title: string
    items: string[]
    icon: any
    type?: 'info' | 'success' | 'warning'
  }) => {
    const getTypeStyles = () => {
      switch (type) {
        case 'success': return 'text-green-400 bg-green-500/20'
        case 'warning': return 'text-yellow-400 bg-yellow-500/20'
        default: return 'text-primary-400 bg-primary-500/20'
      }
    }

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center space-x-2 mb-4">
          <div className={`w-8 h-8 rounded-lg ${getTypeStyles()} flex items-center justify-center`}>
            <Icon className="w-4 h-4" />
          </div>
          <h3 className="text-lg font-semibold text-white">{title}</h3>
        </div>
        
        <div className="space-y-3">
          {items.map((item, index) => (
            <div key={index} className="flex items-start space-x-2">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0" />
              <span className="text-gray-300 text-sm">{item}</span>
            </div>
          ))}
        </div>
      </motion.div>
    )
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading analytics data...</p>
        </div>
      </div>
    )
  }

  if (!analyticsData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-gray-400">Failed to load analytics data</p>
        </div>
      </div>
    )
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
                <BarChart3 className="w-8 h-8 text-primary-400" />
                <h1 className="text-4xl font-bold gradient-text">
                  Analytics Dashboard
                </h1>
              </div>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Deep insights into AI project trends, technology adoption patterns, 
                and market opportunities based on our comprehensive dataset.
              </p>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Navigation Tabs */}
          <div className="flex border-b border-white/20 mb-8">
            <button
              onClick={() => setActiveTab('overview')}
              className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'overview'
                  ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              <span>Overview</span>
            </button>
            <button
              onClick={() => setActiveTab('trends')}
              className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'trends'
                  ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              <TrendingUp className="w-4 h-4" />
              <span>Technology Trends</span>
            </button>
            <button
              onClick={() => setActiveTab('insights')}
              className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'insights'
                  ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              <Target className="w-4 h-4" />
              <span>Market Insights</span>
            </button>
          </div>

          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              {/* Key Stats */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                  title="Total Projects"
                  value={analyticsData.projectStats.totalProjects}
                  icon={Database}
                  trend="up"
                  trendValue="+12% this month"
                  color="primary"
                />
                <StatCard
                  title="Total Stars"
                  value={analyticsData.projectStats.totalStars.toLocaleString()}
                  icon={Star}
                  trend="up"
                  trendValue="+8% this month"
                  color="sundai"
                />
                <StatCard
                  title="Average Stars"
                  value={analyticsData.projectStats.avgStars}
                  icon={Users}
                  trend="neutral"
                  color="green"
                />
                <StatCard
                  title="Recent Projects"
                  value={analyticsData.projectStats.recentProjects}
                  icon={Calendar}
                  trend="up"
                  trendValue="+15% this month"
                  color="purple"
                />
              </div>

              {/* Top Categories */}
              <div>
                <h2 className="text-2xl font-bold text-white mb-6">Project Categories</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {analyticsData.projectStats.topCategories.map((category, index) => (
                    <CategoryCard
                      key={category.name}
                      name={category.name}
                      count={category.count}
                      percentage={(category.count / analyticsData.projectStats.totalProjects) * 100}
                    />
                  ))}
                </div>
              </div>

              {/* Quick Insights */}
              <div>
                <h2 className="text-2xl font-bold text-white mb-6">Quick Insights</h2>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <InsightCard
                    title="Trending Technologies"
                    items={analyticsData.marketInsights.trendingTechnologies}
                    icon={Zap}
                    type="success"
                  />
                  <InsightCard
                    title="Emerging Categories"
                    items={analyticsData.marketInsights.emergingCategories}
                    icon={TrendingUp}
                    type="info"
                  />
                </div>
              </div>
            </motion.div>
          )}

          {/* Trends Tab */}
          {activeTab === 'trends' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              <AnalyticsCharts
                frameworks={analyticsData.technologyTrends.frameworks}
                aiModels={analyticsData.technologyTrends.aiModels}
                vectorDBs={analyticsData.technologyTrends.vectorDBs}
                infrastructure={analyticsData.technologyTrends.infrastructure}
              />
            </motion.div>
          )}

          {/* Insights Tab */}
          {activeTab === 'insights' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <InsightCard
                  title="Market Gaps"
                  items={analyticsData.marketInsights.gaps}
                  icon={AlertTriangle}
                  type="warning"
                />
                <InsightCard
                  title="Market Opportunities"
                  items={analyticsData.marketInsights.opportunities}
                  icon={CheckCircle}
                  type="success"
                />
              </div>

              {/* Technology Adoption Insights */}
              <div className="glass-card p-6">
                <h3 className="text-xl font-bold text-white mb-6">Technology Adoption Insights</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {analyticsData.technologyTrends.frameworks.slice(0, 4).map((framework) => (
                    <div key={framework.name} className="text-center p-4 bg-white/5 rounded-lg">
                      <h4 className="font-semibold text-white mb-2">{framework.name}</h4>
                      <div className="text-2xl font-bold text-primary-400 mb-1">{framework.percentage}%</div>
                      <div className="text-sm text-gray-400">{framework.count} projects</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div className="glass-card p-6">
                <h3 className="text-xl font-bold text-white mb-6">Strategic Recommendations</h3>
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 rounded-full bg-primary-500/20 flex items-center justify-center flex-shrink-0">
                      <span className="text-primary-400 font-bold">1</span>
                    </div>
                    <div>
                      <h4 className="font-semibold text-white mb-1">Focus on AI/ML Integration</h4>
                      <p className="text-gray-300 text-sm">
                        With {analyticsData.technologyTrends.aiModels[0]?.percentage}% of projects using AI models, 
                        integrating AI capabilities can significantly increase project adoption.
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 rounded-full bg-sundai-500/20 flex items-center justify-center flex-shrink-0">
                      <span className="text-sundai-400 font-bold">2</span>
                    </div>
                    <div>
                      <h4 className="font-semibold text-white mb-1">Leverage Modern Frameworks</h4>
                      <p className="text-gray-300 text-sm">
                        {analyticsData.technologyTrends.frameworks[0]?.name} leads with {analyticsData.technologyTrends.frameworks[0]?.percentage}% adoption. 
                        Consider building on established, well-supported frameworks.
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center flex-shrink-0">
                      <span className="text-green-400 font-bold">3</span>
                    </div>
                    <div>
                      <h4 className="font-semibold text-white mb-1">Address Market Gaps</h4>
                      <p className="text-gray-300 text-sm">
                        {analyticsData.marketInsights.gaps.length} identified market gaps present opportunities 
                        for innovative solutions that combine multiple technologies.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Analytics
