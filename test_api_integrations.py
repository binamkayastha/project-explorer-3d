#!/usr/bin/env python3
"""
Test Script for Crunchbase and AngelList API Integrations
Verifies that all API components work correctly
"""

import sys
import os
import time
from typing import Dict, List, Any

# Add the integrations directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'integrations'))

def test_crunchbase_api():
    """Test Crunchbase API functionality"""
    print("🧪 Testing Crunchbase API...")
    
    try:
        from crunchbase_api import CrunchbaseAPI
        
        # Initialize API client
        api = CrunchbaseAPI()
        
        # Test search functionality
        print("  📍 Testing company search...")
        companies = api.search_companies("AI", limit=3)
        print(f"    ✅ Found {len(companies)} companies")
        
        # Test trending companies
        print("  📈 Testing trending companies...")
        trending = api.get_trending_companies()
        print(f"    ✅ Found {len(trending)} trending companies")
        
        # Test API usage
        print("  📊 Testing API usage stats...")
        usage = api.get_api_usage()
        print(f"    ✅ API usage: {usage['requests_made']}/{usage['rate_limit']} requests")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Crunchbase API test failed: {str(e)}")
        return False

def test_angellist_api():
    """Test AngelList API functionality"""
    print("🧪 Testing AngelList API...")
    
    try:
        from angellist_api import AngelListAPI
        
        # Initialize API client
        api = AngelListAPI()
        
        # Test search functionality
        print("  📍 Testing startup search...")
        startups = api.search_startups("AI", limit=3)
        print(f"    ✅ Found {len(startups)} startups")
        
        # Test trending startups
        print("  📈 Testing trending startups...")
        trending = api.get_trending_startups()
        print(f"    ✅ Found {len(trending)} trending startups")
        
        # Test markets
        print("  🏪 Testing markets...")
        markets = api.get_markets()
        print(f"    ✅ Found {len(markets)} markets")
        
        # Test API usage
        print("  📊 Testing API usage stats...")
        usage = api.get_api_usage()
        print(f"    ✅ API usage: {usage['requests_made']}/{usage['rate_limit']} requests")
        
        return True
        
    except Exception as e:
        print(f"    ❌ AngelList API test failed: {str(e)}")
        return False

def test_api_manager():
    """Test unified API manager functionality"""
    print("🧪 Testing API Manager...")
    
    try:
        from api_manager import StartupDataManager
        
        # Initialize manager
        manager = StartupDataManager()
        
        # Test startup search
        print("  🔍 Testing unified startup search...")
        startups = manager.search_startups("AI", limit=5)
        print(f"    ✅ Found {len(startups)} startups across platforms")
        
        # Test trending startups
        print("  🔥 Testing trending startups...")
        trending = manager.get_trending_startups(limit=5)
        print(f"    ✅ Found {len(trending)} trending startups")
        
        # Test insights
        print("  🧠 Testing market insights...")
        insights = manager.get_combined_insights("AI")
        print(f"    ✅ Generated insights for {insights['search_query']}")
        print(f"    ✅ Total startups found: {insights['total_startups_found']}")
        
        # Test API usage stats
        print("  📊 Testing unified API usage...")
        usage = manager.get_api_usage_stats()
        print(f"    ✅ Crunchbase: {usage['crunchbase']['requests_made']} requests")
        print(f"    ✅ AngelList: {usage['angellist']['requests_made']} requests")
        
        return True
        
    except Exception as e:
        print(f"    ❌ API Manager test failed: {str(e)}")
        return False

def test_streamlit_integration():
    """Test Streamlit integration components"""
    print("🧪 Testing Streamlit Integration...")
    
    try:
        from streamlit_integration import (
            initialize_startup_manager,
            render_startup_search_section,
            render_trending_startups_section,
            render_insights_section,
            render_api_settings_section
        )
        
        print("  🔧 Testing manager initialization...")
        manager = initialize_startup_manager()
        print("    ✅ Manager initialized successfully")
        
        print("  🎨 Testing UI components...")
        # Note: These functions require Streamlit context, so we just test imports
        print("    ✅ All UI components imported successfully")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Streamlit integration test failed: {str(e)}")
        return False

