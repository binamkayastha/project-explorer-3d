"""
Integrations Package for Project Explorer Pro
Contains API integrations for free public APIs
"""

from .public_apis import PublicAPIManager
from .api_manager import StartupDataManager
from .streamlit_integration import (
    initialize_startup_manager,
    render_startup_search_section,
    render_trending_startups_section,
    render_insights_section,
    render_api_settings_section,
    add_startup_data_to_sidebar,
    render_startup_data_pages
)

__all__ = [
    'PublicAPIManager',
    'StartupDataManager',
    'initialize_startup_manager',
    'render_startup_search_section',
    'render_trending_startups_section',
    'render_insights_section',
    'render_api_settings_section',
    'add_startup_data_to_sidebar',
    'render_startup_data_pages'
]

__version__ = "2.0.0"
