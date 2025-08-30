#!/usr/bin/env python3
"""
Example Integration for Model Answers
Shows how to use the public APIs in different scenarios for model responses
"""

import sys
import os
from typing import Dict, List, Any

# Add the integrations directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'integrations'))

from src.integrations import StartupDataManager, PublicAPIManager

class ModelAnswerEnhancer:
    """
    Enhances model answers with real-time public API data
    """
    
    def __init__(self):
        """Initialize the enhancer with API managers"""
        self.startup_manager = StartupDataManager()
        self.public_api = PublicAPIManager()
    
    def enhance_technology_trends_answer(self, query: str) -> Dict[str, Any]:
        """
        Enhance a technology trends answer with real data
        
        Args:
            query (str): Technology query (e.g., "AI", "Machine Learning", "React")
            
        Returns:
            Dict[str, Any]: Enhanced answer with real data
        """
        print(f"🔍 Researching trends for: {query}")
        
        # Get real data from multiple sources
        github_projects = self.public_api.search_companies_github(query, limit=10)
        npm_packages = self.public_api.search_companies_npm(query, limit=10)
        pypi_packages = self.public_api.search_companies_pypi(query, limit=10)
        
        # Analyze trends
        total_projects = len(github_projects) + len(npm_packages) + len(pypi_packages)
        total_stars = sum(p.get('stars', 0) for p in github_projects)
        total_downloads = sum(p.get('downloads', 0) for p in npm_packages + pypi_packages)
        
        # Get trending projects
        trending = self.public_api.get_trending_projects(limit=5)
        
        return {
            "query": query,
            "total_projects_found": total_projects,
            "total_stars": total_stars,
            "total_downloads": total_downloads,
            "trending_projects": trending[:3],
            "top_github_projects": github_projects[:3],
            "top_npm_packages": npm_packages[:3],
            "top_pypi_packages": pypi_packages[:3],
            "enhanced_answer": f"""
Based on real-time data analysis, {query} shows strong activity across multiple platforms:

📊 **Activity Overview:**
- Total projects found: {total_projects}
- GitHub stars: {total_stars:,}
- Package downloads: {total_downloads:,}

🔥 **Trending Projects:**
{self._format_trending_projects(trending[:3])}

📈 **Top GitHub Projects:**
{self._format_github_projects(github_projects[:3])}

📦 **Popular Packages:**
{self._format_packages(npm_packages[:3] + pypi_packages[:3])}

This data indicates {query} is {'highly active' if total_projects > 20 else 'moderately active' if total_projects > 10 else 'growing'} in the developer community.
            """
        }
    
    def enhance_startup_research_answer(self, industry: str) -> Dict[str, Any]:
        """
        Enhance startup research with real project data
        
        Args:
            industry (str): Industry focus (e.g., "fintech", "healthtech", "edtech")
            
        Returns:
            Dict[str, Any]: Enhanced startup research
        """
        print(f"🏢 Researching startups in: {industry}")
        
        # Search for industry-related projects
        projects = self.startup_manager.search_startups(industry, limit=15)
        
        # Get market insights
        insights = self.public_api.get_market_insights(industry)
        
        # Analyze by source
        github_count = len([p for p in projects if p.get('source') == 'github'])
        npm_count = len([p for p in projects if p.get('source') == 'npm'])
        pypi_count = len([p for p in projects if p.get('source') == 'pypi'])
        
        return {
            "industry": industry,
            "total_projects": len(projects),
            "github_projects": github_count,
            "npm_packages": npm_count,
            "pypi_packages": pypi_count,
            "market_insights": insights,
            "top_projects": projects[:5],
            "enhanced_answer": f"""
Real-time analysis of {industry} ecosystem:

📈 **Market Activity:**
- Total projects: {len(projects)}
- GitHub repositories: {github_count}
- NPM packages: {npm_count}
- PyPI packages: {pypi_count}

🎯 **Top Projects:**
{self._format_projects(projects[:5])}

📊 **Market Insights:**
- Total stars: {insights.get('total_stars', 0):,}
- Total downloads: {insights.get('total_downloads', 0):,}
- Language distribution: {self._format_language_distribution(insights.get('language_distribution', {}))}

This indicates {industry} is {'a highly active' if len(projects) > 20 else 'a growing' if len(projects) > 10 else 'an emerging'} sector with strong developer interest.
            """
        }
    
    def enhance_technology_comparison_answer(self, tech1: str, tech2: str) -> Dict[str, Any]:
        """
        Compare two technologies with real data
        
        Args:
            tech1 (str): First technology
            tech2 (str): Second technology
            
        Returns:
            Dict[str, Any]: Technology comparison
        """
        print(f"⚖️ Comparing: {tech1} vs {tech2}")
        
        # Get data for both technologies
        tech1_data = self.public_api.get_market_insights(tech1)
        tech2_data = self.public_api.get_market_insights(tech2)
        
        # Compare metrics
        comparison = {
            "tech1": {
                "name": tech1,
                "projects": tech1_data.get('total_projects_found', 0),
                "stars": tech1_data.get('total_stars', 0),
                "downloads": tech1_data.get('total_downloads', 0)
            },
            "tech2": {
                "name": tech2,
                "projects": tech2_data.get('total_projects_found', 0),
                "stars": tech2_data.get('total_stars', 0),
                "downloads": tech2_data.get('total_downloads', 0)
            }
        }
        
        # Determine winner
        tech1_score = comparison["tech1"]["projects"] + comparison["tech1"]["stars"] // 1000
        tech2_score = comparison["tech2"]["projects"] + comparison["tech2"]["stars"] // 1000
        
        winner = tech1 if tech1_score > tech2_score else tech2 if tech2_score > tech1_score else "Tie"
        
        return {
            "comparison": comparison,
            "winner": winner,
            "enhanced_answer": f"""
Real-time comparison of {tech1} vs {tech2}:

📊 **Project Count:**
- {tech1}: {comparison['tech1']['projects']} projects
- {tech2}: {comparison['tech2']['projects']} projects

⭐ **GitHub Stars:**
- {tech1}: {comparison['tech1']['stars']:,} stars
- {tech2}: {comparison['tech2']['stars']:,} stars

📦 **Package Downloads:**
- {tech1}: {comparison['tech1']['downloads']:,} downloads
- {tech2}: {comparison['tech2']['downloads']:,} downloads

🏆 **Overall Winner:** {winner}

Based on current data, {winner} shows {'stronger' if winner != 'Tie' else 'similar'} community engagement and adoption.
            """
        }
    
    def _format_trending_projects(self, projects: List[Dict]) -> str:
        """Format trending projects for display"""
        if not projects:
            return "No trending projects found"
        
        formatted = []
        for i, project in enumerate(projects, 1):
            formatted.append(f"{i}. **{project.get('name', 'Unknown')}** - {project.get('description', '')[:100]}...")
        
        return "\n".join(formatted)
    
    def _format_github_projects(self, projects: List[Dict]) -> str:
        """Format GitHub projects for display"""
        if not projects:
            return "No GitHub projects found"
        
        formatted = []
        for i, project in enumerate(projects, 1):
            stars = project.get('stars', 0)
            language = project.get('language', 'Unknown')
            formatted.append(f"{i}. **{project.get('name', 'Unknown')}** - ⭐ {stars:,} | {language}")
        
        return "\n".join(formatted)
    
    def _format_packages(self, packages: List[Dict]) -> str:
        """Format packages for display"""
        if not packages:
            return "No packages found"
        
        formatted = []
        for i, package in enumerate(packages, 1):
            downloads = package.get('downloads', 0)
            source = package.get('source', 'Unknown')
            formatted.append(f"{i}. **{package.get('name', 'Unknown')}** - 📦 {downloads:,} downloads ({source})")
        
        return "\n".join(formatted)
    
    def _format_projects(self, projects: List[Dict]) -> str:
        """Format projects for display"""
        if not projects:
            return "No projects found"
        
        formatted = []
        for i, project in enumerate(projects, 1):
            source = project.get('source', 'Unknown')
            stars = project.get('stars', 0)
            formatted.append(f"{i}. **{project.get('name', 'Unknown')}** - {source} | ⭐ {stars:,}")
        
        return "\n".join(formatted)
    
    def _format_language_distribution(self, distribution: Dict) -> str:
        """Format language distribution for display"""
        if not distribution:
            return "No language data available"
        
        sorted_langs = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
        return ", ".join([f"{lang} ({count})" for lang, count in sorted_langs[:5]])


def main():
    """Example usage of the Model Answer Enhancer"""
    print("🚀 Model Answer Enhancer - Example Usage")
    print("=" * 50)
    
    enhancer = ModelAnswerEnhancer()
    
    # Example 1: Technology Trends
    print("\n1️⃣ Technology Trends Analysis:")
    trends = enhancer.enhance_technology_trends_answer("AI")
    print(trends["enhanced_answer"])
    
    # Example 2: Startup Research
    print("\n2️⃣ Startup Research:")
    startup_research = enhancer.enhance_startup_research_answer("fintech")
    print(startup_research["enhanced_answer"])
    
    # Example 3: Technology Comparison
    print("\n3️⃣ Technology Comparison:")
    comparison = enhancer.enhance_technology_comparison_answer("React", "Vue")
    print(comparison["enhanced_answer"])
    
    print("\n✅ All examples completed successfully!")
    print("\n💡 Integration Tips:")
    print("- Use these functions in your model response generation")
    print("- Combine with your existing analysis for richer answers")
    print("- Cache results to avoid repeated API calls")
    print("- Add error handling for network issues")


if __name__ == "__main__":
    main()
