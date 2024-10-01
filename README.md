# Sepolia Faucet Application

## Description
This project is a simple Django REST API faucet application that allows users to request Sepolia ETH for free. The application features two main endpoints: one for funding a wallet with Sepolia ETH and another for retrieving transaction statistics. The project is containerized using Docker and Docker Compose for easy deployment and management.

## Endpoints

### 1. `POST /faucet/fund`
- **Purpose**: Send 0.0001 Sepolia ETH from a pre-configured wallet to a specified wallet address.
- **Payload**: Accepts a JSON payload containing the wallet address.

```json
{
  "ethereum_address": "0xYourEthereumAddress"
}
```

- **Rate Limiting**: Users cannot request funds more than once per configurable timeout (default is 1 minute) based on source IP or wallet address. If the rate limit is exceeded, an error message will be returned.
- **Response**:
  - On success: Returns a transaction ID.
  - On failure: Returns a descriptive error message.

### 2. `GET /faucet/stats`
- **Purpose**: Return the following statistics for the last 24 hours:
  - Number of successful transactions.
  - Number of failed transactions.

## Environment Variables (Required for the .env file)

To run the project successfully, the following environment variables must be defined in a `.env` file:

- `INFURA_URL`: The Infura API endpoint for connecting to the Ethereum network.
- `SENDER_ADDRESS`: The Ethereum address from which Sepolia ETH will be sent.
- `PRIVATE_KEY`: The private key of the sender's Ethereum address for signing transactions.

Example `.env` file:

```bash
INFURA_URL=https://sepolia.infura.io/v3/your-infura-project-id
SENDER_ADDRESS=0xYourSenderAddress
PRIVATE_KEY=your-private-key
```

## Setup and Installation

### Prerequisites
- Docker
- Docker Compose

### Step 1: Clone the Repository

```bash
git clone https://github.com/SuperCS92/faucet.git
cd sepolia-faucet
```

### Step 2: Create a `.env` File

Create a `.env` file in the root directory of the project with the following content:

```bash
INFURA_URL=https://sepolia.infura.io/v3/your-infura-project-id
SENDER_ADDRESS=0xYourSenderAddress
PRIVATE_KEY=your-private-key
```

### Step 3: Build and Run the Application with Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Run the application:
   ```bash
   docker-compose up
   ```

The application will be available at `http://localhost:8000`.

### Step 4: Testing the Endpoints

1. **Fund a wallet (POST /faucet/fund)**:
   - Send a POST request with the wallet address:
   ```bash
   curl -X POST http://localhost:8000/faucet/fund/ \
        -H "Content-Type: application/json" \
        -d '{"ethereum_address": "0xYourWalletAddress"}'
   ```

2. **Get transaction stats (GET /faucet/stats)**:
   - Retrieve statistics for the last 24 hours:
   ```bash
   curl -X GET http://localhost:8000/faucet/stats/
   ```

## Project Structure

```bash
faucet/
├── Dockerfile                # Dockerfile to build the app image
├── README.md                 # This README file
├── db.sqlite3                # SQLite database (ignored by Git)
├── docker-compose.yml        # Docker Compose configuration
├── faucet/                   # Original Django app folder
├── fund/                     # New Django app folder for the faucet functionality
├── manage.py                 # Django manage script
├── requirements.txt          # Python dependencies
└── .env    
```

## Requirements

- **Python**: 3.9 or higher
- **Django**: 4.x
- **Web3.py**: Used for interacting with the Ethereum blockchain

## Docker and Docker Compose

The application is fully dockerized for easy deployment. The provided `Dockerfile` builds the application, and `docker-compose.yml` manages both the app and its environment variables.

### Dockerfile

The `Dockerfile` sets up the Django app and installs all necessary dependencies. It exposes port 8000 for accessing the API.

### Docker Compose

The `docker-compose.yml` file configures the services needed to run the application. Environment variables are passed in from the `.env` file.

## Future Improvements

- Add more granular error handling for Ethereum transactions.
- Implement logging for better monitoring of transaction requests.
- Extend the rate-limiting functionality for more configurable options.

## License

This project is licensed under the MIT License.

