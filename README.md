Here’s a README.md file summarizing the use cases, setup instructions, and functionality implemented so far for your project:

# Crypto Tracker API and Web Application

This project is a **crypto tracking platform** that provides real-time information about the top cryptocurrencies by market capitalization. The backend uses **FastAPI** to fetch and serve data from the **CoinMarketCap API**, while the frontend is built with **React** and styled using **Material UI**. 

The system supports the following features:
- **Backend**:
  - Fetches data from CoinMarketCap and populates both an **in-memory cache** and a **PostgreSQL database** for persistence.
  - Updates cryptocurrency data every 15 minutes using a background scheduler.
  - Serves a REST API for accessing the latest crypto data.
  - Automatically handles data initialization during startup (e.g., populates the database and cache).
- **Frontend**:
  - Displays a user-friendly, sortable table of the top 50 cryptocurrencies.
  - Styled using **Material UI** for a modern, responsive design.
  - Includes a navigation bar with placeholders for future features (e.g., login, search).

---

## Features and Use Cases

### Backend
- **Real-Time Crypto Data Fetching**:
  - The system fetches cryptocurrency data from the CoinMarketCap API, including:
    - Name, Symbol, Rank
    - Price (USD)
    - 24-hour % change
    - 24-hour trading volume
    - Market capitalization
  - Data is refreshed every 15 minutes and stored in:
    - **In-memory cache**: For fast retrieval by the API.
    - **PostgreSQL database**: For persistence and reliability.
    
- **API Endpoints**:
  - `/` - Health check for the backend.
  - `/cryptos` - Fetches the top 50 cryptocurrencies from the in-memory cache.
    - Includes fields like rank, name, price, market cap, 24-hour change, and volume.

- **Resilient Startup**:
  - On startup:
    - Data is first fetched from CoinMarketCap.
    - Cache and database are populated to ensure no empty states.
    - Background scheduler starts to refresh data periodically.

### Frontend
- **Sortable Cryptocurrency Table**:
  - Displays the top 50 cryptocurrencies in a Material UI table.
  - Columns include:
    - Rank (#)
    - Name
    - Price (formatted as `$`)
    - 24h % Change (with red/green coloring for negative/positive values)
    - 24h Volume (formatted in `B` for billions or `M` for millions)
    - Market Cap (formatted in `B` for billions)
  - Columns are sortable by clicking on the headers.
  
- **Navigation Bar**:
  - Includes links for:
    - `Home`: Links to the homepage with the cryptocurrency table.
    - `Placeholder 1` and `Placeholder 2`: For future features.
    - A **login button** on the far right.
  - A **search bar** for future functionality (currently placeholder only).

---

## Getting Started

### Prerequisites

1. **Python 3.9+**
2. **Node.js** (LTS version, e.g., 18.x)
3. **PostgreSQL** installed and running locally.
4. **CoinMarketCap API Key**:
   - Sign up at [CoinMarketCap API](https://coinmarketcap.com/api/) and generate a free API key.

---

### Setup Instructions

#### Backend

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd coin_app
   ```
   
2.	Create a virtual environment and install dependencies:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

3.	Set up environment variables:
	•	Create a .env file in the coin_app directory:
```
COINMARKETCAP_API_KEY=your_api_key_here
DATABASE_URL=postgresql://localhost:5432/coin_app_db
```

4.	Ensure PostgreSQL is running and create a database:
```
brew services start postgresql
createdb coin_app_db
```

5.	Run the backend:
```
uvicorn main:app --reload
```

6.	Verify the backend:
	•	Visit http://127.0.0.1:8000/ to ensure the server is running.
	•	Visit http://127.0.0.1:8000/cryptos to fetch the latest cryptocurrency data.

Frontend

1.	Navigate to the coin_client folder:
```
cd coin_client
```
2.	Install dependencies:
```
npm install
```
3.	Start the React development server:
```
npm start
```
4.	Visit the frontend in your browser:
	•	Open http://localhost:3000 to see the table of cryptocurrencies.

Project Structure

Backend
```
coin_app/
├── db/
│   ├── models.py          # SQLAlchemy models for database
│   └── session.py         # DB connection and session management
├── services/
│   ├── cmc_service.py     # Handles fetching data from CoinMarketCap
│   └── data_service.py    # Cache and database update logic
├── scheduler/
│   └── jobs.py            # Background job scheduler setup
├── router/
│   └── crypto_router.py   # API endpoints for serving data
├── main.py                # Entry point for FastAPI app
├── .env                   # Environment variables
└── requirements.txt       # Backend dependencies
```
Frontend
```
coin_client/
├── src/
│   ├── components/
│   │   ├── Navbar.js       # Navigation bar
│   │   └── CryptoTable.js  # Cryptocurrency table
│   ├── App.js              # Main React app
│   └── index.js            # React entry point
├── package.json            # Frontend dependencies
└── .env                    # Environment variables for React (if needed)
```
Future Enhancements
	1.	Frontend Features:
	•	Add search functionality to the table.
	•	Implement login functionality for user-specific features like portfolio tracking.
	•	Support charts for historical price trends.
	2.	Backend Features:
	•	Add endpoints for user account management.
	•	Extend the database schema to support user portfolios.
	•	Introduce machine learning models for crypto health analysis.
	3.	Deployment:
	•	Containerize the app with Docker.
	•	Deploy the backend on AWS (e.g., ECS or Lambda) and the frontend on a static hosting service (e.g., S3 + CloudFront).

License

This project is licensed under the MIT License.
