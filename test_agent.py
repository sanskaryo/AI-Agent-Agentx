import subprocess
import time
import webbrowser
from src.agent.workflow import WebpageMaintenanceAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_test_server():
    """Start the test HTTP server."""
    server_process = subprocess.Popen(['python', 'serve_test.py'])
    time.sleep(2)  # Wait for server to start
    return server_process

def run_agent_test():
    """Run the agent test."""
    # Start test server
    server_process = start_test_server()
    
    try:
        # Initialize agent
        agent = WebpageMaintenanceAgent()
        
        # Test URL
        test_url = "http://localhost:8000/test_page.html"
        
        # Run the agent
        logger.info(f"Starting agent test with URL: {test_url}")
        result = agent.run(test_url)
        
        # Print results
        logger.info("Test Results:")
        logger.info(f"Status: {result.get('status')}")
        logger.info(f"Analysis: {result.get('analysis')}")
        logger.info(f"Plan: {result.get('plan')}")
        logger.info(f"Execution Steps: {result.get('execution_steps')}")
        logger.info(f"Verification: {result.get('verification')}")
        
        # Open test page in browser
        webbrowser.open(test_url)
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        # Clean up
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    run_agent_test() 