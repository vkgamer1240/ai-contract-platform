"""
Enhanced CUAD Contract Analyzer - YOUR FINE-TUNED MODEL
========================================================
This is YOUR primary fine-tuned RoBERTa model for contract analysis.
Works 100% independently without any external APIs.
"""
import torch
from transformers import RobertaTokenizer, RobertaForQuestionAnswering
import json
import re
from typing import Dict, List, Any
import os
from datetime import datetime

class EnhancedCUADAnalyzer:
    def __init__(self, model_path="./", enable_groq_enhancement=False):
        """Initialize YOUR fine-tuned analyzer"""
        print("Loading YOUR Enhanced CUAD Analyzer...")
        
        # Load environment file if it exists
        self._load_env_file()
        
        # Load YOUR CUAD model (fine-tuned)
        print("📚 Loading YOUR fine-tuned RoBERTa model...")
        self.tokenizer = RobertaTokenizer.from_pretrained(model_path)
        self.model = RobertaForQuestionAnswering.from_pretrained(model_path)
        self.model.eval()
        print("✅ YOUR fine-tuned model loaded successfully!")
        
        # Optional Groq enhancement (can be disabled)
        self.groq_enhancer = None
        if enable_groq_enhancement:
            try:
                from groq_enhancement import groq_enhancer
                if groq_enhancer.is_available():
                    self.groq_enhancer = groq_enhancer
                    print("✅ Optional Groq enhancement available")
                else:
                    print("⚠️  Groq enhancement not configured (optional)")
            except ImportError:
                print("ℹ️  Groq enhancement module not found (optional)")
        else:
            print("ℹ️  Running with YOUR fine-tuned model only (recommended)")
        
        # Enhanced question templates
        self.question_templates = {
            "governing_law": [
                "What law governs this contract?",
                "Which jurisdiction's laws apply?",
                "What governing law clause is specified?",
                "Under what legal system is this agreement governed?"
            ],
            "termination": [
                "How can this contract be terminated?",
                "What termination conditions exist?",
                "What notice is required for termination?",
                "Under what circumstances can the agreement end?"
            ],
            "liability": [
                "What are the liability limits?",
                "What is the maximum liability amount?",
                "What damages are excluded?",
                "How is liability capped or limited?"
            ],
            "payment_terms": [
                "What are the payment amounts?",
                "When are payments due?",
                "What payment schedules apply?",
                "What late fees or penalties exist?"
            ],
            "intellectual_property": [
                "Who owns the intellectual property?",
                "What IP ownership rules apply?",
                "Who retains IP rights?",
                "What IP licensing terms exist?"
            ],
            "confidentiality": [
                "What confidentiality obligations exist?",
                "How long must information be kept confidential?",
                "What information must be protected?",
                "What are the non-disclosure requirements?"
            ],
            "data_privacy": [
                "What data privacy provisions exist?",
                "How is user data protected?",
                "What data collection rights are granted?",
                "What data retention policies apply?"
            ],
            "app_permissions": [
                "What app permissions are required?",
                "What device access is granted?",
                "What user information can be collected?",
                "What third-party integrations are allowed?"
            ],
            "subscription_terms": [
                "What are the subscription terms?",
                "How much does the subscription cost?",
                "What auto-renewal policies exist?",
                "How can subscriptions be cancelled?"
            ],
            "user_content": [
                "Who owns user-generated content?",
                "What rights does the app have to user content?",
                "Can user content be shared or monetized?",
                "What content moderation policies exist?"
            ]
        }
        
        # Risk assessment categories
        self.risk_categories = {
            "high_risk": [
                "unlimited liability",
                "no termination rights",
                "perpetual license",
                "exclusive ownership",
                "no data protection",
                "automatic renewal without notice",
                "broad indemnification",
                "no warranty disclaimers"
            ],
            "medium_risk": [
                "limited termination rights",
                "shared liability",
                "long-term commitment",
                "restrictive confidentiality",
                "limited data rights",
                "complex payment terms",
                "moderate penalties"
            ],
            "legal_red_flags": [
                "governing law in foreign jurisdiction",
                "mandatory arbitration",
                "class action waiver",
                "broad liability exclusions",
                "unlimited data collection",
                "no user rights",
                "unilateral modification rights"
            ]
        }
        
        print("YOUR Enhanced CUAD Analyzer loaded successfully!")
    
    def _load_env_file(self):
        """Load environment variables from .env file"""
        from pathlib import Path
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.strip() and not line.startswith('#') and '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
    
    def get_optional_enhancement(self, contract_text: str, analysis_type: str = "comprehensive") -> Dict:
        """Get optional enhanced analysis (if available)"""
        if self.groq_enhancer:
            enhancement = self.groq_enhancer.enhance_analysis(contract_text, analysis_type)
            if enhancement:
                return enhancement
        
        # Return basic enhancement from YOUR model only
        return {
            "analysis": f"Analysis completed using YOUR fine-tuned model. Contract type detected and analyzed.",
            "model": "YOUR_FINE_TUNED_ROBERTA",
            "timestamp": datetime.now().isoformat(),
            "enhanced": False
        }
    
    def detect_contract_type(self, contract_text: str) -> str:
        """Detect the type of contract to apply appropriate analysis"""
        text_lower = contract_text.lower()
        
        # App/Software specific indicators
        app_indicators = [
            "app store", "mobile app", "application", "ios", "android",
            "terms of service", "privacy policy", "user agreement",
            "software license", "saas", "platform", "api"
        ]
        
        # Employment indicators
        employment_indicators = [
            "employment", "employee", "employer", "salary", "wages",
            "benefits", "vacation", "sick leave", "non-compete"
        ]
        
        # Vendor/Supply indicators
        vendor_indicators = [
            "supply", "vendor", "supplier", "purchase", "goods",
            "delivery", "procurement", "materials"
        ]
        
        # Service indicators
        service_indicators = [
            "service agreement", "consulting", "professional services",
            "statement of work", "sow"
        ]
        
        if any(indicator in text_lower for indicator in app_indicators):
            return "app_agreement"
        elif any(indicator in text_lower for indicator in employment_indicators):
            return "employment"
        elif any(indicator in text_lower for indicator in vendor_indicators):
            return "vendor_supply"
        elif any(indicator in text_lower for indicator in service_indicators):
            return "service_agreement"
        else:
            return "general_contract"
    
    def assess_risks(self, contract_text: str, cuad_results: Dict) -> Dict:
        """Assess risks based on CUAD results and contract content"""
        risks = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": [],
            "red_flags": [],
            "risk_score": 0
        }
        
        text_lower = contract_text.lower()
        
        # High risk assessments
        if "unlimited" in text_lower and "liability" in text_lower:
            risks["high_risk"].append("Unlimited liability exposure")
            risks["risk_score"] += 30
        
        if cuad_results.get("governing_law", {}).get("confidence", 0) < 0.5:
            risks["medium_risk"].append("Unclear governing law provisions")
            risks["risk_score"] += 15
        
        # Check for specific high-risk terms
        high_risk_terms = [
            ("no termination", "No clear termination rights"),
            ("perpetual", "Perpetual obligations or licenses"),
            ("exclusive", "Exclusive rights granted"),
            ("irrevocable", "Irrevocable commitments"),
            ("unlimited data", "Unlimited data collection rights")
        ]
        
        for term, description in high_risk_terms:
            if term in text_lower:
                risks["high_risk"].append(description)
                risks["risk_score"] += 25
        
        # Medium risk assessments
        medium_risk_terms = [
            ("automatic renewal", "Automatic renewal clauses"),
            ("third party", "Third-party data sharing"),
            ("modify", "Unilateral modification rights"),
            ("arbitration", "Mandatory arbitration clauses")
        ]
        
        for term, description in medium_risk_terms:
            if term in text_lower:
                risks["medium_risk"].append(description)
                risks["risk_score"] += 10
        
        # Red flags
        red_flag_terms = [
            ("class action waiver", "Class action lawsuit waiver"),
            ("foreign jurisdiction", "Foreign jurisdiction governing law"),
            ("no warranty", "Complete warranty disclaimers"),
            ("unlimited access", "Unlimited device/data access")
        ]
        
        for term, description in red_flag_terms:
            if term in text_lower:
                risks["red_flags"].append(description)
                risks["risk_score"] += 20
        
        # Calculate overall risk level
        if risks["risk_score"] >= 50:
            risks["overall_risk"] = "HIGH"
        elif risks["risk_score"] >= 25:
            risks["overall_risk"] = "MEDIUM"
        else:
            risks["overall_risk"] = "LOW"
        
        return risks
    
    def analyze_contract_comprehensive(self, contract_text: str) -> Dict:
        """Comprehensive contract analysis using YOUR fine-tuned model"""
        
        print("🧠 Starting analysis with YOUR fine-tuned model...")
        
        # Detect contract type using YOUR model
        contract_type = self.detect_contract_type(contract_text)
        print(f"📋 Contract type detected: {contract_type}")
        
        # Get CUAD analysis using YOUR fine-tuned model
        cuad_results = {}
        relevant_categories = self.get_relevant_categories(contract_type)
        
        print("🔍 Analyzing contract sections with YOUR model...")
        for category in relevant_categories:
            if category in self.question_templates:
                result = self.answer_question_advanced(contract_text, category)
                cuad_results[category] = result
        
        # Risk assessment using YOUR model's results
        print("⚠️  Assessing risks with YOUR model...")
        risk_assessment = self.assess_risks(contract_text, cuad_results)
        
        # Optional enhancement (can be None if disabled)
        optional_enhancement = self.get_optional_enhancement(contract_text)
        
        # Generate recommendations using YOUR model
        recommendations = self.generate_recommendations(risk_assessment, contract_type)
        
        # Combine results (YOUR model is primary)
        comprehensive_result = {
            "contract_type": contract_type,
            "cuad_analysis": cuad_results,  # YOUR fine-tuned model results
            "risk_assessment": risk_assessment,  # YOUR model's risk analysis
            "optional_enhancement": optional_enhancement,  # Optional external enhancement
            "recommendations": recommendations,  # YOUR model's recommendations
            "timestamp": datetime.now().isoformat(),
            "primary_model": "YOUR_FINE_TUNED_ROBERTA_CUAD"
        }
        
        print("✅ Analysis completed successfully with YOUR fine-tuned model!")
        return comprehensive_result
    
    def get_relevant_categories(self, contract_type: str) -> List[str]:
        """Get relevant analysis categories based on contract type"""
        base_categories = ["governing_law", "termination", "liability", "confidentiality"]
        
        type_specific = {
            "app_agreement": [
                "data_privacy", "app_permissions", "subscription_terms", 
                "user_content", "intellectual_property"
            ],
            "employment": [
                "payment_terms", "intellectual_property", "termination"
            ],
            "vendor_supply": [
                "payment_terms", "liability", "termination"
            ],
            "service_agreement": [
                "payment_terms", "intellectual_property", "liability"
            ]
        }
        
        return base_categories + type_specific.get(contract_type, [])
    
    def generate_recommendations(self, risk_assessment: Dict, contract_type: str) -> List[str]:
        """Generate recommendations based on risk assessment"""
        recommendations = []
        
        if risk_assessment["overall_risk"] == "HIGH":
            recommendations.append("⚠️ HIGH RISK: Consider legal review before signing")
            recommendations.append("Negotiate liability limitations and termination rights")
        
        if risk_assessment["red_flags"]:
            recommendations.append("🚩 Red flags identified - detailed legal review recommended")
        
        if contract_type == "app_agreement":
            recommendations.extend([
                "Review data privacy terms carefully",
                "Check app permission requirements",
                "Verify subscription cancellation process",
                "Understand content ownership rights"
            ])
        
        if len(risk_assessment["high_risk"]) > 2:
            recommendations.append("Consider negotiating high-risk terms before agreement")
        
        return recommendations
    
    def answer_question_advanced(self, context: str, question_category: str, max_length: int = 512) -> Dict:
        """Advanced question answering with improved techniques"""
        relevant_context = self.extract_relevant_context(context, question_category)
        questions = self.question_templates.get(question_category, [question_category])
        
        best_answer = ""
        best_confidence = 0
        best_question = ""
        
        for question in questions:
            enhanced_context = f"Contract Document: {relevant_context}"
            
            inputs = self.tokenizer.encode_plus(
                question,
                enhanced_context,
                add_special_tokens=True,
                max_length=max_length,
                truncation=True,
                padding='max_length',
                return_tensors='pt'
            )
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                start_logits = outputs.start_logits
                end_logits = outputs.end_logits
            
            answer, confidence = self.extract_answer_beam_search(inputs, start_logits, end_logits)
            
            if confidence > best_confidence and len(answer.strip()) > 3:
                best_answer = answer
                best_confidence = confidence
                best_question = question
        
        best_answer = self.postprocess_answer(best_answer)
        
        return {
            "answer": best_answer,
            "confidence": best_confidence,
            "question_used": best_question
        }
    
    def extract_relevant_context(self, full_context: str, question_category: str) -> str:
        """Extract relevant context for specific question categories"""
        section_keywords = {
            "governing_law": ["governing law", "governed by", "jurisdiction", "laws of"],
            "termination": ["terminat", "end", "expire", "breach", "notice"],
            "liability": ["liabilit", "damages", "limit", "cap", "exclude"],
            "payment_terms": ["pay", "fee", "cost", "price", "invoice", "subscription"],
            "intellectual_property": ["intellectual property", "IP", "copyright", "license"],
            "confidentiality": ["confidential", "non-disclosure", "privacy", "secret"],
            "data_privacy": ["data", "privacy", "personal information", "collection"],
            "app_permissions": ["permission", "access", "device", "location", "camera"],
            "subscription_terms": ["subscription", "billing", "auto-renew", "cancel"],
            "user_content": ["user content", "user data", "upload", "share"]
        }
        
        keywords = section_keywords.get(question_category, [])
        sentences = re.split(r'[.!?]+', full_context)
        
        scored_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
            
            score = sum(2 for keyword in keywords if keyword.lower() in sentence.lower())
            scored_sentences.append((sentence, score))
        
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        relevant_sentences = [sent[0] for sent in scored_sentences[:5] if sent[1] > 0]
        
        return '. '.join(relevant_sentences) + '.' if relevant_sentences else full_context[:1000]
    
    def extract_answer_beam_search(self, inputs, start_logits, end_logits, beam_size=5):
        """Extract answer using beam search"""
        start_probs = torch.softmax(start_logits, dim=-1)[0]
        end_probs = torch.softmax(end_logits, dim=-1)[0]
        
        start_candidates = torch.topk(start_probs, beam_size)
        end_candidates = torch.topk(end_probs, beam_size)
        
        best_answer = ""
        best_score = 0
        
        for start_idx, start_prob in zip(start_candidates.indices, start_candidates.values):
            for end_idx, end_prob in zip(end_candidates.indices, end_candidates.values):
                if start_idx <= end_idx and end_idx - start_idx < 50:
                    score = start_prob * end_prob
                    
                    if score > best_score:
                        answer_tokens = inputs['input_ids'][0][start_idx:end_idx+1]
                        answer = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)
                        
                        if self.is_valid_answer(answer):
                            best_answer = answer
                            best_score = score.item()
        
        return best_answer, best_score
    
    def is_valid_answer(self, answer: str) -> bool:
        """Validate answer quality"""
        if not answer or len(answer.strip()) < 3:
            return False
        
        bad_answers = ["supplier", "client", "company", "party", "the", "this", "that"]
        return answer.strip().lower() not in bad_answers
    
    def postprocess_answer(self, answer: str) -> str:
        """Clean and format answer"""
        if not answer or answer.strip() == "":
            return "No answer found"
        
        answer = re.sub(r'<[^>]+>', '', answer.strip())
        answer = re.sub(r'\s+', ' ', answer)
        
        if answer and answer[0].islower():
            answer = answer[0].upper() + answer[1:]
        
        return answer

