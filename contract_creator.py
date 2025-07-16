"""
Contract Creation Module using RoBERTa + Groq AI
==============================================
This module generates professional contracts using your fine-tuned RoBERTa model 
combined with Groq AI for natural language generation.
"""
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional

class ContractCreator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize contract creator with Groq API"""
        self.api_key = api_key or os.getenv('GROQ_API_KEY_CREATION') or os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.available = bool(self.api_key)
    
    def create_contract(self, contract_params: Dict) -> Dict:
        """Create a professional contract using RoBERTa analysis + Groq generation"""
        
        if not self.available:
            return {
                "success": False,
                "error": "Groq API not available for contract creation",
                "contract": None
            }
        
        try:
            # Extract parameters
            company_a = contract_params.get('company_a', 'Company A')
            company_b = contract_params.get('company_b', 'Company B')
            services = contract_params.get('services', 'professional services')
            duration = contract_params.get('duration', '12 months')
            payment_terms = contract_params.get('payment_terms', 'monthly payments')
            start_date = contract_params.get('start_date', 'upon signing')
            confidentiality_level = contract_params.get('confidentiality_level', 'standard')
            
            # Create comprehensive prompt for contract generation
            system_prompt = """You are a professional contract attorney with expertise in creating legally sound service agreements. Generate a comprehensive, professional contract that includes all necessary legal language and protections for both parties."""
            
            user_prompt = f"""
            Generate a professional SERVICE AGREEMENT contract between {company_a} and {company_b} for {services}.
            
            Contract Parameters:
            - Service Provider: {company_a}
            - Client: {company_b}
            - Services: {services}
            - Duration: {duration}
            - Payment Terms: {payment_terms}
            - Start Date: {start_date}
            - Confidentiality Level: {confidentiality_level}
            
            The contract MUST include these sections:
            1. **PARTIES** - Full identification of both parties
            2. **SCOPE OF SERVICES** - Detailed description of services to be provided
            3. **PAYMENT TERMS** - Clear payment schedule, amounts, and methods
            4. **DURATION & TERMINATION** - Contract length and termination conditions
            5. **CONFIDENTIALITY** - Non-disclosure and confidentiality provisions
            6. **INTELLECTUAL PROPERTY** - Ownership rights and licensing
            7. **LIABILITY & INDEMNIFICATION** - Limitation of liability clauses
            8. **GOVERNING LAW** - Jurisdiction and applicable law
            9. **DISPUTE RESOLUTION** - Mediation and arbitration procedures
            10. **GENERAL PROVISIONS** - Entire agreement, amendments, severability
            
            Format Requirements:
            - Use professional legal language
            - Include appropriate headings and numbering
            - Add signature blocks at the end
            - Ensure enforceability and mutual protection
            - Include standard boilerplate clauses
            
            Make it comprehensive but readable, legally sound but not overly complex.
            """
            
            # Try multiple models for contract generation
            models_to_try = [
                "llama3-70b-8192",      # Most capable for complex legal text
                "mixtral-8x7b-32768",   # Good alternative
                "llama3-8b-8192"        # Fallback option
            ]
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            for model in models_to_try:
                try:
                    payload = {
                        "model": model,
                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user", 
                                "content": user_prompt
                            }
                        ],
                        "temperature": 0.1,  # Low temperature for consistency
                        "max_tokens": 4000   # Long contracts need more tokens
                    }
                    
                    print(f"🤖 Generating contract with model: {model}")
                    response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        result = response.json()
                        contract_text = result["choices"][0]["message"]["content"]
                        
                        print(f"✅ Contract generated successfully with {model}")
                        
                        return {
                            "success": True,
                            "contract": contract_text,
                            "model_used": model,
                            "timestamp": datetime.now().isoformat(),
                            "parameters": contract_params,
                            "word_count": len(contract_text.split()),
                            "sections": self._extract_sections(contract_text)
                        }
                    elif response.status_code == 429:
                        print(f"⚠️ Model {model} is busy, trying next...")
                        continue
                    else:
                        print(f"⚠️ Model {model} failed with status {response.status_code}")
                        continue
                        
                except Exception as e:
                    print(f"❌ Error with model {model}: {str(e)}")
                    continue
            
            return {
                "success": False,
                "error": "All models are currently unavailable. Please try again later.",
                "contract": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Contract generation failed: {str(e)}",
                "contract": None
            }
    
    def _extract_sections(self, contract_text: str) -> list:
        """Extract main sections from the generated contract"""
        sections = []
        lines = contract_text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for section headers (usually numbered or all caps)
            if (line.isupper() and len(line) > 3) or \
               (line.startswith(tuple('123456789')) and '.' in line[:5]) or \
               line.startswith('**') and line.endswith('**'):
                sections.append(line.replace('**', '').strip())
        
        return sections[:10]  # Return first 10 sections found
    
    def analyze_contract_risks(self, contract_text: str) -> Dict:
        """Use RoBERTa model to analyze risks in the generated contract"""
        try:
            # Import the enhanced analyzer to analyze our own generated contract
            from enhanced_analyzer import enhanced_analyzer
            
            analysis = enhanced_analyzer.analyze_contract_comprehensive(contract_text)
            
            return {
                "risk_analysis": analysis.get('risk_assessment', {}),
                "cuad_analysis": analysis.get('cuad_analysis', {}),
                "contract_type": analysis.get('contract_type', 'service_agreement'),
                "recommendations": self._generate_contract_recommendations(analysis)
            }
        except Exception as e:
            print(f"Risk analysis failed: {str(e)}")
            return {
                "risk_analysis": {"error": "Risk analysis unavailable", "risk_score": 25, "overall_risk": "MEDIUM"},
                "recommendations": ["Review contract manually", "Consider legal consultation"]
            }
    
    def _generate_contract_recommendations(self, analysis: Dict) -> list:
        """Generate recommendations for contract improvement"""
        recommendations = []
        
        risk_assessment = analysis.get('risk_assessment', {})
        high_risks = risk_assessment.get('high_risk', [])
        medium_risks = risk_assessment.get('medium_risk', [])
        
        if len(high_risks) > 3:
            recommendations.append("Consider adding more liability protections")
        
        if len(medium_risks) > 5:
            recommendations.append("Review payment and termination terms")
            
        recommendations.extend([
            "Have contract reviewed by legal counsel",
            "Ensure compliance with local jurisdiction laws",
            "Consider adding dispute resolution mechanisms",
            "Review confidentiality terms with stakeholders"
        ])
        
        return recommendations[:5]  # Return top 5 recommendations
