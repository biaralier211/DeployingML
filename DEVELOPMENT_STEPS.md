# KMart ML Model Development Steps

## Project Overview
This document outlines the complete development process for the KMart ML API system, including data processing, model development, API creation, and deployment setup.

## 1. Project Structure Setup

### Initial Directory Structure
```
KMartModel/
├── api_server_refactored.py      # Main FastAPI server
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── data_csv/                     # Raw data storage
├── product_embeddings.npy        # Pre-computed embeddings
├── src/                          # Modular source code
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── api_routes.py         # API endpoint definitions
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_manager.py       # Data loading and management
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py             # Pydantic data models
│   └── services/
│       ├── __init__.py
│       ├── interaction_services.py # User interaction tracking
│       └── ml_services.py        # ML recommendation logic
```

## 2. Data Processing and Model Development

### Step 1: Data Collection and Preparation
- Collected product data from CSV files
- Cleaned and preprocessed product information
- Extracted product features (name, description, price, condition, location, rating)
- Normalized data formats for consistency

### Step 2: Embedding Generation
- Implemented semantic embedding generation using sentence transformers
- Created product embeddings for similarity calculations
- Saved embeddings to `product_embeddings.npy` for fast access
- Optimized embedding storage and retrieval

### Step 3: Recommendation System Development
- Built collaborative filtering-based recommendation engine
- Implemented content-based filtering using product embeddings
- Created hybrid recommendation approach combining multiple signals
- Added trending products analysis based on recent interactions

## 3. API Development

### Step 1: FastAPI Server Setup
```python
# Main server configuration
app = FastAPI(
    title="KMart ML API", 
    description="API for product recommendations, search, and trending products"
)
```

### Step 2: CORS Configuration for Flutter Integration
```python
# CORS middleware setup for cross-platform access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configured for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 3: API Endpoints Implementation
- **Recommendations**: `/recommendations` - Get personalized product recommendations
- **Search**: `/search` - Semantic product search
- **Trending**: `/trending` - Get trending products
- **Similar Products**: `/similar-products/{product_id}` - Find similar items
- **Product Details**: `/products/{product_id}` - Get detailed product information

### Step 4: Interaction Tracking System
- **Product Views**: Track when users view products
- **Favorites**: Monitor favorite/unfavorite actions
- **Cart Interactions**: Track add/remove from cart
- **Chat Interactions**: Monitor customer service interactions
- **Reviews**: Track product review submissions
- **Search Interactions**: Monitor search queries and results

## 4. Modular Architecture Implementation

### Step 1: Data Manager (`src/data/data_manager.py`)
- Centralized data loading and management
- Product information retrieval
- Price extraction and normalization
- Embedding storage and access

### Step 2: ML Services (`src/services/ml_services.py`)
- Recommendation engine implementation
- Search functionality using embeddings
- Trending products calculation
- Similar products identification

### Step 3: Interaction Services (`src/services/interaction_services.py`)
- User interaction tracking and storage
- Interaction analytics and insights
- Real-time interaction processing

### Step 4: API Routes (`src/api/api_routes.py`)
- RESTful endpoint definitions
- Request/response model handling
- Error handling and validation
- Service integration

### Step 5: Data Models (`src/models/models.py`)
- Pydantic models for request/response validation
- Type safety and data validation
- API documentation generation

## 5. Network Configuration for Flutter Integration

### Step 1: Server Binding Configuration
```python
# Changed from localhost to 0.0.0.0 for network access
uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 2: Cross-Platform URL Configuration
- **Android Emulator**: `http://10.0.2.2:8000`
- **Android Device**: `http://10.10.134.12:8000`
- **iOS Simulator**: `http://localhost:8000`
- **iOS Device**: `http://10.10.134.12:8000`

## 6. Dependencies and Environment Setup

### Step 1: Python Environment
```bash
# Virtual environment creation
python -m venv myenv
myenv\Scripts\activate  # Windows
```

### Step 2: Required Packages (`requirements.txt`)
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
sentence-transformers==2.2.2
```

### Step 3: Package Installation
```bash
pip install -r requirements.txt
```

## 7. Testing and Validation

### Step 1: API Testing
- Tested all endpoints using FastAPI's automatic documentation
- Validated request/response models
- Verified error handling and edge cases

### Step 2: Network Connectivity Testing
- Confirmed server accessibility from different platforms
- Tested CORS functionality
- Validated cross-platform communication

### Step 3: ML Model Validation
- Tested recommendation accuracy
- Validated search functionality
- Confirmed trending products calculation

## 8. Deployment and Production Considerations

### Step 1: Security Configuration
- CORS origins should be restricted in production
- API key authentication (if needed)
- Rate limiting implementation

### Step 2: Performance Optimization
- Embedding caching for fast retrieval
- Database integration for scalability
- Load balancing for high traffic

### Step 3: Monitoring and Logging
- API usage analytics
- Error tracking and reporting
- Performance monitoring

## 9. Flutter Integration Steps

### Step 1: Base URL Configuration
- Configure appropriate base URL based on platform
- Implement retry logic for network failures
- Add error handling for connection issues

### Step 2: API Client Implementation
- HTTP client setup with proper headers
- Request/response serialization
- Error handling and user feedback

### Step 3: User Interface Integration
- Recommendation display
- Search functionality
- Product detail pages
- Interaction tracking

## 10. Key Achievements

### Technical Accomplishments
- ✅ Modular, scalable API architecture
- ✅ ML-powered recommendation system
- ✅ Real-time interaction tracking
- ✅ Cross-platform compatibility
- ✅ Comprehensive error handling
- ✅ Type-safe API with Pydantic models

### Business Value
- ✅ Personalized product recommendations
- ✅ Enhanced search capabilities
- ✅ User behavior analytics
- ✅ Improved customer engagement
- ✅ Scalable e-commerce solution

## 11. Future Enhancements

### Planned Improvements
- Machine learning model retraining pipeline
- Advanced analytics dashboard
- A/B testing framework
- Real-time notifications
- Advanced search filters
- Recommendation explainability

### Scalability Considerations
- Database migration for large datasets
- Microservices architecture
- Cloud deployment
- CDN integration
- Caching strategies

## 12. Troubleshooting Guide

### Common Issues and Solutions
1. **Connection Refused**: Ensure server is running on 0.0.0.0:8000
2. **CORS Errors**: Verify CORS middleware configuration
3. **Model Loading**: Check file paths and dependencies
4. **Network Access**: Confirm IP address and firewall settings

## Conclusion

This KMart ML API system represents a complete end-to-end solution for e-commerce recommendation and search functionality. The modular architecture ensures maintainability and scalability, while the comprehensive API design enables seamless integration with Flutter applications across multiple platforms.

The system successfully combines machine learning capabilities with modern web API design principles, providing a robust foundation for e-commerce applications with personalized user experiences. 