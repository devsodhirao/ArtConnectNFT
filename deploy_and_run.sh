#!/bin/bash

# Load environment variables
set -a
if [ -f .env ]; then
    source .env
else
    echo "Warning: .env file not found. Using environment variables."
fi
set +a

# Check if required environment variables are set
if [ -z "$SKALE_ENDPOINT" ]; then
    echo "Error: SKALE_ENDPOINT is not set. Please set it as an environment variable."
    exit 1
fi

if [ -z "$PRIVATE_KEY" ]; then
    echo "Error: PRIVATE_KEY is not set. Please set it as an environment variable."
    exit 1
fi

# Deploy the smart contract
echo "Deploying the smart contract..."
npx hardhat run scripts/deploy.js --network skale

# Check if the deployment was successful
if [ ! -f "contract-address.txt" ]; then
    echo "Error: Contract deployment failed. contract-address.txt not found."
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
pip install -r requirements.txt

# Start the Flask server
echo "Starting the Flask server..."
python main.py
