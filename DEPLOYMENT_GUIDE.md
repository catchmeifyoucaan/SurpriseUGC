# 🚀 ViralForge.ai - Deployment Guide

## 🌟 **Deploy Backend to Render & Frontend to Vercel**

### 📋 **Prerequisites**

1. **GitHub Account** - Push your code to GitHub
2. **Render Account** - For backend deployment
3. **Vercel Account** - For frontend deployment
4. **API Keys** - Get all required API keys

### 🔑 **Required API Keys**

```bash
# AI Services
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
HEYGEN_API_KEY=...
GOOGLE_AI_API_KEY=...  # For Veo3
ANTHROPIC_API_KEY=...

# Cloud Services
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET=viralforge-videos
S3_REGION=us-east-1

# Payments
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Monitoring
SENTRY_DSN=https://...
```

---

## 🚀 **Step 1: Deploy Backend to Render**

### 1.1 **Connect GitHub Repository**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the repository containing ViralForge.ai

### 1.2 **Configure Web Service**

```yaml
# Service Configuration
Name: viralforge-backend
Environment: Python
Region: Oregon (US West)
Branch: main
Root Directory: backend
Build Command: pip install -r requirements.txt && alembic upgrade head
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 1.3 **Set Environment Variables**

In Render dashboard, add these environment variables:

```bash
# Core Settings
PYTHON_VERSION=3.11.0
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=false

# Database (Render will provide this)
DATABASE_URL=postgresql://...

# Redis (Render will provide this)
REDIS_URL=redis://...

# AI Services
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
HEYGEN_API_KEY=...
GOOGLE_AI_API_KEY=...
ANTHROPIC_API_KEY=...

# Cloud Storage
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET=viralforge-videos
S3_REGION=us-east-1

# Payments
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Monitoring
SENTRY_DSN=https://...

# CORS
BACKEND_CORS_ORIGINS=https://viralforge.vercel.app,https://viralforge.ai
```

### 1.4 **Add PostgreSQL Database**

1. Go to **"New +"** → **"PostgreSQL"**
2. Configure:
   ```yaml
   Name: viralforge-db
   Database: viralforge
   User: viralforge_user
   Plan: Starter
   ```

### 1.5 **Add Redis Cache**

1. Go to **"New +"** → **"Redis"**
2. Configure:
   ```yaml
   Name: viralforge-redis
   Plan: Starter
   Max Memory Policy: allkeys-lru
   ```

### 1.6 **Deploy**

1. Click **"Create Web Service"**
2. Render will automatically deploy your backend
3. Your backend URL will be: `https://viralforge-backend.onrender.com`

---

## 🎨 **Step 2: Deploy Frontend to Vercel**

### 2.1 **Connect GitHub Repository**

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"New Project"**
3. Import your GitHub repository
4. Select the repository

### 2.2 **Configure Project**

```yaml
# Project Configuration
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### 2.3 **Set Environment Variables**

In Vercel dashboard, add these environment variables:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://viralforge-backend.onrender.com
NEXT_PUBLIC_APP_NAME=ViralForge.ai
NEXT_PUBLIC_APP_VERSION=1.0.0

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Analytics
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
NEXT_PUBLIC_SENTRY_DSN=https://...

# Feature Flags
NEXT_PUBLIC_ENABLE_QUANTUM_AI=true
NEXT_PUBLIC_ENABLE_VEO3=true
NEXT_PUBLIC_ENABLE_CULTURAL_ADAPTATION=true
NEXT_PUBLIC_ENABLE_HYPER_PERSONALIZATION=true
```

### 2.4 **Deploy**

1. Click **"Deploy"**
2. Vercel will automatically deploy your frontend
3. Your frontend URL will be: `https://viralforge.vercel.app`

---

## 🔧 **Step 3: Configure Custom Domain (Optional)**

### 3.1 **Backend Domain (Render)**

1. Go to your Render service
2. Click **"Settings"** → **"Custom Domains"**
3. Add: `api.viralforge.ai`
4. Configure DNS records as instructed

### 3.2 **Frontend Domain (Vercel)**

1. Go to your Vercel project
2. Click **"Settings"** → **"Domains"**
3. Add: `viralforge.ai`
4. Configure DNS records as instructed

---

## 🧪 **Step 4: Test Deployment**

### 4.1 **Test Backend API**

