"""
Optional Groq API Enhancement Module
===================================
This module provides optional enhanced analysis using Groq API.
Your main project works 100% without this module.
"""
import os
import requests
from datetime import datetime
from typing import Dict, Optional

class GroqEnhancement:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq enhancement (optional)"""
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.available = bool(self.api_key)
    
    def is_available(self) -> bool:
        """Check if Groq enhancement is available"""
        return self.available
    
    def enhance_analysis(self, contract_text: str, analysis_type: str = "comprehensive") -> Optional[Dict]:
        """Provide enhanced analysis using Groq API (optional)"""
        if not self.available:
            return None
        
        prompts = {
            "comprehensive": """
            Analyze this contract comprehensively. Provide:
            1. Key contract terms summary
            2. Risk assessment (High/Medium/Low risks)
            3. Red flags or concerning clauses
            4. Recommendations for negotiation
            5. Compliance considerations
            
            Contract:
            {contract_text}
            """,
            
            "risk_assessment": """
            Perform a detailed risk assessment of this contract. Identify:
            1. High-risk clauses that could cause significant harm
            2. Medium-risk terms that need attention
            3. Legal red flags or unusual provisions
            4. Financial risks and exposure
            5. Operational risks and constraints
            
            Contract:
            {contract_text}
            """,
            
            "app_specific": """
            This appears to be an app or software agreement. Analyze specifically:
            1. Data privacy and user rights
            2. App permissions and device access
            3. Content ownership and licensing
            4. Subscription and billing terms
            5. Platform-specific risks (iOS/Android)
            6. GDPR/CCPA compliance issues
            
            Contract:
            {contract_text}
            """,
            
            "simple_summary": """
            Please provide a simple, easy-to-understand summary of this contract in plain English.
            
            Focus on:
            1. What type of contract this is
            2. Key terms a normal person should know about
            3. Main risks or concerns to be aware of
            4. Important clauses to pay attention to
            5. Overall recommendation (favorable/unfavorable/neutral)
            
            Keep it conversational and simple, like explaining to a friend who has no legal background.
            
            Contract:
            {contract_text}
            """,
            
            "risk_highlighting": """
            Analyze this contract and identify specific clauses that represent different risk levels. 
            
            Please provide a simple analysis in this format:
            
            HIGH RISK CLAUSES:
            - [specific clause text] - [why this is high risk]
            
            MEDIUM RISK CLAUSES:
            - [specific clause text] - [why this is medium risk]
            
            LOW RISK/SAFE CLAUSES:
            - [specific clause text] - [why this is safe/good]
            
            Focus on:
            - Liability limitations (high risk if unlimited, low risk if limited)
            - Termination clauses (high risk if difficult, low risk if reasonable)
            - Payment terms (medium risk if unclear, low risk if clear)
            - Data handling (high risk if unlimited collection, low risk if limited)
            - Warranty disclaimers (medium to high risk)
            
            Contract:
            {contract_text}
            """
        }
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Try multiple models with fallback
            models_to_try = [
                "llama3-8b-8192",           # Fast and available
                "mixtral-8x7b-32768",       # Backup option
                "llama3-70b-8192",          # Powerful but might be busy
                "gemma-7b-it"               # Another fallback
            ]
            
            for model in models_to_try:
                try:
                    payload = {
                        "model": model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an expert contract attorney with specialization in technology agreements, app terms of service, and risk assessment. Provide clear, accurate, and practical analysis."
                            },
                            {
                                "role": "user",
                                "content": prompts[analysis_type].format(contract_text=contract_text[:4000])
                            }
                        ],
                        "temperature": 0.1,
                        "max_tokens": 2000
                    }
                    
                    print(f"🤖 Trying Groq model: {model}")
                    response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"✅ Success with model: {model}")
                        return {
                            "analysis": result["choices"][0]["message"]["content"],
                            "model": model,
                            "timestamp": datetime.now().isoformat(),
                            "enhanced": True
                        }
                    elif response.status_code == 429:
                        print(f"⚠️ Model {model} is busy (429), trying next...")
                        continue
                    elif response.status_code == 503:
                        print(f"⚠️ Model {model} unavailable (503), trying next...")
                        continue
                    else:
                        print(f"⚠️ Model {model} failed with status {response.status_code}, trying next...")
                        continue
                        
                except requests.exceptions.Timeout:
                    print(f"⏰ Model {model} timed out, trying next...")
                    continue
                except Exception as e:
                    print(f"❌ Model {model} error: {str(e)}, trying next...")
                    continue
            
            print("❌ All Groq models are currently busy or unavailable")
            return None
                
        except Exception as e:
            print(f"Groq enhancement failed (optional): {str(e)}")
            return None
    
    def enhance_recommendations(self, risk_assessment: Dict, contract_type: str) -> list:
        """Generate enhanced recommendations (optional)"""
        if not self.available:
            return []
        
        # This could call Groq for enhanced recommendations
        # For now, return empty to keep it optional
        return []

# Global instance (optional)
groq_enhancer = GroqEnhancement()
