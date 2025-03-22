from openai import OpenAI
from typing import Dict, Any
from src.config.settings import API_KEY

class LLMHandler:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)
        self.model = "gpt-4"  # or "gpt-3.5-turbo" for faster, cheaper option
        
    def generate_text(self, prompt: str, max_length: int = 500) -> str:
        """
        Generate text using OpenAI's GPT model.
        
        Args:
            prompt (str): Input prompt for text generation
            max_length (int): Maximum length of generated text
            
        Returns:
            str: Generated text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant specialized in webpage analysis and maintenance."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return ""
    
    def analyze_content(self, content: str) -> dict:
        """
        Analyze webpage content using GPT.
        
        Args:
            content (str): Webpage content to analyze
            
        Returns:
            dict: Analysis results including SEO score, readability, and issues
        """
        prompt = f"""Analyze the following webpage content and provide a detailed analysis:
        
        Content:
        {content}
        
        Please provide a JSON response with the following structure:
        {{
            "seo_score": <score 0-100>,
            "readability_score": <score 0-100>,
            "issues": ["issue1", "issue2", ...],
            "improvements": ["improvement1", "improvement2", ...]
        }}
        """
        
        try:
            analysis = self.generate_text(prompt)
            return self._parse_analysis(analysis)
        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            return {
                "seo_score": 0,
                "readability_score": 0,
                "issues": [],
                "improvements": []
            }
    
    def _parse_analysis(self, analysis: str) -> dict:
        """
        Parse the GPT analysis into a structured format.
        
        Args:
            analysis (str): Raw analysis text
            
        Returns:
            dict: Structured analysis results
        """
        try:
            import json
            # Try to parse as JSON first
            return json.loads(analysis)
        except:
            # Fallback to text parsing if JSON parsing fails
            return {
                "raw_analysis": analysis,
                "seo_score": self._extract_score(analysis, "SEO score"),
                "readability_score": self._extract_score(analysis, "Readability score"),
                "issues": self._extract_list(analysis, "issues found"),
                "improvements": self._extract_list(analysis, "improvements")
            }
    
    def _extract_score(self, text: str, keyword: str) -> int:
        """Extract numerical score from text."""
        try:
            import re
            pattern = f"{keyword}.*?(\\d+)"
            match = re.search(pattern, text)
            return int(match.group(1)) if match else 0
        except:
            return 0
    
    def _extract_list(self, text: str, keyword: str) -> list:
        """Extract list items from text."""
        try:
            import re
            pattern = f"{keyword}.*?([^\\n]+)"
            match = re.search(pattern, text)
            if match:
                items = match.group(1).split(",")
                return [item.strip() for item in items]
            return []
        except:
            return [] 