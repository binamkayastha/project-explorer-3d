import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { 
  Brain, 
  Search, 
  Database, 
  BarChart3, 
  ArrowRight, 
  Sparkles, 
  Zap, 
  Target,
  Users,
  TrendingUp
} from 'lucide-react'

const Home = () => {
  const features = [
    {
      icon: Search,
      title: 'AI Project Matcher',
      description: 'Find similar projects using advanced AI algorithms',
      color: 'from-blue-500 to-cyan-500',
      path: '/ai-matcher'
    },
    {
      icon: Database,
      title: 'Project Explorer',
      description: 'Browse and analyze 300+ AI projects',
      color: 'from-purple-500 to-pink-500',
      path: '/explorer'
    },
    {
      icon: BarChart3,
      title: 'Analytics Dashboard',
      description: 'Get insights into project trends and technologies',
      color: 'from-green-500 to-emerald-500',
      path: '/analytics'
    }
  ]

  const stats = [
    { label: 'Projects Analyzed', value: '300+', icon: Database },
    { label: 'AI Models', value: '50+', icon: Brain },
    { label: 'Technologies', value: '100+', icon: Zap },
    { label: 'Active Users', value: '10K+', icon: Users }
  ]

  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center py-20"
      >
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-primary-500/10 border border-primary-500/20 mb-8"
        >
          <Sparkles className="w-4 h-4 text-primary-500" />
          <span className="text-sm font-medium text-primary-600 dark:text-primary-400">
            Award-Winning AI Platform
          </span>
        </motion.div>

        <h1 className="text-6xl md:text-7xl font-bold mb-6">
          <span className="gradient-text">Discover</span>
          <br />
          <span className="text-dark-900 dark:text-white">AI Projects</span>
        </h1>

        <p className="text-xl text-dark-600 dark:text-dark-300 max-w-3xl mx-auto mb-12 leading-relaxed">
          Explore the world's most innovative AI projects. Find similar ideas, analyze technology stacks, 
          and build your next breakthrough with our award-winning platform.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/ai-matcher">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-primary flex items-center space-x-2"
            >
              <Search className="w-5 h-5" />
              <span>Start Exploring</span>
              <ArrowRight className="w-5 h-5" />
            </motion.button>
          </Link>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="btn-secondary flex items-center space-x-2"
          >
            <Target className="w-5 h-5" />
            <span>Watch Demo</span>
          </motion.button>
        </div>
      </motion.section>

      {/* Stats Section */}
      <motion.section
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.4 }}
        className="py-16"
      >
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
                className="text-center"
              >
                <div className="glass-card p-6 card-hover">
                  <Icon className="w-8 h-8 text-primary-500 mx-auto mb-4" />
                  <div className="text-3xl font-bold gradient-text mb-2">{stat.value}</div>
                  <div className="text-sm text-dark-600 dark:text-dark-400">{stat.label}</div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.section>

      {/* Features Section */}
      <motion.section
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.6 }}
        className="py-20"
      >
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">
            <span className="gradient-text">Powerful Features</span>
          </h2>
          <p className="text-xl text-dark-600 dark:text-dark-300 max-w-2xl mx-auto">
            Everything you need to discover, analyze, and build with AI projects
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <Link key={feature.title} to={feature.path}>
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.8 + index * 0.1 }}
                  whileHover={{ y: -10 }}
                  className="glass-card p-8 card-hover group"
                >
                  <div className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-dark-900 dark:text-white">
                    {feature.title}
                  </h3>
                  <p className="text-dark-600 dark:text-dark-300 leading-relaxed">
                    {feature.description}
                  </p>
                  <div className="flex items-center mt-6 text-primary-600 dark:text-primary-400 font-medium">
                    <span>Learn more</span>
                    <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                  </div>
                </motion.div>
              </Link>
            )
          })}
        </div>
      </motion.section>

      {/* CTA Section */}
      <motion.section
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 1 }}
        className="py-20 text-center"
      >
        <div className="gradient-border">
          <div className="glass-card p-12">
            <h2 className="text-4xl font-bold mb-6">
              Ready to <span className="gradient-text">Build</span> Something Amazing?
            </h2>
            <p className="text-xl text-dark-600 dark:text-dark-300 mb-8 max-w-2xl mx-auto">
              Join thousands of developers and entrepreneurs who are already using our platform 
              to discover and build the next generation of AI applications.
            </p>
            <Link to="/ai-matcher">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-primary text-lg px-8 py-4"
              >
                Get Started Now
              </motion.button>
            </Link>
          </div>
        </div>
      </motion.section>
    </div>
  )
}

export default Home