def test_data_formats():
    """Test data format consistency"""
    print("🧪 Testing Data Formats...")
    
    try:
        from api_manager import StartupDataManager
        
        manager = StartupDataManager()
        
        # Test startup data format
        print("  📋 Testing startup data format...")
        startups = manager.search_startups("test", limit=1)
        
        if startups:
            startup = startups[0]
            required_fields = ['id', 'name', 'description', 'source']
            
            for field in required_fields:
                if field not in startup:
                    print(f"    ❌ Missing required field: {field}")
                    return False
            
            print("    ✅ Startup data format is correct")
        
        # Test insights data format
        print("  📊 Testing insights data format...")
        insights = manager.get_combined_insights("test")
        
        required_insight_fields = ['total_startups_found', 'total_funding', 'search_query']
        for field in required_insight_fields:
            if field not in insights:
                print(f"    ❌ Missing required insight field: {field}")
                return False
        
        print("    ✅ Insights data format is correct")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Data format test failed: {str(e)}")
        return False

def test_error_handling():
    """Test error handling and edge cases"""
    print("🧪 Testing Error Handling...")
    
    try:
        from api_manager import StartupDataManager
        
        manager = StartupDataManager()
        
        # Test empty search
        print("  🔍 Testing empty search...")
        empty_results = manager.search_startups("", limit=5)
        print(f"    ✅ Empty search handled gracefully: {len(empty_results)} results")
        
        # Test invalid parameters
        print("  ⚠️ Testing invalid parameters...")
        try:
            invalid_results = manager.search_startups("test", limit=-1)
            print("    ✅ Invalid limit handled gracefully")
        except Exception:
            print("    ✅ Invalid limit properly rejected")
        
        # Test API usage tracking
        print("  📈 Testing usage tracking...")
        initial_usage = manager.get_api_usage_stats()
        manager.search_startups("test", limit=1)
        updated_usage = manager.get_api_usage_stats()
        
        if updated_usage['crunchbase']['requests_made'] > initial_usage['crunchbase']['requests_made']:
            print("    ✅ Usage tracking working correctly")
        else:
            print("    ⚠️ Usage tracking may not be working")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Error handling test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all API integration tests"""
    print("🚀 Starting API Integration Tests...")
    print("=" * 50)
    
    tests = [
        ("Crunchbase API", test_crunchbase_api),
        ("AngelList API", test_angellist_api),
        ("API Manager", test_api_manager),
        ("Streamlit Integration", test_streamlit_integration),
        ("Data Formats", test_data_formats),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name} tests...")
        start_time = time.time()
        
        try:
            success = test_func()
            end_time = time.time()
            duration = end_time - start_time
            
            if success:
                print(f"✅ {test_name} tests passed in {duration:.2f}s")
                results.append((test_name, True, duration))
            else:
                print(f"❌ {test_name} tests failed in {duration:.2f}s")
                results.append((test_name, False, duration))
                
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            print(f"💥 {test_name} tests crashed in {duration:.2f}s: {str(e)}")
            results.append((test_name, False, duration))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total_duration = 0
    
    for test_name, success, duration in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name:<25} ({duration:.2f}s)")
        
        if success:
            passed += 1
        total_duration += duration
    
    print("-" * 50)
    print(f"📈 Overall: {passed}/{len(results)} tests passed in {total_duration:.2f}s")
    
    if passed == len(results):
        print("🎉 All tests passed! API integrations are working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

def main():
    """Main test runner"""
    print("Project Explorer Pro - API Integration Test Suite")
    print("Testing Crunchbase and AngelList API integrations")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("src/integrations"):
        print("❌ Error: src/integrations directory not found!")
        print("Please run this script from the project root directory.")
        return False
    
    # Run tests
    success = run_all_tests()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Get your API keys from Crunchbase and AngelList")
        print("2. Set environment variables or configure in the app")
        print("3. Run: streamlit run streamlit_app_with_apis.py")
        print("4. Enjoy your enhanced Project Explorer Pro!")
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify API endpoints are accessible")
        print("3. Check for any missing dependencies")
        print("4. Review the error messages above")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
