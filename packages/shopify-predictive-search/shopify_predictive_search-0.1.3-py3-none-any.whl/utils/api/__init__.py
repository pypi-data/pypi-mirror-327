# src/shopify_search/__init__.py
from src.utils.api.shopify_client import ShopifySearch
from src.config import Config
from src.models.search_results import SearchResults, Product, Collection, Page

__version__ = "0.1.0"
__all__ = ["ShopifySearch", "Config", "SearchResults", "Product", "Collection", "Page"]