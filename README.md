# Vuelites

Vuelites is a client made in Vue for watching soccer highlights from Reddit. It gets highlights from Reddit 
using PRAW and Flask and displays them nicely in Vue for your viewing pleasure. 

https://vuelites.onrender.com/

## Local Setup

### 1. Reddit Client Setup in Flask

To use Vuelites locally, set up the Reddit client in Flask using your credentials. Get your credentials from your enviroment or set them manually in the application. 

```python
id = os.environ.get('ID')
client_secret = os.environ.get('CLIENT_SECRET')
user_agent = os.environ.get('USER_AGENT')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

reddit = praw.Reddit(
    client_id=id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)
```

### 2. Run the Flask server

```npm
cd backend
python3 run.py
```

### 3. Run Vue 
```npm
cd frontend
npm run dev
```

Paste the url into your browser for example: http://localhost:5173

### Troubleshooting

Go to flask_api/__init__.py
If for example Vue is hosted locally at http://localhost:5173:

```py
CORS(app, origins=['http://localhost:5173'])
```

Make sure AXIOS is correctly pointing to the Flask server

Go to frontend/src/services/HighlightService.js and make sure the baseURL matches the Flask server
```js
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    withCredentials: false, 
    headers: {
        Accept: 'application/json',
        'Content-type': 'application/json'
    }
})
```
