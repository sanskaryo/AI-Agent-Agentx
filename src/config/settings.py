import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
API_KEY = os.getenv("API_KEY")

# Webpage Analysis Configuration
MAX_RETRIES = 3
TIMEOUT = 30  # seconds
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Monitoring Configuration
PROMETHEUS_PORT = 8000
GRAFANA_PORT = 3000

# MCP Configuration
MCP_ENDPOINT = os.getenv("MCP_ENDPOINT", "http://localhost:8080")
MCP_TIMEOUT = 60  # seconds

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 