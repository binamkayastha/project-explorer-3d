import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Brain, Github, Twitter, Linkedin, Mail, Heart } from 'lucide-react'

const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="mt-20 border-t border-white/10">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-sundai-500 rounded-xl flex items-center justify-center">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <span className="text-xl font-bold gradient-text">Sundai AI</span>
                <div className="text-sm text-dark-500 dark:text-dark-400">Explorer</div>
              </div>
            </Link>
            <p className="text-dark-600 dark:text-dark-300 mb-6 max-w-md">
              Discover the world's most innovative AI projects. Find similar ideas, analyze technology stacks, 
              and build your next breakthrough with our award-winning platform.
            </p>
            <div className="flex space-x-4">
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-lg bg-white text-dark-700 border border-white/60 hover:bg-primary-50 hover:text-primary-700 transition-all duration-300 dark:bg-dark-700 dark:text-white dark:border-dark-500 dark:hover:bg-dark-600"
              >
                <Github className="w-5 h-5" />
              </motion.a>
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-lg bg-white text-dark-700 border border-white/60 hover:bg-primary-50 hover:text-primary-700 transition-all duration-300 dark:bg-dark-700 dark:text-white dark:border-dark-500 dark:hover:bg-dark-600"
              >
                <Twitter className="w-5 h-5" />
              </motion.a>
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-lg bg-white text-dark-700 border border-white/60 hover:bg-primary-50 hover:text-primary-700 transition-all duration-300 dark:bg-dark-700 dark:text-white dark:border-dark-500 dark:hover:bg-dark-600"
              >
                <Linkedin className="w-5 h-5" />
              </motion.a>
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-lg bg-white text-dark-700 border border-white/60 hover:bg-primary-50 hover:text-primary-700 transition-all duration-300 dark:bg-dark-700 dark:text-white dark:border-dark-500 dark:hover:bg-dark-600"
              >
                <Mail className="w-5 h-5" />
              </motion.a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-dark-900 dark:text-white">Quick Links</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/" className="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/ai-matcher" className="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                  AI Matcher
                </Link>
              </li>
              <li>
                <Link to="/explorer" className="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                  Project Explorer
                </Link>
              </li>
              <li>
                <Link to="/analytics" className="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                  Analytics
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-dark-900 dark:text-white">Support</h3>
            <ul className="space-y-3">
              <li>
                <a href="#" className="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" className="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                  API Reference
                </a>
              </li>
              <li>
                <a href="#" className="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                  Contact Us
                </a>
              </li>
              <li>
                <a href="#" className="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                  Privacy Policy
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-white/10 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-dark-600 dark:text-dark-300 text-sm">
            © {currentYear} Sundai AI Explorer. All rights reserved.
          </p>
          <div className="flex items-center space-x-2 mt-4 md:mt-0">
            <span className="text-dark-600 dark:text-dark-300 text-sm">Made with</span>
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            >
              <Heart className="w-4 h-4 text-red-500" />
            </motion.div>
            <span className="text-dark-600 dark:text-dark-300 text-sm">for the AI community</span>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
