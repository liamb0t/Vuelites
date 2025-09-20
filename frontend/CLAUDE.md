# GoalRush Frontend

Soccer highlights app frontend built with Nuxt 3. This is the client-side application that displays soccer highlights and integrates with the Flask backend API.

## Tech Stack
- **Framework**: Nuxt 3 (SPA mode)
- **UI**: Vue 3 + Tailwind CSS + Shadcn/UI components
- **Icons**: Lucide Vue Next
- **Animations**: Motion-v
- **State**: VueUse composables

## Project Structure
- `components/` - Vue components including HighlightsPage, LeagueFilter, SearchBar, TimeFilter
- `composables/` - Vue composables like useHighlights for data fetching
- `pages/highlights/` - Highlights pages
- `utils/` - Utility functions
- `assets/img/` - League logos and images

## Development Commands
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production (generates SPA in dist/)
npm run build

# Preview production build
npm run preview
```

## Backend Integration
- Backend located at `../vuelites/backend` (Flask app)
- Frontend builds to `dist/` which is served as static SPA by Flask
- SSR disabled (`ssr: false`) for SPA deployment

## League Support
Currently supports:
- Bundesliga
- La Liga 
- Ligue 1
- MLS

## Key Features
- Soccer highlights browsing
- League filtering
- Time-based filtering
- Video playback
- Responsive design with Tailwind CSS