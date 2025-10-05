import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X, Search, Brain, Database, BarChart3, Sun, Moon, Sparkles } from 'lucide-react'
import { useTheme } from '@/contexts/ThemeContext'

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const location = useLocation()
  const { theme, toggleTheme } = useTheme()

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const navItems = [
    { path: '/', label: 'Home', icon: Brain },
    { path: '/ai-matcher', label: 'AI Matcher', icon: Search },
    { path: '/explorer', label: 'Explorer', icon: Database },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
  ]

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled 
          ? 'glass-card-dark shadow-lg' 
          : 'bg-transparent'
      }`}
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-3 group" aria-label="Sundai AI Explorer home">
            <motion.div
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.6 }}
              className="relative"
            >
              <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-sundai-500 rounded-xl flex items-center justify-center glow-effect">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute -top-1 -right-1 w-4 h-4 bg-sundai-400 rounded-full"
              >
                <Sparkles className="w-3 h-3 text-white" />
              </motion.div>
            </motion.div>
            <div>
              <span className="text-xl font-bold gradient-text">Sundai AI</span>
              <div className="text-xs text-dark-500 dark:text-dark-400">Explorer</div>
            </div>
          </Link>

          <div className="hidden md:flex items-center space-x-1" role="navigation" aria-label="Main">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`relative flex items-center space-x-2 px-4 py-2 rounded-xl transition-all duration-300 group ${
                    isActive
                      ? 'bg-primary-600 text-white shadow-md dark:bg-primary-500/80'
                      : 'text-dark-800 hover:text-primary-700 dark:text-dark-50 dark:hover:text-primary-300'
                  }`}
                  aria-current={isActive ? 'page' : undefined}
                >
                  <Icon className="w-4 h-4" />
                  <span className="font-medium">{item.label}</span>
                  {isActive && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute inset-0 rounded-xl bg-primary-600/40 dark:bg-primary-500/40"
                      initial={false}
                      transition={{ type: "spring", stiffness: 500, damping: 30 }}
                    />
                  )}
                </Link>
              )
            })}
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-xl bg-white text-dark-900 border border-white/40 hover:bg-primary-50 transition-all duration-300 dark:bg-dark-700 dark:text-white dark:border-dark-500"
              aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
            >
              {theme === 'light' ? (
                <Moon className="w-5 h-5 text-dark-700" />
              ) : (
                <Sun className="w-5 h-5 text-amber-300" />
              )}
            </button>

            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 rounded-xl bg-white text-dark-900 border border-white/40 hover:bg-primary-50 transition-all duration-300 dark:bg-dark-700 dark:text-white dark:border-dark-500"
              aria-expanded={isOpen}
              aria-controls="mobile-nav"
              aria-label="Toggle navigation menu"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden py-4 space-y-2"
              id="mobile-nav"
            >
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setIsOpen(false)}
                    className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                      location.pathname === item.path
                        ? 'bg-primary-600 text-white shadow-md'
                        : 'text-dark-900 hover:bg-dark-50 dark:text-dark-50 dark:hover:bg-dark-700'
                    }`}
                    aria-current={location.pathname === item.path ? 'page' : undefined}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                )
              })}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.nav>
  )
}

export default Navbar
