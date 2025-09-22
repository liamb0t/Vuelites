# VueLites

Soccer highlights app with Flask backend API and Nuxt 3 frontend, deployed on Vercel.

## Architecture
- **Backend**: Flask API (`/api/`) serving soccer highlights data
- **Frontend**: Nuxt 3 SPA (`/frontend/`) built to static files
- **Database**: MongoDB for data storage
- **Deployment**: Vercel with Python serverless functions

## Tech Stack

### Backend
- Flask 3.0.0 with CORS support
- MongoDB with PyMongo
- Reddit API integration (PRAW)
- Redis for caching

### Frontend  
- Nuxt 3 (SPA mode)
- Vue 3 + Tailwind CSS
- Shadcn/UI components
- VueUse composables

## Development Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask development server
python backend/run.py
```

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Deployment
Project is configured for Vercel deployment with:
- Flask API as serverless functions (`/api/`)
- Static Nuxt build served from `frontend/dist/`
- Routing configured in `vercel.json`

## Project Structure
```
/
├── api/index.py          # Vercel serverless entry point
├── backend/              # Flask application
├── frontend/             # Nuxt 3 application
├── vercel.json          # Vercel deployment config
└── requirements.txt     # Python dependencies
```

## Supported Leagues
- Bundesliga
- La Liga
- Ligue 1
- MLS