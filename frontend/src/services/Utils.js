import PremIcon from '@/assets/icons/prem-logo2.png'
import LaLigaIcon from '@/assets/icons/la-liga-logo.jpeg'
import BundesligaLogo from '@/assets/icons/bundesliga-logo.png'
import SerieALogo from '@/assets/icons/serie-a-logo.png'
import Ligue1Logo from '@/assets/icons/ligue-1-logo.png'
import eflLogo from '@/assets/icons/efl-logo.png'
import mlsLogo from '@/assets/icons/mls-logo.gif'
import eredivisieLogo from '@/assets/icons/eredivisie.png'
import soccerIcon from '@/assets/icons/soccer-icon.png'

const categories = [
    { category: 'soccer', endpoint: 'highlightsSubreddit', text: 'All', img_url: soccerIcon },
    { category: 'PremierLeague', endpoint: 'highlightsLeague', text: 'Premier League', img_url: PremIcon },
    { category: 'LaLiga', endpoint: 'highlightsLeague', text: 'La Liga', img_url: LaLigaIcon },
    { category: 'Bundesliga', endpoint: 'highlightsLeague', text: 'Bundesliga', img_url: BundesligaLogo },
    { category: 'SerieA', endpoint: 'highlightsLeague', text: 'Serie A', img_url: SerieALogo },
    { category: 'Ligue1', endpoint: 'highlightsLeague', text: 'Ligue 1', img_url: Ligue1Logo },
    { category: 'Eredivisie', endpoint: 'highlightsLeague', text: 'Eredivisie', img_url: eredivisieLogo },
    { category: 'EFL', endpoint: 'highlightsLeague', text: 'Championship', img_url: eflLogo },
    { category: 'MLS', endpoint: 'highlightsLeague', text: 'MLS', img_url: mlsLogo },
  ];

export default {
    getImgUrl(subreddit) {
        return categories.find((c) => c.category === subreddit);
    }
}