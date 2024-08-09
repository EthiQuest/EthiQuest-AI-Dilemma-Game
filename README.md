# EthiQuest-AI-Dilemma-Game

## Overview

The AI Ethics Dilemma Game is an interactive, educational tool designed to help IT professionals and leaders navigate complex ethical scenarios in the field of artificial intelligence. Through a series of AI-generated dilemmas, players make decisions that shape their ethical leadership profile, providing valuable insights into decision-making processes in high-stakes IT environments.

## Features

- Dynamic, AI-generated ethical dilemmas
- Customizable difficulty levels and focus areas
- Web and mobile interfaces for accessibility
- Real-time scoring and ethical profile generation
- Data-driven insights for organizations

## Tech Stack

- Frontend: React, TailwindCSS
- Backend: Python Flask RESTful API
- Database: MySQL
- AI Integration: OpenAI GPT-4 and Anthropic Claude APIs
- Deployment: Render

## Project Structure

```
ai-ethics-dilemma-game/
├── frontend/      # React-based web frontend
├── backend/       # Flask API and server-side logic
├── mobile/        # React Native mobile app
├── docs/          # Project documentation
├── tests/         # Test suites
└── scripts/       # Automation scripts
```

For a detailed project structure, see `docs/project_structure.md`.

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/ai-ethics-dilemma-game.git
   cd ai-ethics-dilemma-game
   ```

2. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

3. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the backend directory with the following:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   DATABASE_URL=your_mysql_database_url
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

5. Initialize the database:
   ```
   flask db upgrade
   ```

## Running with Docker

To run the application using Docker:

1. Make sure you have Docker and Docker Compose installed on your system.

2. Clone the repository:
   ```
   git clone https://github.com/your-username/ai-ethics-dilemma-game.git
   cd ai-ethics-dilemma-game
   ```

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. Access the application at `http://localhost:3000`

To stop the application, use `Ctrl+C` in the terminal where docker-compose is running.

To run in detached mode:
```
docker-compose up -d
```

To stop and remove containers, networks, and volumes:
```
docker-compose down
```

## Running the Application

1. Start the backend server:
   ```
   cd backend
   flask run
   ```

2. Start the frontend development server:
   ```
   cd frontend
   npm start
   ```

3. Access the application at `http://localhost:3000`

## Testing

Run backend tests:
```
cd backend
pytest
```

Run frontend tests:
```
cd frontend
npm test
```

## Deployment

Deployment instructions can be found in `docs/deployment.md`.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- OpenAI for GPT-4 API
- Anthropic for Claude API
- All contributors and testers
