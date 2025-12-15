# Arabic Portrait Generator - Coolify Deployment Guide

This guide will help you deploy the Arabic Portrait Generator to your Coolify instance.

## Prerequisites

1. Coolify instance running
2. Git repository (GitHub, GitLab, etc.)
3. Gemini API key with billing enabled

## Quick Deploy Steps

### 1. Push to Git Repository

```bash
cd C:\Users\Ahmed\Desktop\Metalise
git init
git add .
git commit -m "Initial commit - Arabic Portrait Generator"
git remote add origin YOUR_GIT_REPO_URL
git push -u origin main
```

### 2. Create New Service in Coolify

1. **Login to Coolify Dashboard**
2. **Create New Project** (or select existing)
3. **Add New Resource** → **Application**
4. **Select Git Repository**
   - Connect your repository
   - Select the `Metalise` repository
   - Branch: `main`

### 3. Configure Build Settings

**Build Pack:** `Dockerfile`
- Coolify will automatically detect the Dockerfile

**Port:** `5000`

**Health Check Path:** `/api/health`

### 4. Set Environment Variables

In Coolify, go to **Environment Variables** and add:

```env
GEMINI_API_KEY=AIzaSyDwRJm6Hsoj_3-ybCxXbS84OJTdx1IqnNo
FLASK_SECRET_KEY=your-random-secret-key-here-change-this
```

> ⚠️ **Important**: Generate a new `FLASK_SECRET_KEY` for production:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### 5. Configure Domain (Optional)

1. **Add Domain** in Coolify
2. Enter your domain (e.g., `metalise.yourdomain.com`)
3. Coolify will automatically configure SSL/HTTPS

### 6. Deploy

Click **Deploy** button and wait for the build to complete.

## Manual Docker Deployment (Alternative)

If you want to deploy manually:

```bash
# Build the image
docker build -t metalise-app .

# Run the container
docker run -d \
  --name metalise \
  -p 5000:5000 \
  -e GEMINI_API_KEY=your_api_key \
  -e FLASK_SECRET_KEY=your_secret_key \
  metalise-app
```

## Post-Deployment

### Verify Deployment

1. Visit your app URL
2. Check `/api/health` endpoint (should return `{"status": "healthy"}`)
3. Upload a test image and verify the UI works

### Enable Billing for Image Generation

⚠️ **Critical**: Image generation requires Gemini API billing to be enabled

1. Go to [Google Cloud Console](https://console.cloud.google.com/billing)
2. Enable billing on your project
3. Test image generation in your deployed app

## Coolify Configuration Files

The following files are configured for Coolify deployment:

- ✅ `Dockerfile` - Container configuration
- ✅ `requirements.txt` - Python dependencies (includes gunicorn)
- ✅ `.gitignore` - Excludes sensitive files
- ✅ `.env.example` - Environment template
- ✅ `script.js` - Updated for production (dynamic API URL)

## Troubleshooting

### Build Fails

- Check Coolify build logs
- Verify all files are committed to Git
- Ensure `requirements.txt` includes all dependencies

### App Doesn't Start

- Check environment variables are set correctly
- Verify `GEMINI_API_KEY` is valid
- Check Coolify logs for errors

### API Errors (429 Quota)

- Enable billing on your Google Cloud project
- Wait a few minutes for billing to propagate
- Check API quotas in Google Cloud Console

### CORS Errors

- The app includes `flask-cors` for cross-origin requests
- No additional configuration needed

## Architecture

```
┌─────────────────┐
│   Coolify       │
│   - Docker      │
│   - SSL/HTTPS   │
│   - Auto Deploy │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Container     │
│   - Flask App   │
│   - Gunicorn    │
│   - Port 5000   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini API     │
│  (Image Gen)    │
└─────────────────┘
```

## Production Checklist

- [ ] Git repository created and pushed
- [ ] Coolify project configured
- [ ] Environment variables set
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active
- [ ] Google Cloud billing enabled
- [ ] Health check passing
- [ ] Test image generation working
- [ ] `.env` file NOT committed to Git

## Support

For issues:
- Check Coolify logs
- Verify Gemini API key and billing
- Review Flask app logs in container

---

**Your app will be live at**: `https://your-coolify-domain.com`

Enjoy your deployed Arabic Portrait Generator! 🚀✨
