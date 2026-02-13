"""
ScaleDown API Client for Context Compression
"""
import requests
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class ScaleDownClient:
    """Client for interacting with ScaleDown API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('SCALEDOWN_API_KEY')
        self.base_url = "https://api.scaledown.xyz"
        self.enabled = bool(self.api_key)
        
    def compress_prompt(self, text: str, context: str = "") -> dict:
        """
        Compress text using ScaleDown API
        
        Args:
            text: Main prompt/query to compress
            context: Optional context or instructions
            
        Returns:
            dict with 'compressed_text', 'original_tokens', 'compressed_tokens'
        """
        if not self.enabled:
            return self._fallback_response(text)
        
        try:
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            # Prepare context and prompt for ScaleDown
            # We must put the content we want compressed into the 'context' field
            # The 'prompt' field is used to guide the compression
            
            payload_context = text  # Inventory data goes here
            
            # Use provided context or generic instruction as the prompt
            payload_prompt = context if context else "Analyze this inventory data for restocking and optimization."
            
            # Ensure prompt is not empty
            if not payload_prompt or len(payload_prompt.strip()) < 5:
                payload_prompt = "Analyze this data."
            
            # Ensure text is not empty and has minimum length
            if not text or len(text.strip()) < 10:
                return self._fallback_response(text, error="Text too short for compression")
            
            payload = {
                'context': payload_context,
                'prompt': payload_prompt,
                'scaledown': {
                    'rate': 'auto'
                }
            }
            
            response = requests.post(
                f'{self.base_url}/compress/raw/',
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('successful'):
                    # Extract from results object safely
                    results = data.get('results', {})
                    if isinstance(results, list):
                        if results:
                            results = results[0]
                        else:
                            # Empty list case
                            results = {}
                    
                    # Get compressed text, defaulting to original if missing
                    compressed_text = results.get('compressed_prompt', text)
                    
                    # Extract token counts
                    original_tokens = results.get('original_prompt_tokens')
                    compressed_tokens = results.get('compressed_prompt_tokens')
                    
                    # Fallback to word count if tokens still not provided
                    if original_tokens is None:
                        original_tokens = len(text.split())
                    if compressed_tokens is None:
                        compressed_tokens = len(compressed_text.split())
                    
                    # Get compression ratio
                    compression_ratio = results.get('compression_ratio', 0)
                    if compression_ratio == 0:
                        # Try metadata as fallback
                        metadata = data.get('request_metadata', {})
                        compression_ratio = metadata.get('average_compression_ratio', 0)
                    
                    return {
                        'compressed_text': compressed_text,
                        'original_tokens': original_tokens,
                        'compressed_tokens': compressed_tokens,
                        'success': True,
                        'latency_ms': data.get('latency_ms', 0),
                        'compression_ratio': compression_ratio
                    }
                else:
                    return self._fallback_response(text, error=f"Compression failed. API response: {str(data)[:200]}")
            else:
                return self._fallback_response(text, error=f"API Error {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            return self._fallback_response(text, error=f"Network Error: {str(e)}")
        except Exception as e:
            return self._fallback_response(text, error=f"Unexpected Error: {str(e)}")
    
    def _fallback_response(self, text: str, error: Optional[str] = None) -> dict:
        """Return original text when compression fails"""
        token_count = len(text.split())
        
        return {
            'compressed_text': text,
            'original_tokens': token_count,
            'compressed_tokens': token_count,
            'success': False,
            'error': error or 'ScaleDown API not configured'
        }
    
    def get_stats(self, result: dict) -> str:
        """Format compression statistics"""
        if result['success']:
            # Use API's compression ratio if available (more accurate)
            if 'compression_ratio' in result and result['compression_ratio'] > 0:
                reduction_pct = (1 - result['compression_ratio']) * 100
                return f"✅ Compressed: {result['original_tokens']} → {result['compressed_tokens']} tokens ({reduction_pct:.1f}% reduction)"
            else:
                # Fallback to calculated ratio
                ratio = (1 - result['compressed_tokens'] / result['original_tokens']) * 100
                return f"✅ Compressed: {result['original_tokens']} → {result['compressed_tokens']} tokens ({ratio:.1f}% reduction)"
        else:
            return f"No compression: {result.get('error', 'Unknown error')}"
