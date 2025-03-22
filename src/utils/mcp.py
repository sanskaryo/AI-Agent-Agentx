import requests
from typing import Dict, Any, Optional
from ..config.settings import MCP_ENDPOINT, MCP_TIMEOUT

class MCPHandler:
    def __init__(self):
        self.endpoint = MCP_ENDPOINT
        self.timeout = MCP_TIMEOUT
        self.session = requests.Session()
    
    def secure_request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a secure request using MCP.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            path (str): API endpoint path
            data (dict, optional): Request data
            headers (dict, optional): Request headers
            
        Returns:
            dict: Response data
        """
        url = f"{self.endpoint}{path}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def get_seo_data(self, url: str) -> Dict[str, Any]:
        """Get SEO data for a URL."""
        return self.secure_request(
            method="GET",
            path="/seo",
            data={"url": url}
        )
    
    def get_performance_data(self, url: str) -> Dict[str, Any]:
        """Get performance data for a URL."""
        return self.secure_request(
            method="GET",
            path="/performance",
            data={"url": url}
        )
    
    def update_content(self, url: str, content: str) -> Dict[str, Any]:
        """Update webpage content."""
        return self.secure_request(
            method="POST",
            path="/content",
            data={
                "url": url,
                "content": content
            }
        )
    
    def validate_changes(self, url: str, changes: Dict[str, Any]) -> Dict[str, Any]:
        """Validate proposed changes."""
        return self.secure_request(
            method="POST",
            path="/validate",
            data={
                "url": url,
                "changes": changes
            }
        )
    
    def close(self):
        """Close the session."""
        self.session.close() 