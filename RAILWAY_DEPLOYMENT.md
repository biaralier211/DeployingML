# Railway Deployment Guide for KMart ML API

## Prerequisites
- GitHub account with your code repository
- Railway account (free tier available)
- Your KMart ML API code ready for deployment

## Step 1: Prepare Your Repository

### Ensure these files are in your repository:
- ✅ `api_server_refactored.py` - Main FastAPI application
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Railway process definition
- ✅ `runtime.txt` - Python version specification
- ✅ `railway.json` - Railway configuration
- ✅ `.gitignore` - Exclude unnecessary files
- ✅ `src/` directory - All your source code
- ✅ `data_csv/` directory - Your data files
- ✅ `product_embeddings.npy` - Pre-computed embeddings

## Step 2: Deploy to Railway

### Option A: Deploy via Railway Dashboard

1. **Go to Railway Dashboard**
   - Visit [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your KMart ML API repository

3. **Configure Deployment**
   - Railway will automatically detect it's a Python project
   - The `Procfile` will tell Railway how to run your app
   - Railway will use the `requirements.txt` to install dependencies

4. **Deploy**
   - Click "Deploy" and wait for the build to complete
   - Railway will provide you with a public URL

### Option B: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Railway Project**
   ```bash
   railway init
   ```

4. **Deploy**
   ```bash
   railway up
   ```

## Step 3: Configure Environment Variables (Optional)

In Railway Dashboard:
1. Go to your project
2. Click on "Variables" tab
3. Add any environment variables if needed:
   ```
   PYTHON_VERSION=3.11.0
   ```

## Step 4: Update Your Flutter App

Once deployed, Railway will give you a URL like:
```
https://your-app-name.railway.app
```

### Update your Flutter app's base URL:

**For Production:**
```dart
String baseUrl = "https://your-app-name.railway.app";
```

**For Development (keep local):**
```dart
String baseUrl = "http://10.0.2.2:8000"; // Android Emulator
// or
String baseUrl = "http://10.10.134.12:8000"; // Android Device
```

## Step 5: Test Your Deployment

### Test API Endpoints:
1. **Health Check**: `https://your-app-name.railway.app/`
2. **API Documentation**: `https://your-app-name.railway.app/docs`
3. **Recommendations**: `https://your-app-name.railway.app/recommendations`
4. **Search**: `https://your-app-name.railway.app/search`

### Test from Flutter App:
- Update your Flutter app with the new Railway URL
- Test all functionality to ensure it works

## Step 6: Monitor and Maintain

### Railway Dashboard Features:
- **Logs**: View application logs in real-time
- **Metrics**: Monitor CPU, memory, and network usage
- **Deployments**: View deployment history and rollback if needed
- **Variables**: Manage environment variables
- **Domains**: Configure custom domains

### Common Issues and Solutions:

1. **Build Fails**
   - Check `requirements.txt` for missing dependencies
   - Ensure all files are committed to GitHub
   - Check Railway logs for specific error messages

2. **App Crashes on Startup**
   - Verify `Procfile` syntax
   - Check if all required files are present
   - Review application logs

3. **CORS Issues**
   - Update CORS origins in `api_server_refactored.py`
   - Add your Flutter app's domain to allowed origins

4. **Memory Issues**
   - Railway free tier has memory limits
   - Consider upgrading to paid plan for larger models
   - Optimize model loading and caching

## Step 7: Production Considerations

### Security:
- Update CORS origins to only allow your Flutter app's domain
- Consider adding API key authentication
- Use HTTPS (Railway provides this automatically)

### Performance:
- Monitor memory usage (especially for ML models)
- Consider model optimization for production
- Implement caching strategies

### Scaling:
- Railway automatically scales based on traffic
- Monitor usage and upgrade plan if needed
- Consider database integration for larger datasets

## Step 8: Custom Domain (Optional)

1. **In Railway Dashboard:**
   - Go to your project
   - Click "Settings" → "Domains"
   - Add your custom domain

2. **Update DNS:**
   - Point your domain to Railway's servers
   - Follow Railway's DNS configuration instructions

## Troubleshooting

### Common Error Messages:

1. **"Module not found"**
   - Check `requirements.txt` includes all dependencies
   - Ensure all import paths are correct

2. **"Port already in use"**
   - Railway handles this automatically
   - Use `$PORT` environment variable (already configured)

3. **"File not found"**
   - Ensure all data files are committed to GitHub
   - Check file paths in your code

### Getting Help:
- Check Railway logs in the dashboard
- Review FastAPI documentation
- Check your application logs for specific errors

## Success Checklist

- ✅ Repository pushed to GitHub
- ✅ Railway project created and deployed
- ✅ API endpoints responding correctly
- ✅ Flutter app updated with new URL
- ✅ All functionality tested
- ✅ CORS configured properly
- ✅ Environment variables set (if needed)
- ✅ Monitoring set up

Your KMart ML API is now deployed and ready for production use! 🚀 