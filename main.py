import argparse
import logging
from src.agent.workflow import WebpageMaintenanceAgent
from src.config.settings import LOG_LEVEL, LOG_FORMAT

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AI Webpage Maintenance Agent')
    parser.add_argument('url', help='URL of the webpage to maintain')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize and run the agent
        agent = WebpageMaintenanceAgent()
        logger.info(f"Starting webpage maintenance for URL: {args.url}")
        
        result = agent.run(args.url)
        
        if result.get('status') == 'failed':
            logger.error(f"Maintenance failed: {result.get('error')}")
        else:
            logger.info("Maintenance completed successfully")
            logger.debug(f"Results: {result}")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
