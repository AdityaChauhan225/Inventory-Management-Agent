"""
Ollama Agent for Inventory Analysis
"""
import os
from typing import Dict, Optional
from dotenv import load_dotenv
import ollama

load_dotenv()


class InventoryAgent:
    """AI Agent for inventory analysis using Ollama"""
    
    def __init__(self, model: Optional[str] = None):
        self.model = model or os.getenv('OLLAMA_MODEL', 'glm-5:cloud')
        self.base_url = os.getenv('OLLAMA_API_BASE', 'http://localhost:11434')
        
        # Configure ollama client
        os.environ['OLLAMA_HOST'] = self.base_url
        
    def analyze_inventory(self, data: str, user_question: Optional[str] = None) -> str:
        """
        Analyze inventory data and provide insights
        
        Args:
            data: Processed inventory data (compressed or raw)
            user_question: Optional specific question from user
            
        Returns:
            AI-generated analysis and recommendations
        """
        # Determine context based on data content
        context_focus = []
        if "sales" in data.lower() or "demand" in data.lower():
            context_focus.append("Analyze sales trends and demand patterns")
        if "stock" in data.lower() or "quantity" in data.lower():
            context_focus.append("Identify stockout risks and overstock situations")
        
        focus_str = "; ".join(context_focus) if context_focus else "Analyze inventory levels"

        # Build dynamic prompt
        system_prompt = f"""You are an expert inventory management analyst. 
{focus_str}.

Based on the provided data, generate a structured analysis including:
1. 🔴 CRITICAL ALERTS: Items needing immediate attention (low stock/high demand).
2. 🟡 WARNINGS: Potential future risks or slow-moving items.
3. 📈 DEMAND INSIGHTS: High performing products and trends.
4. 💡 OPTIMIZATION: Specific actionable recommendations.

Format your response with clear headings and bullet points. Be concise and data-driven."""

        user_prompt = f"INVENTORY DATA:\n{data}\n\n"
        if user_question:
            user_prompt += f"USER QUESTION: {user_question}\n\n"
        user_prompt += "Please provide your detailed analysis and recommendations:"
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ]
            )
            
            return response['message']['content']
            
        except Exception as e:
            error_msg = str(e)
            if "connection refused" in error_msg.lower():
                return "❌ Error: Could not connect to Ollama. As check if 'ollama serve' is running."
            elif "not found" in error_msg.lower():
                return f"❌ Error: Model '{self.model}' not found. Please run 'ollama pull {self.model}'."
            return f"❌ AI Analysis Error: {error_msg}"
    
    def generate_recommendations(self, analysis: str) -> Dict[str, list]:
        """
        Extract structured recommendations from analysis
        
        Returns:
            dict with 'critical', 'warnings', 'optimizations'
        """
        recommendations = {
            'critical': [],
            'warnings': [],
            'optimizations': []
        }
        
        lines = analysis.split('\n')
        current_section = None
        
        for line in lines:
            line_clean = line.strip()
            line_lower = line_clean.lower()
            
            # Skip empty lines
            if not line_clean:
                continue
                
            # Detect sections
            if 'critical' in line_lower and ('alert' in line_lower or 'attention' in line_lower):
                current_section = 'critical'
                continue
            elif 'warning' in line_lower:
                current_section = 'warnings'
                continue
            elif 'optimization' in line_lower or 'recommend' in line_lower:
                current_section = 'optimizations'
                continue
            elif 'demand' in line_lower or 'insight' in line_lower:
                current_section = None # Skip other sections for now
                continue
            
            # Extract content if in a section
            if current_section and (line_clean.startswith('-') or line_clean.startswith('*') or line_clean[0].isdigit()):
                # Remove bullet points and numbers
                clean_content = line_clean.lstrip('-*1234567890. ')
                if clean_content:
                    recommendations[current_section].append(clean_content)
        
        return recommendations
    
    def identify_high_demand(self, data: str) -> str:
        """Identify products with highest demand"""
        prompt = f"""Based on this inventory data, identify the top 5 products with highest demand.
        
{data}

List them in order with brief reasoning (1 line per item)."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'user', 'content': prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error identifying high demand items: {str(e)}"
