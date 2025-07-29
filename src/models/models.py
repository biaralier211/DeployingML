"""
models for KMart ML API
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Core ML Request/Response Models
class RecommendationRequest(BaseModel):
    user_id: str
    num_recommendations: int = 10

class SearchRequest(BaseModel):
    query: str
    num_results: int = 10   

class ProductRecommendation(BaseModel):
    product_id: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    score: float

class SearchResult(BaseModel):
    product_id: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    score: float

class TrendingProduct(BaseModel):
    product_id: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    interaction_count: int

class SimilarProduct(BaseModel):
    product_id: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    similarity_score: float

# Interaction Tracking Models
class ProductViewInteraction(BaseModel):
    user_id: str
    product_id: str
    interaction_type: str  # 'view' or 'view_details'
    metadata: Dict[str, Any] = {}  # Product name, category, price, source

class FavoritesInteraction(BaseModel):
    user_id: str
    product_id: str
    interaction_type: str  # 'like' or 'unlike'
    metadata: Dict[str, Any] = {}  # Product name, category, price

class CartInteraction(BaseModel):
    user_id: str
    product_id: str
    interaction_type: str  # 'add_to_cart'
    metadata: Dict[str, Any] = {}  # Product name, category, price, quantity

class ChatInteraction(BaseModel):
    user_id: str
    product_id: str
    interaction_type: str  # 'chat_message'
    metadata: Dict[str, Any] = {}  # Product name, seller info, message length, chat room ID

class ReviewInteraction(BaseModel):
    user_id: str
    product_id: str
    interaction_type: str  # 'rating'
    metadata: Dict[str, Any] = {}  # Product name, category, rating value, previous rating

class SearchInteraction(BaseModel):
    user_id: str
    interaction_type: str  # 'search'
    metadata: Dict[str, Any] = {}  # Search query, results count

class InteractionResponse(BaseModel):
    success: bool
    message: str
    interaction_id: Optional[str] = None 