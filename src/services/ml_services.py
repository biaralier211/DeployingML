"""
ML services for KMart ML API - Optimized for Render deployment
"""

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.models.models import ProductRecommendation, SearchResult, TrendingProduct, SimilarProduct

class MLServices:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        # Initialize TF-IDF for text search (lighter alternative to transformers)
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self._initialize_tfidf()
    
    def _initialize_tfidf(self):
        """Initialize TF-IDF vectorizer for text search"""
        try:
            # Combine product names and descriptions for TF-IDF
            texts = []
            for _, product in self.data_manager.product_df.iterrows():
                name = product.get('name', '')
                description = product.get('description', '')
                texts.append(f"{name} {description}")
            
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        except Exception as e:
            print(f"Warning: TF-IDF initialization failed: {e}")
    
    def get_recommendations(self, user_id: str, num_recommendations: int = 5) -> List[ProductRecommendation]:
        """Get product recommendations for a user"""
        try:
            # Simple popularity-based recommendations for now
            # In production, you'd want to implement proper collaborative filtering
            
            # Get top products by rating/price ratio
            recommendations = []
            products = self.data_manager.product_df.copy()
            
            # Calculate a simple score based on rating and price
            products['score'] = products['rating'].fillna(3.0) / (products['price'].fillna(10.0) + 1)
            top_products = products.nlargest(num_recommendations, 'score')
            
            for _, product in top_products.iterrows():
                price = self.data_manager.extract_price(product)
                
                recommendations.append(ProductRecommendation(
                    product_id=product.get('id', ''),
                    name=product.get('name', 'Unknown Product'),
                    description=product.get('description', ''),
                    price=price,
                    score=float(product['score'])
                ))
            
            return recommendations
        
        except Exception as e:
            raise Exception(f"Error getting recommendations: {str(e)}")
    
    def search_products(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """Search products using TF-IDF similarity"""
        try:
            if self.tfidf_vectorizer is None or self.tfidf_matrix is None:
                # Fallback to simple text search
                return self._simple_text_search(query, num_results)
            
            # Transform query using TF-IDF
            query_vector = self.tfidf_vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
            top_indices = similarities.argsort()[::-1][:num_results]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0:  # Only include relevant results
                    product_info = self.data_manager.product_df.iloc[idx]
                    price = self.data_manager.extract_price(product_info)
                    
                    results.append(SearchResult(
                        product_id=product_info.get('id', ''),
                        name=product_info.get('name', 'Unknown Product'),
                        description=product_info.get('description', ''),
                        price=price,
                        score=float(similarities[idx])
                    ))
            
            return results
        
        except Exception as e:
            # Fallback to simple search
            return self._simple_text_search(query, num_results)
    
    def _simple_text_search(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """Simple text-based search as fallback"""
        try:
            query_lower = query.lower()
            results = []
            
            for _, product in self.data_manager.product_df.iterrows():
                name = product.get('name', '').lower()
                description = product.get('description', '').lower()
                
                # Simple keyword matching
                if query_lower in name or query_lower in description:
                    price = self.data_manager.extract_price(product)
                    score = 0.5  # Default score for simple search
                    
                    results.append(SearchResult(
                        product_id=product.get('id', ''),
                        name=product.get('name', 'Unknown Product'),
                        description=product.get('description', ''),
                        price=price,
                        score=score
                    ))
                    
                    if len(results) >= num_results:
                        break
            
            return results
        
        except Exception as e:
            raise Exception(f"Error in simple text search: {str(e)}")
    
    def get_trending_products(self, days: int = 7, limit: int = 10) -> List[TrendingProduct]:
        """Get trending products based on recent interactions"""
        try:
            # Simple trending based on product ratings and recent activity
            products = self.data_manager.product_df.copy()
            
            # Calculate trending score (rating * recent activity factor)
            products['trending_score'] = products['rating'].fillna(3.0) * 1.1  # Simple trending factor
            
            top_trending = products.nlargest(limit, 'trending_score')
            
            trending_products = []
            for _, product in top_trending.iterrows():
                price = self.data_manager.extract_price(product)
                
                trending_products.append(TrendingProduct(
                    product_id=product.get('id', ''),
                    name=product.get('name', 'Unknown Product'),
                    description=product.get('description', ''),
                    price=price,
                    trending_score=float(product['trending_score']),
                    days_trending=days
                ))
            
            return trending_products
        
        except Exception as e:
            raise Exception(f"Error getting trending products: {str(e)}")
    
    def get_similar_products(self, product_id: str, limit: int = 5) -> List[SimilarProduct]:
        """Get similar products based on category and price range"""
        try:
            # Find the target product
            target_product = None
            for _, product in self.data_manager.product_df.iterrows():
                if product.get('id') == product_id:
                    target_product = product
                    break
            
            if target_product is None:
                raise Exception("Product not found")
            
            target_price = self.data_manager.extract_price(target_product)
            target_category = target_product.get('category', '')
            
            # Find similar products based on category and price
            similar_products = []
            for _, product in self.data_manager.product_df.iterrows():
                if product.get('id') != product_id:  # Exclude the target product
                    price = self.data_manager.extract_price(product)
                    category = product.get('category', '')
                    
                    # Calculate similarity score
                    price_similarity = 1.0 / (1.0 + abs(price - target_price) / max(price, target_price, 1))
                    category_similarity = 1.0 if category == target_category else 0.3
                    
                    similarity_score = (price_similarity + category_similarity) / 2
                    
                    if similarity_score > 0.3:  # Only include reasonably similar products
                        similar_products.append({
                            'product': product,
                            'score': similarity_score
                        })
            
            # Sort by similarity score and return top results
            similar_products.sort(key=lambda x: x['score'], reverse=True)
            
            results = []
            for item in similar_products[:limit]:
                product = item['product']
                price = self.data_manager.extract_price(product)
                
                results.append(SimilarProduct(
                    product_id=product.get('id', ''),
                    name=product.get('name', 'Unknown Product'),
                    description=product.get('description', ''),
                    price=price,
                    similarity_score=float(item['score'])
                ))
            
            return results
        
        except Exception as e:
            raise Exception(f"Error getting similar products: {str(e)}") 