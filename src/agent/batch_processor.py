from typing import List, Dict, Any
import asyncio
import aiohttp
import logging
from concurrent.futures import ThreadPoolExecutor
from src.agent.workflow import WebpageMaintenanceAgent
from src.agent.content_updater import ContentUpdater

logger = logging.getLogger(__name__)

class BatchProcessor:
    def __init__(self, max_workers: int = 5):
        self.agent = WebpageMaintenanceAgent()
        self.content_updater = ContentUpdater()
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def process_url(self, url: str) -> Dict[str, Any]:
        """Process a single URL asynchronously."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        return await self._process_content(url, html_content)
                    else:
                        return {"url": url, "status": "failed", "error": f"HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            return {"url": url, "status": "failed", "error": str(e)}

    async def _process_content(self, url: str, html_content: str) -> Dict[str, Any]:
        """Process webpage content."""
        try:
            # Run analysis
            analysis = await asyncio.get_event_loop().run_in_executor(
                self.executor, self.agent.analyze_page, url
            )

            # Check for content updates
            updates = await self._check_updates(analysis)
            if updates:
                html_content = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.content_updater.update_content, html_content, updates
                )

            return {
                "url": url,
                "status": "success",
                "analysis": analysis,
                "updates": updates
            }
        except Exception as e:
            logger.error(f"Error processing content for {url}: {str(e)}")
            return {"url": url, "status": "failed", "error": str(e)}

    async def _check_updates(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Check for content updates based on analysis."""
        updates = {}
        
        # Check for outdated prices
        if "outdated_prices" in analysis:
            price_data = await self._fetch_price_updates(analysis["outdated_prices"])
            if price_data:
                updates["prices"] = price_data

        # Check for missing content
        if "missing_content" in analysis:
            content_data = await self._generate_missing_content(analysis["missing_content"])
            if content_data:
                updates["content"] = content_data

        return updates

    async def _fetch_price_updates(self, outdated_prices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fetch updated prices from API."""
        try:
            # Example API endpoint - replace with actual endpoint
            api_endpoint = "https://api.example.com/prices"
            params = {
                "products": [p["product_id"] for p in outdated_prices]
            }
            
            data = await asyncio.get_event_loop().run_in_executor(
                self.executor, self.content_updater.fetch_updated_data, api_endpoint, params
            )
            
            return data if data else {}
        except Exception as e:
            logger.error(f"Error fetching price updates: {str(e)}")
            return {}

    async def _generate_missing_content(self, missing_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate missing content using LLM."""
        try:
            content_data = {}
            for item in missing_content:
                # Use LLM to generate content
                content = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.agent.llm.generate_content, item["description"]
                )
                if content:
                    content_data[item["id"]] = content
            return content_data
        except Exception as e:
            logger.error(f"Error generating missing content: {str(e)}")
            return {}

    async def process_batch(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Process a batch of URLs concurrently."""
        tasks = [self.process_url(url) for url in urls]
        return await asyncio.gather(*tasks)

    def close(self):
        """Clean up resources."""
        self.executor.shutdown(wait=True) 