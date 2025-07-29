"""
API routes for KMart ML API
"""

from fastapi import APIRouter, HTTPException
from typing import List
from src.models.models import (
    RecommendationRequest, SearchRequest, ProductRecommendation, SearchResult,
    TrendingProduct, SimilarProduct, ProductViewInteraction, FavoritesInteraction,
    CartInteraction, ChatInteraction, ReviewInteraction, SearchInteraction, InteractionResponse
)
from src.services.ml_services import MLServices
from src.services.interaction_services import InteractionServices

router = APIRouter()

# Global services (will be initialized in main app)
ml_services = None
interaction_services = None

def init_services(data_manager):
    """Initialize services with data manager"""
    global ml_services, interaction_services
    ml_services = MLServices(data_manager)
    interaction_services = InteractionServices(data_manager)

@router.get("/")
def read_root():
    return {"message": "KMart ML API is running!"}

@router.post("/recommendations", response_model=List[ProductRecommendation])
def get_recommendations(request: RecommendationRequest):
    """Get product recommendations for a user"""
    try:
        return ml_services.get_recommendations(request.user_id, request.num_recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[SearchResult])
def search_products(request: SearchRequest):
    """Search products using semantic search"""
    try:
        return ml_services.search_products(request.query, request.num_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending", response_model=List[TrendingProduct])
def get_trending_products(days: int = 7, limit: int = 10):
    """Get trending products based on recent interactions"""
    try:
        return ml_services.get_trending_products(days, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/similar-products/{product_id}", response_model=List[SimilarProduct])
def get_similar_products(product_id: str, limit: int = 5):
    """Get similar products based on product embeddings"""
    try:
        return ml_services.get_similar_products(product_id, limit)
    except Exception as e:
        if "Product not found" in str(e):
            raise HTTPException(status_code=404, detail="Product not found")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_id}")
def get_product_details(product_id: str):
    """Get detailed information about a specific product"""
    try:
        product_info = ml_services.data_manager.get_product_info(product_id)
        if product_info is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        price = ml_services.data_manager.extract_price(product_info)
        
        return {
            "product_id": product_id,
            "name": product_info.get('name', 'Unknown Product'),
            "description": product_info.get('description', ''),
            "price": price,
            "condition": product_info.get('condition', ''),
            "location": product_info.get('location', ''),
            "rating": product_info.get('rating', 0.0)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Interaction tracking routes
@router.post("/interactions/product-view", response_model=InteractionResponse)
def track_product_view(interaction: ProductViewInteraction):
    """Track product view interactions (card tap and details page)"""
    try:
        return interaction_services.track_product_view(interaction)
    except Exception as e:
        if "Invalid interaction type" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interactions/favorites", response_model=InteractionResponse)
def track_favorites_interaction(interaction: FavoritesInteraction):
    """Track favorites/likes interactions"""
    try:
        return interaction_services.track_favorites(interaction)
    except Exception as e:
        if "Invalid interaction type" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interactions/cart", response_model=InteractionResponse)
def track_cart_interaction(interaction: CartInteraction):
    """Track shopping cart interactions"""
    try:
        return interaction_services.track_cart(interaction)
    except Exception as e:
        if "Invalid interaction type" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interactions/chat", response_model=InteractionResponse)
def track_chat_interaction(interaction: ChatInteraction):
    """Track chat interactions"""
    try:
        return interaction_services.track_chat(interaction)
    except Exception as e:
        if "Invalid interaction type" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interactions/review", response_model=InteractionResponse)
def track_review_interaction(interaction: ReviewInteraction):
    """Track review and rating interactions"""
    try:
        return interaction_services.track_review(interaction)
    except Exception as e:
        if "Invalid interaction type" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interactions/search", response_model=InteractionResponse)
def track_search_interaction(interaction: SearchInteraction):
    """Track search interactions"""
    try:
        return interaction_services.track_search(interaction)
    except Exception as e:
        if "Invalid interaction type" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/interactions/user/{user_id}")
def get_user_interactions(user_id: str, limit: int = 50):
    """Get all interactions for a specific user"""
    try:
        return interaction_services.get_user_interactions(user_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/interactions/product/{product_id}")
def get_product_interactions(product_id: str, limit: int = 50):
    """Get all interactions for a specific product"""
    try:
        return interaction_services.get_product_interactions(product_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Additional endpoint for Flutter app compatibility
@router.post("/user_interactions")
def user_interactions_endpoint():
    """Compatibility endpoint for Flutter app - redirects to proper interaction endpoints"""
    return {
        "message": "Please use specific interaction endpoints:",
        "endpoints": {
            "product_view": "POST /interactions/product-view",
            "favorites": "POST /interactions/favorites", 
            "cart": "POST /interactions/cart",
            "chat": "POST /interactions/chat",
            "review": "POST /interactions/review",
            "search": "POST /interactions/search",
            "get_user_interactions": "GET /interactions/user/{user_id}",
            "get_product_interactions": "GET /interactions/product/{product_id}"
        }
    } 