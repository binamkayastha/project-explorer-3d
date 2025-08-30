#!/usr/bin/env python3
"""
Test Script for Public API Integration
Verifies that the public API integration works correctly
"""

import sys
import os
import time

# Add the integrations directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'integrations'))

def test_public_api_integration():
    """Test the public API integration"""
    print("🚀 Testing Public API Integration...")
    print("=" * 50)
    
    try:
        from public_apis import PublicAPIManager
        from api_manager import StartupDataManager
        
        # Test PublicAPIManager
        print("🧪 Testing PublicAPIManager...")
        public_api = PublicAPIManager()
        
        # Test GitHub search
        print("  📍 Testing GitHub search...")
        github_results = public_api.search_companies_github("AI", limit=3)
        print(f"    ✅ Found {len(github_results)} GitHub projects")
        
        # Test NPM search
        print("  📦 Testing NPM search...")
        npm_results = public_api.search_companies_npm("react", limit=3)
        print(f"    ✅ Found {len(npm_results)} NPM packages")
        
        # Test PyPI search
        print("  🐍 Testing PyPI search...")
        pypi_results = public_api.search_companies_pypi("machine learning", limit=3)
        print(f"    ✅ Found {len(pypi_results)} PyPI packages")
        
        # Test trending projects
        print("  🔥 Testing trending projects...")
        trending = public_api.get_trending_projects(limit=5)
        print(f"    ✅ Found {len(trending)} trending projects")
        
        # Test market insights
        print("  🧠 Testing market insights...")
        insights = public_api.get_market_insights("AI")
        print(f"    ✅ Generated insights for {insights['search_query']}")
        print(f"    ✅ Total projects found: {insights['total_projects_found']}")
        
        # Test StartupDataManager
        print("\n🧪 Testing StartupDataManager...")
        manager = StartupDataManager()
        
        # Test unified search
        print("  🔍 Testing unified search...")
        unified_results = manager.search_startups("AI", limit=5)
        print(f"    ✅ Found {len(unified_results)} projects across platforms")
        
        # Test API usage stats
        print("  📊 Testing API usage stats...")
        usage = manager.get_api_usage_stats()
        print(f"    ✅ Total requests: {usage['total_requests']}")
        print(f"    ✅ APIs used: {usage['public_apis']['apis_used']}")
        
        print("\n✅ All tests passed! Public API integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False

def main():
    """Main test runner"""
    print("Project Explorer Pro - Public API Integration Test")
    print("Testing free public APIs (GitHub, NPM, PyPI)")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("src/integrations"):
        print("❌ Error: src/integrations directory not found!")
        print("Please run this script from the project root directory.")
        return False
    
    # Run tests
    success = test_public_api_integration()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Run: streamlit run streamlit_app_with_apis.py")
        print("2. Navigate to '🚀 Public API Data' in the sidebar")
        print("3. Start searching for projects!")
        print("4. No API keys or registration required!")
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the integrations directory structure")
        print("3. Check for any missing dependencies")
        print("4. Review the error messages above")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
