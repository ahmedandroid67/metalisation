# Deployment Preparation Checklist

## Created Files ✅
- [x] Dockerfile (with gunicorn for production)
- [x] Updated requirements.txt (added gunicorn)
- [x] Updated script.js (dynamic API URL)
- [x] DEPLOYMENT.md (comprehensive guide)
- [x] .coolify (configuration notes)
- [x] Updated .gitignore

## Next Steps for Deployment

### 1. Initialize Git Repository
```bash
cd C:\Users\Ahmed\Desktop\Metalise
git init
git add .
git commit -m "Initial commit - Arabic Portrait Generator"
```

### 2. Push to GitHub/GitLab
```bash
git remote add origin YOUR_REPO_URL
git push -u origin main
```

### 3. Deploy in Coolify
1. Login to Coolify
2. Create new Application
3. Connect Git repository
4. Set environment variables:
   - `GEMINI_API_KEY`
   - `FLASK_SECRET_KEY`
5. Deploy!

## Important Notes
- ⚠️ API key in `.env` will NOT be committed (in .gitignore)
- ⚠️ Must set environment variables in Coolify
- ⚠️ Must enable billing for Gemini API
- ✅ Dockerfile uses gunicorn for production
- ✅ Health check endpoint: `/api/health`
- ✅ Port 5000 exposed

## Files Ready for Deployment
All necessary files are now in `C:\Users\Ahmed\Desktop\Metalise`
