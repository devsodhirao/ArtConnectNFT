from app import app
from blockchain_simulator import blockchain_simulator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Test blockchain connection
    try:
        network_id = blockchain_simulator.get_network_id()
        latest_block = blockchain_simulator.get_latest_block()
        if network_id:
            logger.info(f"Connected to blockchain network. Network ID: {network_id}")
        if latest_block:
            logger.info(f"Latest block number: {latest_block['number']}")
        else:
            logger.warning("Failed to retrieve latest block")
    except Exception as e:
        logger.error(f"Failed to connect to blockchain: {str(e)}")

    # Start the Flask application
    app.run(host="0.0.0.0", port=5000)
