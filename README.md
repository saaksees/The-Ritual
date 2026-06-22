# The Ritual - AI-Powered Skincare Consultant

A personalized skincare recommendation website using Google Gemini AI.

## 🚀 Quick Deploy to Vercel

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/saaksees/The-Ritual.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **"Add New Project"**
3. Import your `The-Ritual` repository
4. Framework preset: **Other**
5. Click **Deploy**

### Step 3: Add API Key (Environment Variable)

1. In Vercel dashboard → Your project → **Settings** → **Environment Variables**
2. Add:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** `AIzaSyAQ.Ab8RN6IeOrlNI265LrYVKIaRDtMA5V-lT15nK1JXcnQw0JZDtw`
3. Click **Save**
4. Go to **Deployments** → Click the three dots on latest deployment → **Redeploy**

### Step 4: Done! 🎉

Your site will be live at: `https://the-ritual.vercel.app` (or your custom Vercel URL)

---

## 📁 Project Structure

```
The Ritual/
├── index.html          # Frontend (quiz, results, styling)
├── api/
│   └── recommend.py   # Backend API (Google Gemini integration)
├── vercel.json        # Vercel configuration
└── README.md          # This file
```

## 🔑 About the API

- **Model:** Google Gemini 1.5 Flash (free tier)
- **Rate limit:** 15 requests/min
- **No credit card required**
- Get your own key at: [aistudio.google.com](https://aistudio.google.com)

## 🛠️ Local Development

To test locally, you can use Python's http.server, but the API won't work without Vercel's serverless function environment. Best to deploy to Vercel for full functionality.

## 📝 Features

- Personalized skin analysis
- Budget-aware product recommendations
- Indian & Korean beauty brands
- Lifestyle-based customization
- Beautiful, minimal UI
