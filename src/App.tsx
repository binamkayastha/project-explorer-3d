import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { useLocation } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import AIProjectMatcher from './pages/AIProjectMatcher'
import ProjectExplorer from './pages/ProjectExplorer'
import Analytics from './pages/Analytics'
import { ThemeProvider } from './contexts/ThemeContext'

function App() {
  const location = useLocation()

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-dark-900 dark:via-dark-800 dark:to-dark-900">
        <Navbar />
        <AnimatePresence mode="wait">
          <motion.main
            key={location.pathname}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="container mx-auto px-4 py-8"
          >
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/ai-matcher" element={<AIProjectMatcher />} />
              <Route path="/explorer" element={<ProjectExplorer />} />
              <Route path="/analytics" element={<Analytics />} />
            </Routes>
          </motion.main>
        </AnimatePresence>
        <Footer />
      </div>
    </ThemeProvider>
  )
}

export default App
