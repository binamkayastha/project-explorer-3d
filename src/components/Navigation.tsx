import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Cube, BarChart3 } from 'lucide-react';

const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
      <div className="glass-panel px-4 py-2 rounded-full flex items-center gap-2">
        <Link to="/">
          <Button
            variant={location.pathname === '/' ? 'default' : 'ghost'}
            size="sm"
            className={`flex items-center gap-2 ${
              location.pathname === '/' 
                ? 'bg-cosmic-aurora text-black hover:bg-cosmic-aurora/90' 
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <Cube className="w-4 h-4" />
            3D Viewer
          </Button>
        </Link>
        
        <div className="w-px h-6 bg-border" />
        
        <Link to="/streamlit">
          <Button
            variant={location.pathname === '/streamlit' ? 'default' : 'ghost'}
            size="sm"
            className={`flex items-center gap-2 ${
              location.pathname === '/streamlit' 
                ? 'bg-cosmic-plasma text-white hover:bg-cosmic-plasma/90' 
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            Analytics
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default Navigation;
