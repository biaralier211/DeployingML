# KMart ML API Endpoints Summary

## Base URL
```
http://localhost:8000
```

## Core ML Endpoints

### 1. Get Recommendations
**Endpoint:** `POST /recommendations`
**Description:** Get personalized product recommendations for a user

**Request Body:**
```json
{
  "user_id": "user123",
  "num_recommendations": 5
}
```

**Response:**
```json
[
  {
    "product_id": "product123",
    "name": "Product Name",
    "description": "Product description",
    "price": 150000.0,
    "score": 0.85
  }
]
```

### 2. Search Products
**Endpoint:** `POST /search`
**Description:** Search products using semantic search

**Request Body:**
```json
{
  "query": "laptop computer",
  "num_results": 5
}
```

**Response:**
```json
[
  {
    "product_id": "product123",
    "name": "Product Name",
    "description": "Product description",
    "price": 150000.0,
    "score": 0.92
  }
]
```

### 3. Get Trending Products
**Endpoint:** `GET /trending`
**Description:** Get trending products based on recent interactions

**Query Parameters:**
- `days` (optional): Number of days to look back (default: 7)
- `limit` (optional): Number of products to return (default: 10)

**Response:**
```json
[
  {
    "product_id": "product123",
    "name": "Product Name",
    "description": "Product description",
    "price": 150000.0,
    "interaction_count": 25
  }
]
```

### 4. Get Similar Products
**Endpoint:** `GET /similar-products/{product_id}`
**Description:** Get similar products based on product embeddings

**Query Parameters:**
- `limit` (optional): Number of similar products to return (default: 5)

**Response:**
```json
[
  {
    "product_id": "product456",
    "name": "Similar Product",
    "description": "Product description",
    "price": 120000.0,
    "similarity_score": 0.87
  }
]
```

### 5. Get Product Details
**Endpoint:** `GET /products/{product_id}`
**Description:** Get detailed information about a specific product

**Response:**
```json
{
  "product_id": "product123",
  "name": "Product Name",
  "description": "Product description",
  "price": 150000.0,
  "condition": "New",
  "location": "Kampala",
  "rating": 4.5
}
```

## Interaction Tracking Endpoints (Flutter App)

### 1. Track Product Views
**Endpoint:** `POST /interactions/product-view`
**Description:** Track product card taps and details page views

**Request Body:**
```json
{
  "user_id": "user123",
  "product_id": "product123",
  "interaction_type": "view",  // or "view_details"
  "metadata": {
    "source": "home_page",
    "category": "electronics"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Product view tracked successfully",
  "interaction_id": "int_20241201_143022_user123"
}
```

### 2. Track Favorites/Likes
**Endpoint:** `POST /interactions/favorites`
**Description:** Track product likes and unlikes

**Request Body:**
```json
{
  "user_id": "user123",
  "product_id": "product123",
  "interaction_type": "like",  // or "unlike"
  "metadata": {
    "category": "electronics"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Product like tracked successfully",
  "interaction_id": "int_20241201_143022_user123"
}
```

### 3. Track Shopping Cart
**Endpoint:** `POST /interactions/cart`
**Description:** Track add to cart interactions

**Request Body:**
```json
{
  "user_id": "user123",
  "product_id": "product123",
  "interaction_type": "add_to_cart",
  "metadata": {
    "quantity": 2,
    "category": "electronics"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Product added to cart tracked successfully",
  "interaction_id": "int_20241201_143022_user123"
}
```

### 4. Track Chat Interactions
**Endpoint:** `POST /interactions/chat`
**Description:** Track chat messages related to products

**Request Body:**
```json
{
  "user_id": "user123",
  "product_id": "product123",
  "interaction_type": "chat_message",
  "metadata": {
    "seller_info": "John Doe",
    "message_length": 45,
    "chat_room_id": "room_123"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Chat interaction tracked successfully",
  "interaction_id": "int_20241201_143022_user123"
}
```

### 5. Track Reviews & Ratings
**Endpoint:** `POST /interactions/review`
**Description:** Track product ratings and reviews

**Request Body:**
```json
{
  "user_id": "user123",
  "product_id": "product123",
  "interaction_type": "rating",
  "metadata": {
    "rating_value": 5,
    "previous_rating": 4,
    "review_text": "Great product!",
    "category": "electronics"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Review interaction tracked successfully",
  "interaction_id": "int_20241201_143022_user123"
}
```

### 6. Track Search Interactions
**Endpoint:** `POST /interactions/search`
**Description:** Track search queries

