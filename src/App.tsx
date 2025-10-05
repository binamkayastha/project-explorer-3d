import { useEffect, useRef } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import AIProjectMatcher from "./pages/AIProjectMatcher";
import ProjectExplorer from "./pages/ProjectExplorer";
import Analytics from "./pages/Analytics";
import { ThemeProvider } from "./contexts/ThemeContext";

function App() {
  const location = useLocation();
  const mainRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (mainRef.current) {
      mainRef.current.focus();
    }
  }, [location.pathname]);

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-dark-900 dark:via-dark-800 dark:to-dark-900">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:bg-white focus:text-dark-900 dark:focus:bg-dark-800 dark:focus:text-white px-4 py-2 rounded"
        >
          Skip to main content
        </a>
        <Navbar />
        <AnimatePresence mode="wait">
          <motion.main
            key={location.pathname}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="container mx-auto px-4 pt-16 pb-12"
            id="main-content"
            tabIndex={-1}
            ref={mainRef}
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
  );
}

export default App;