```bash
# Test health endpoint
curl https://viralforge-backend.onrender.com/health

# Test quantum AI endpoint
curl -X POST https://viralforge-backend.onrender.com/api/v1/quantum-ai/quantum-status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4.2 **Test Frontend**

1. Visit: `https://viralforge.vercel.app`
2. Test all features:
   - ✅ Quantum AI optimization
   - ✅ Veo3 video generation
   - ✅ Cultural adaptation
   - ✅ Hyper-personalization

---

## 📊 **Step 5: Monitor & Scale**

### 5.1 **Render Monitoring**

- **Logs**: View real-time logs in Render dashboard
- **Metrics**: Monitor CPU, memory, and response times
- **Auto-scaling**: Configure based on traffic

### 5.2 **Vercel Analytics**

- **Performance**: Monitor Core Web Vitals
- **Analytics**: Track user behavior
- **Functions**: Monitor API function performance

### 5.3 **Database Monitoring**

- **PostgreSQL**: Monitor query performance
- **Redis**: Monitor cache hit rates
- **Backups**: Configure automatic backups

---

## 🚀 **Step 6: Production Optimization**

### 6.1 **Performance Optimization**

```bash
# Backend (Render)
- Enable auto-scaling
- Configure health checks
- Set up monitoring alerts

# Frontend (Vercel)
- Enable edge caching
- Configure CDN
- Optimize bundle size
```

### 6.2 **Security Hardening**

```bash
# Backend Security
- Enable HTTPS only
- Configure CORS properly
- Set up rate limiting
- Enable security headers

# Frontend Security
- Enable CSP headers
- Configure HSTS
- Set up security monitoring
```

### 6.3 **Backup Strategy**

```bash
# Database Backups
- Daily automated backups
- Point-in-time recovery
- Cross-region replication

# Code Backups
- GitHub repository
- Automated deployments
- Rollback procedures
```

---

## 🔄 **Step 7: CI/CD Pipeline**

### 7.1 **GitHub Actions**

```yaml
# .github/workflows/deploy.yml
name: Deploy ViralForge.ai

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: |
          cd backend && python -m pytest
          cd frontend && npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Render
        run: |
          # Render auto-deploys on push
          echo "Backend deployed to Render"
      
      - name: Deploy to Vercel
        run: |
          # Vercel auto-deploys on push
          echo "Frontend deployed to Vercel"
```

---

## 🎯 **Step 8: Go Live Checklist**

### ✅ **Pre-Launch Checklist**

- [ ] Backend deployed and tested
- [ ] Frontend deployed and tested
- [ ] Database configured and backed up
- [ ] Redis cache configured
- [ ] All API keys configured
- [ ] SSL certificates active
- [ ] Custom domains configured
- [ ] Monitoring set up
- [ ] Error tracking configured
- [ ] Performance optimized
- [ ] Security hardened
- [ ] Backup strategy in place

### ✅ **Launch Day**

- [ ] Monitor system health
- [ ] Track user registrations
- [ ] Monitor API performance
- [ ] Check error rates
- [ ] Verify payments work
- [ ] Test all features
- [ ] Monitor server resources

---

## 🆘 **Troubleshooting**

### Common Issues

1. **Backend Won't Start**
   ```bash
   # Check logs in Render dashboard
   # Verify environment variables
   # Check database connection
   ```

2. **Frontend Build Fails**
   ```bash
   # Check Vercel build logs
   # Verify dependencies
   # Check environment variables
   ```

3. **API Connection Issues**
   ```bash
   # Verify CORS settings
   # Check API URL configuration
   # Test API endpoints directly
   ```

4. **Database Connection Issues**
   ```bash
   # Check DATABASE_URL
   # Verify database is running
   # Check network connectivity
   ```

---

## 🎉 **Success!**

Your **ViralForge.ai** platform is now deployed and ready to revolutionize content creation!

### 🌟 **Your URLs**
- **Frontend**: `https://viralforge.vercel.app`
- **Backend**: `https://viralforge-backend.onrender.com`
- **API Docs**: `https://viralforge-backend.onrender.com/docs`

### 🚀 **Next Steps**
1. **Test all features** thoroughly
2. **Configure monitoring** and alerts
3. **Set up analytics** tracking
4. **Launch marketing** campaign
5. **Scale globally** with the built-in features

---

**ViralForge.ai - The Future of AI-Powered Content Creation is Now Live!** 🚀