**Request Body:**
```json
{
  "user_id": "user123",
  "interaction_type": "search",
  "metadata": {
    "search_query": "laptop computer",
    "results_count": 15
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Search interaction tracked successfully",
  "interaction_id": "int_20241201_143022_user123"
}
```

## Analytics Endpoints

### 1. Get User Interactions
**Endpoint:** `GET /interactions/user/{user_id}`
**Description:** Get all interactions for a specific user

**Query Parameters:**
- `limit` (optional): Number of interactions to return (default: 50)

**Response:**
```json
{
  "user_id": "user123",
  "total_interactions": 25,
  "interactions": [
    {
      "interaction_id": "int_20241201_143022_user123",
      "product_id": "product123",
      "interaction_type": "view",
      "timestamp": "2024-12-01T14:30:22",
      "quantity": "",
      "rating": "",
      "review": "",
      "metadata": {
        "product_name": "Product Name",
        "category": "electronics",
        "price": 150000.0
      }
    }
  ]
}
```

### 2. Get Product Interactions
**Endpoint:** `GET /interactions/product/{product_id}`
**Description:** Get all interactions for a specific product

**Query Parameters:**
- `limit` (optional): Number of interactions to return (default: 50)

**Response:**
```json
{
  "product_id": "product123",
  "total_interactions": 15,
  "interactions": [
    {
      "interaction_id": "int_20241201_143022_user123",
      "user_id": "user123",
      "interaction_type": "view",
      "timestamp": "2024-12-01T14:30:22",
      "quantity": "",
      "rating": "",
      "review": "",
      "metadata": {
        "product_name": "Product Name",
        "category": "electronics",
        "price": 150000.0
      }
    }
  ]
}
```

## Flutter App Integration Examples

### Product View Tracking
```dart
// Product card tap
await http.post(
  Uri.parse('http://localhost:8000/interactions/product-view'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'user_id': 'user123',
    'product_id': 'product123',
    'interaction_type': 'view',
    'metadata': {
      'source': 'home_page',
      'category': 'electronics'
    }
  })
);

// Product details page view
await http.post(
  Uri.parse('http://localhost:8000/interactions/product-view'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'user_id': 'user123',
    'product_id': 'product123',
    'interaction_type': 'view_details',
    'metadata': {
      'source': 'product_list',
      'category': 'electronics'
    }
  })
);
```

### Favorites Tracking
```dart
// Like product
await http.post(
  Uri.parse('http://localhost:8000/interactions/favorites'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'user_id': 'user123',
    'product_id': 'product123',
    'interaction_type': 'like',
    'metadata': {
      'category': 'electronics'
    }
  })
);

// Unlike product
await http.post(
  Uri.parse('http://localhost:8000/interactions/favorites'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'user_id': 'user123',
    'product_id': 'product123',
    'interaction_type': 'unlike',
    'metadata': {
      'category': 'electronics'
    }
  })
);
```

### Cart Tracking
```dart
// Add to cart
await http.post(
  Uri.parse('http://localhost:8000/interactions/cart'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'user_id': 'user123',
    'product_id': 'product123',
    'interaction_type': 'add_to_cart',
    'metadata': {
      'quantity': 2,
      'category': 'electronics'
    }
  })
);
```

### Chat Tracking
```dart
// Send chat message
await http.post(
  Uri.parse('http://localhost:8000/interactions/chat'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'user_id': 'user123',
    'product_id': 'product123',
    'interaction_type': 'chat_message',
    'metadata': {
      'seller_info': 'John Doe',
      'message_length': 45,
      'chat_room_id': 'room_123'
    }
  })
);
```

### Review Tracking
```dart
// Rate product
await http.post(
  Uri.parse('http://localhost:8000/interactions/review'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'user_id': 'user123',
    'product_id': 'product123',
    'interaction_type': 'rating',
    'metadata': {
      'rating_value': 5,
      'previous_rating': 4,
      'review_text': 'Great product!',
      'category': 'electronics'
    }
  })
);
```

### Search Tracking
```dart
// Search query
await http.post(
  Uri.parse('http://localhost:8000/interactions/search'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'user_id': 'user123',
    'interaction_type': 'search',
    'metadata': {
      'search_query': 'laptop computer',
      'results_count': 15
    }
  })
);
```

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (product/user not found)
- `500`: Internal Server Error

Error response format:
```json
{
  "detail": "Error message describing the issue"
}
```

## Notes

1. All interaction data is automatically saved to the CSV file and used for analytics
2. Metadata is stored as JSON and can include any additional information
3. Interaction IDs are automatically generated with timestamps
4. The API automatically enriches metadata with product information when available
5. All endpoints support CORS for Flutter app integration 