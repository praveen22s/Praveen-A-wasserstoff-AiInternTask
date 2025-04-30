# What Beats It? 🎮

A creative word association game powered by AI, where players try to guess words that "beat" a given seed word.

![Game Banner](https://via.placeholder.com/800x200?text=What+Beats+It%3F)

## 🌟 Overview

"What Beats It?" is an engaging word game where players are presented with a seed word and must come up with words that conceptually "beat" it. The AI determines if your guess is valid based on creative associations and relationships between words.

## 🚀 Features

- **AI-Powered Validation**: Uses Google's Gemini API to validate word relationships and create creative game content
- **Real-time Feedback**: Instant validation of guesses with AI-generated explanations
- **Game History**: Track your previous guesses and see why they did or didn't beat the seed word
- **Rate Limiting**: Protects the API from excessive requests using SlowAPI
- **Responsive Design**: Play seamlessly on desktop or mobile devices

## 🛠️ Tech Stack

### Frontend
- **React**: Modern, component-based UI framework
- **CSS**: Custom styling for an engaging game experience

### Backend
- **FastAPI**: High-performance Python web framework
- **Google Gemini API**: AI model for creative word association validation
- **SQLAlchemy**: ORM for database interactions
- **Alembic**: Database migration tool
- **SlowAPI**: For API rate limiting

### Database
- **PostgreSQL**: Robust relational database for game data storage

### Caching
- **Redis**: In-memory data store for improved performance

### Deployment
- **Render**: Cloud platform hosting all application components

## 📋 Project Structure

Below is the project structure showing key components:


```
genai-intern-game/
├── backend/               # FastAPI application
│   ├── api/               # API routes and endpoints
│   ├── core/              # Core game logic and AI integration
│   └── db/                # Database models and configuration
├── frontend/              # React application
│   ├── public/            # Static assets
│   └── src/               # React components and logic
│       └── components/    # UI components for the game
└── tests/                 # Testing suite
```

## 💻 Development Environment

This project was developed using Windows Subsystem for Linux (WSL) with Ubuntu. WSL is recommended for Windows users to ensure compatibility with all tools and services used in this project.

### Setting up WSL (for Windows users)

1. Install WSL by running the following in PowerShell as Administrator:
```powershell
wsl --install
```

2. After installation and restart, WSL will use Ubuntu by default. Open Ubuntu from the Start menu to set up your Linux username and password.

3. All commands in this README should be run in the WSL terminal for Windows users.

## 🚀 Getting Started

### Prerequisites
- WSL (Windows Subsystem for Linux) with Ubuntu (for Windows users)
- Node.js (v14+)
- Python (v3.8+)
- PostgreSQL
- Redis

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/praveen22s/Praveen-A-wasserstoff-AiInternTask.git
cd genai-intern-game
```

2. Set up the backend:
```bash
cd backend
pip install -r requirements.txt
# Create .env file with required environment variables (see .env.example below)
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Set up Redis:
```bash
# Install Redis on WSL (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install redis-server

# Install Redis (macOS with Homebrew)
brew install redis

# For native Windows (not recommended)
# Download the Windows port from https://github.com/tporadowski/redis/releases
```

### Running Locally

1. Start Redis server:
```bash
# In WSL (Ubuntu/Debian)
sudo service redis-server start
# or
redis-server

# macOS
redis-server

# Windows (not recommended for development)
# Navigate to Redis installation directory and run
redis-server.exe
```

2. Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

3. Start the frontend:
```bash
cd frontend
npm start
```

4. Visit `http://localhost:3000` in your browser

## 🐳 Docker Deployment

The application can be deployed using Docker Compose:

```bash
docker-compose up -d
```

This will start all services including PostgreSQL and Redis, so no separate Redis installation is needed when using Docker.

## 🧪 Testing

Run the test suite to ensure everything is working correctly:

```bash
# Make sure Redis is running before testing
pytest
```

The test suite includes end-to-end tests that verify the game's functionality.

## 📝 Sample .env File

Create a `.env` file in the root directory with the following variables:

```
# Database (for WSL, ensure PostgreSQL is running in WSL too)
DATABASE_URL=postgresql://username:password@localhost:5432/what_beats_it

# Redis
REDIS_URL=redis://localhost:6379/0

# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# App Settings
DEBUG=True
RATE_LIMIT_PER_MINUTE=10
```

## 📝 Game Rules

1. You'll be presented with a "seed word"
2. Enter a word that you think conceptually "beats" the seed word
3. The AI will determine if your guess is valid and explain why
4. Try to find as many valid words as possible!

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Google Gemini API for powering the creative AI components
- Render for hosting services
- All contributors and testers who helped shape this game
