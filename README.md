# The Ritual - AI-Powered Skincare Consultant

A personalized skincare recommendation website using Groq AI (Llama 3.3 70B).

## 🌐 Live Demo

**[Visit The Ritual](https://the-ritual-saaksees-projects.vercel.app/)**

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
   - **Name:** `GROQ_API_KEY`
   - **Value:** Your Groq API key from [console.groq.com](https://console.groq.com)
3. Click **Save**
4. Go to **Deployments** → Click the three dots on latest deployment → **Redeploy**

### Step 4: Done! 🎉

Your site will be live at: `https://the-ritual-saaksees-projects.vercel.app/`

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

- **Model:** Groq Llama 3.3 70B Versatile
- **Provider:** Groq (super fast inference)
- **Free tier:** 30 requests/min
- Get your API key at: [console.groq.com](https://console.groq.com)

## 🛠️ Local Development

To test locally, you can use Python's http.server, but the API won't work without Vercel's serverless function environment. Best to deploy to Vercel for full functionality.

## 📝 Features

- Personalized skin analysis
- Budget-aware product recommendations
- Indian & Korean beauty brands
- Lifestyle-based customization
- Beautiful, minimal UI
