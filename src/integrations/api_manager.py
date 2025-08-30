"""
Unified API Manager for Public APIs
Combines multiple public APIs to provide comprehensive startup and company data
"""

import sys
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

# Add the integrations directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from .public_apis import PublicAPIManager
except ImportError:
    # Fallback for direct import
    from public_apis import PublicAPIManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StartupDataManager:
    """
    Unified manager for public APIs that don't require registration
    Provides comprehensive startup and company data
    """
    
    def __init__(self):
        """
        Initialize the startup data manager
        """
        self.public_api = PublicAPIManager()
        
        # Cache for storing results
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour cache
        
    def search_startups(self, query: str, limit: int = 20, sources: List[str] = None) -> List[Dict]:
        """
        Search for startups across multiple public platforms
        
        Args:
            query (str): Search query
            limit (int): Number of results per source
            sources (List[str]): List of sources to search ('github', 'npm', 'pypi')
            
        Returns:
            List[Dict]: Combined startup data
        """
        if sources is None:
            sources = ['github', 'npm', 'pypi']
        
        all_startups = []
        
        if 'github' in sources:
            try:
                companies = self.public_api.search_companies_github(query, limit)
                all_startups.extend(companies)
            except Exception as e:
                logger.error(f"Error searching GitHub: {str(e)}")
        
        if 'npm' in sources:
            try:
                startups = self.public_api.search_companies_npm(query, limit)
                all_startups.extend(startups)
            except Exception as e:
                logger.error(f"Error searching NPM: {str(e)}")
        
        if 'pypi' in sources:
            try:
                pypi_projects = self.public_api.search_companies_pypi(query, limit)
                all_startups.extend(pypi_projects)
            except Exception as e:
                logger.error(f"Error searching PyPI: {str(e)}")
        
        # Remove duplicates based on name and source
        unique_startups = {}
        for startup in all_startups:
            key = f"{startup['name']}_{startup['source']}"
            if key not in unique_startups:
                unique_startups[key] = startup
        
        return list(unique_startups.values())
    
    def get_trending_startups(self, category: str = None, limit: int = 20) -> List[Dict]:
        """
        Get trending startups from multiple platforms
        
        Args:
            category (str): Optional category filter
            limit (int): Number of results to return
            
        Returns:
            List[Dict]: Trending startups data
        """
        try:
            trending = self.public_api.get_trending_projects(category, limit)
            return trending
        except Exception as e:
            logger.error(f"Error getting trending startups: {str(e)}")
            return []
    
    def get_startup_details(self, startup_id: str, source: str) -> Optional[Dict]:
        """
        Get detailed startup information
        
        Args:
            startup_id (str): Startup ID
            source (str): Source platform ('github', 'npm', 'pypi')
            
        Returns:
            Optional[Dict]: Detailed startup information
        """
        try:
            # For public APIs, we'll return the basic info we have
            # In a real implementation, you might make additional API calls
            if source == 'github':
                # Try to get more details from GitHub
                details = self.public_api.search_companies_github(startup_id, 1)
                if details:
                    return details[0]
            
            elif source == 'npm':
                # Try to get more details from NPM
                details = self.public_api.search_companies_npm(startup_id, 1)
                if details:
                    return details[0]
            
            elif source == 'pypi':
                # Try to get more details from PyPI
                details = self.public_api.search_companies_pypi(startup_id, 1)
                if details:
                    return details[0]
        
        except Exception as e:
            logger.error(f"Error getting startup details: {str(e)}")
        
        return None
    
    def get_funding_rounds(self, startup_id: str, source: str) -> List[Dict]:
        """
        Get funding rounds for a startup (not available in public APIs)
        
        Args:
            startup_id (str): Startup ID
            source (str): Source platform
            
        Returns:
            List[Dict]: List of funding rounds (empty for public APIs)
        """
        # Public APIs don't provide funding information
        return []
    
    def get_team_members(self, startup_id: str, source: str) -> List[Dict]:
        """
        Get team members for a startup (limited in public APIs)
        
        Args:
            startup_id (str): Startup ID
            source (str): Source platform
            
        Returns:
            List[Dict]: List of team members
        """
        try:
            if source == 'github':
                # For GitHub, we can get owner information
                details = self.public_api.search_companies_github(startup_id, 1)
                if details:
                    owner = details[0].get('owner', {})
                    return [{
                        'id': owner.get('id', ''),
                        'name': owner.get('login', ''),
                        'title': 'Owner',
                        'avatar_url': owner.get('avatar_url', ''),
                        'source': 'github'
                    }]
        except Exception as e:
            logger.error(f"Error getting team members: {str(e)}")
        
        return []
    
    def get_markets_and_categories(self) -> Dict[str, List[Dict]]:
        """
        Get available markets and categories from public platforms
        
        Returns:
            Dict[str, List[Dict]]: Markets and categories data
        """
        markets = {}
        
        # GitHub categories (programming languages)
        github_categories = [
            {'id': 'python', 'name': 'Python', 'source': 'github'},
            {'id': 'javascript', 'name': 'JavaScript', 'source': 'github'},
            {'id': 'java', 'name': 'Java', 'source': 'github'},
            {'id': 'typescript', 'name': 'TypeScript', 'source': 'github'},
            {'id': 'go', 'name': 'Go', 'source': 'github'},
            {'id': 'rust', 'name': 'Rust', 'source': 'github'},
            {'id': 'cpp', 'name': 'C++', 'source': 'github'},
            {'id': 'csharp', 'name': 'C#', 'source': 'github'}
        ]
        markets['github'] = github_categories
        
        # NPM categories (package types)
        npm_categories = [
            {'id': 'framework', 'name': 'Framework', 'source': 'npm'},
            {'id': 'utility', 'name': 'Utility', 'source': 'npm'},
            {'id': 'ui', 'name': 'UI Component', 'source': 'npm'},
            {'id': 'api', 'name': 'API Client', 'source': 'npm'},
            {'id': 'testing', 'name': 'Testing', 'source': 'npm'},
            {'id': 'build', 'name': 'Build Tool', 'source': 'npm'}
        ]
        markets['npm'] = npm_categories
        
        # PyPI categories (Python package types)
        pypi_categories = [
            {'id': 'data-science', 'name': 'Data Science', 'source': 'pypi'},
            {'id': 'web-framework', 'name': 'Web Framework', 'source': 'pypi'},
            {'id': 'machine-learning', 'name': 'Machine Learning', 'source': 'pypi'},
            {'id': 'utility', 'name': 'Utility', 'source': 'pypi'},
            {'id': 'api', 'name': 'API Client', 'source': 'pypi'},
            {'id': 'testing', 'name': 'Testing', 'source': 'pypi'}
        ]
        markets['pypi'] = pypi_categories
        
        return markets
    
    def get_api_usage_stats(self) -> Dict[str, Dict]:
        """
        Get API usage statistics for all platforms
        
        Returns:
            Dict[str, Dict]: Usage statistics for each platform
        """
        public_usage = self.public_api.get_api_usage_stats()
        
        return {
            'public_apis': public_usage,
            'total_requests': public_usage['requests_made'],
            'total_remaining': public_usage['remaining_requests']
        }
    
    def reset_usage_counters(self):
        """Reset usage counters for all APIs"""
        self.public_api.reset_usage_counter()
    
    def get_combined_insights(self, query: str) -> Dict[str, Any]:
        """
        Get comprehensive insights by combining data from all platforms
        
        Args:
            query (str): Search query
            
        Returns:
            Dict[str, Any]: Combined insights and analytics
        """
        try:
            insights = self.public_api.get_market_insights(query)
            
            # Add additional analysis
            projects = insights.get('projects', [])
            
            # Analyze popularity metrics
            total_stars = insights.get('total_stars', 0)
            total_downloads = insights.get('total_downloads', 0)
            
            # Calculate average metrics
            avg_stars = total_stars / len(projects) if projects else 0
            avg_downloads = total_downloads / len(projects) if projects else 0
            
            # Add calculated insights
            insights.update({
                'average_stars': avg_stars,
                'average_downloads': avg_downloads,
                'popularity_score': (total_stars + total_downloads) / 1000,  # Normalized score
                'platform_diversity': len(insights.get('source_distribution', {})),
                'language_diversity': len(insights.get('language_distribution', {}))
            })
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting combined insights: {str(e)}")
            return {
                'total_projects_found': 0,
                'total_stars': 0,
                'total_downloads': 0,
                'source_distribution': {},
                'language_distribution': {},
                'search_query': query,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }


# Example usage and testing
if __name__ == "__main__":
    # Initialize the manager
    manager = StartupDataManager()
    
    # Search for startups
    startups = manager.search_startups("AI", limit=10)
    print(f"Found {len(startups)} startups")
    
    # Get trending startups
    trending = manager.get_trending_startups(limit=5)
    print(f"Found {len(trending)} trending startups")
    
    # Get combined insights
    insights = manager.get_combined_insights("AI")
    print(f"Insights: {insights}")
    
    # Get API usage stats
    usage = manager.get_api_usage_stats()
    print(f"API Usage: {usage}")

