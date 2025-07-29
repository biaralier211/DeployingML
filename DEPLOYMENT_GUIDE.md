# KMart ML API - Render Deployment Guide

## Overview
This guide will walk you through deploying your KMart ML API to Render, a cloud platform that offers free hosting for web services.

## Prerequisites
- A GitHub account
- Your KMart ML API code pushed to a GitHub repository
- A Render account (free at render.com)

## Step 1: Prepare Your Repository

### 1.1 Ensure All Files Are Committed
Make sure your repository includes all necessary files:
```
KMartModel/
├── api_server_refactored.py      # Main FastAPI server
├── requirements.txt              # Python dependencies
├── render.yaml                   # Render configuration
├── runtime.txt                   # Python version specification
├── Procfile                      # Process definition
├── .gitignore                    # Git ignore rules
├── data_csv/                     # Your data files
├── product_embeddings.npy        # Pre-computed embeddings
└── src/                          # Source code modules
```

### 1.2 Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Deploy on Render

### 2.1 Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Verify your email address

### 2.2 Create New Web Service
1. Click "New +" button
2. Select "Web Service"
3. Connect your GitHub repository
4. Select the repository containing your KMart ML API

### 2.3 Configure the Service
- **Name**: `kmart-ml-api` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (if code is in root)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn api_server_refactored:app --host 0.0.0.0 --port $PORT`

### 2.4 Advanced Settings (Optional)
- **Auto-Deploy**: Enable to automatically deploy on code changes
- **Health Check Path**: `/` (your root endpoint)

### 2.5 Create Service
Click "Create Web Service" and wait for the build to complete.

## Step 3: Verify Deployment

### 3.1 Check Build Logs
- Monitor the build process in Render dashboard
- Ensure all dependencies install successfully
- Check for any error messages

### 3.2 Test Your API
Once deployed, your API will be available at:
```
https://your-service-name.onrender.com
```

Test the endpoints:
- **Health Check**: `GET https://your-service-name.onrender.com/`
- **API Docs**: `GET https://your-service-name.onrender.com/docs`
- **Recommendations**: `POST https://your-service-name.onrender.com/recommendations`

## Step 4: Update Flutter App

### 4.1 Update Base URL
Replace your local development URL with the Render URL:

```dart
// Before (local development)
String baseUrl = "http://10.0.2.2:8000";

// After (Render deployment)
String baseUrl = "https://your-service-name.onrender.com";
```

### 4.2 Test All Endpoints
Verify that all your Flutter app features work with the deployed API:
- Product recommendations
- Search functionality
- Interaction tracking
- Product details

## Step 5: Environment Variables (If Needed)

If you need to add environment variables:
1. Go to your service in Render dashboard
2. Navigate to "Environment" tab
3. Add any required environment variables
4. Redeploy the service

## Troubleshooting

### Common Issues

#### 1. Build Failures
- **Problem**: Dependencies not installing
- **Solution**: Check `requirements.txt` for correct package versions

#### 2. Runtime Errors
- **Problem**: Application crashes on startup
- **Solution**: Check logs for import errors or missing files

#### 3. Memory Issues
- **Problem**: Application runs out of memory
- **Solution**: Consider upgrading to a paid plan or optimizing model loading

#### 4. Cold Start Delays
- **Problem**: First request takes a long time
- **Solution**: This is normal for free tier. Consider paid plans for better performance

### Debugging Steps
1. Check Render logs in the dashboard
2. Test endpoints using curl or Postman
3. Verify all files are properly committed to GitHub
4. Ensure Python version compatibility

## Performance Optimization

### For Free Tier
- Keep model files as small as possible
- Optimize embedding loading
- Consider lazy loading for heavy operations

### For Paid Plans
- Enable auto-scaling
- Use CDN for static files
- Implement caching strategies

## Monitoring

### Render Dashboard
- Monitor service health
- Check response times
- View error rates
- Track resource usage

### Custom Monitoring
- Implement health check endpoints
- Add logging for debugging
- Monitor API usage patterns

## Security Considerations

### Production Security
1. **CORS Configuration**: Update CORS origins to your Flutter app's domain
2. **Rate Limiting**: Implement rate limiting for API endpoints
3. **Authentication**: Add API key authentication if needed
4. **HTTPS**: Render provides HTTPS by default

### Environment Variables
Store sensitive information in Render environment variables:
- API keys
- Database credentials
- Configuration secrets

## Cost Management

### Free Tier Limits
- 750 hours per month
- 512 MB RAM
- Shared CPU
- Sleep after 15 minutes of inactivity

### Upgrading
Consider upgrading if you need:
- More memory for larger models
- Better performance
- No sleep mode
- Custom domains

## Support

### Render Support
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Render Status](https://status.render.com)

### API Documentation
Your deployed API includes automatic documentation at:
```
https://your-service-name.onrender.com/docs
```

## Next Steps

After successful deployment:
1. Update your Flutter app with the new API URL
2. Test all functionality thoroughly
3. Monitor performance and usage
4. Consider implementing additional features
5. Plan for scaling as your user base grows

## Success Checklist

- [ ] Repository pushed to GitHub
- [ ] Render service created successfully
- [ ] Build completed without errors
- [ ] API endpoints responding correctly
- [ ] Flutter app updated with new URL
- [ ] All features tested and working
- [ ] Documentation updated
- [ ] Monitoring configured

Congratulations! Your KMart ML API is now deployed and accessible worldwide! 🚀 