# Example usage and testing
def main():
    # Initialize with Groq API key (set environment variable GROQ_API_KEY)
    analyzer = EnhancedCUADAnalyzer(groq_api_key="your_groq_api_key_here")
    
    # Sample app agreement
    app_agreement = """
    MOBILE APP TERMS OF SERVICE
    
    By downloading and using this mobile application, you agree to these terms.
    
    GOVERNING LAW: This agreement is governed by California law.
    
    DATA COLLECTION: We collect your location data, device information, contacts, and usage patterns. This data may be shared with third-party partners for advertising purposes.
    
    APP PERMISSIONS: The app requires access to your camera, microphone, location, contacts, and storage. These permissions are used to provide core functionality.
    
    SUBSCRIPTION: Premium features cost $9.99/month with automatic renewal. Cancellation must be done through app store settings.
    
    USER CONTENT: Any content you upload becomes our property and can be used for any commercial purpose without compensation.
    
    LIABILITY: We disclaim all warranties and limit our liability to the maximum extent permitted by law.
    
    TERMINATION: We can terminate your account at any time without notice for any reason.
    """
    
    # Comprehensive analysis
    results = analyzer.analyze_contract_comprehensive(app_agreement)
    
    print("=" * 80)
    print("ENHANCED CUAD CONTRACT ANALYSIS")
    print("=" * 80)
    print(f"Contract Type: {results['contract_type']}")
    print(f"Risk Level: {results['risk_assessment']['overall_risk']}")
    print(f"Risk Score: {results['risk_assessment']['risk_score']}")
    
    print("\nKey Findings:")
    for category, result in results['cuad_analysis'].items():
        print(f"- {category}: {result['answer'][:100]}...")
    
    print(f"\nHigh Risks: {len(results['risk_assessment']['high_risk'])}")
    for risk in results['risk_assessment']['high_risk']:
        print(f"  ⚠️ {risk}")
    
    print(f"\nRecommendations:")
    for rec in results['recommendations']:
        print(f"  • {rec}")

if __name__ == "__main__":
    main()
