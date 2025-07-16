"""
Advanced CUAD model tester with sophisticated prompt engineering
"""
import torch
from transformers import RobertaTokenizer, RobertaForQuestionAnswering
import json
import re

class AdvancedCUADTester:
    def __init__(self, model_path="./"):
        """Initialize the model and tokenizer"""
        print("Loading CUAD model...")
        self.tokenizer = RobertaTokenizer.from_pretrained(model_path)
        self.model = RobertaForQuestionAnswering.from_pretrained(model_path)
        self.model.eval()
        print("Model loaded successfully!")
        
        # Advanced question templates with context-aware prompting
        self.question_templates = {
            "governing_law": [
                "What law governs this contract?",
                "Which state or country's laws apply to this agreement?",
                "Under what jurisdiction is this contract governed?",
                "What governing law clause is specified?"
            ],
            "termination": [
                "How can this contract be terminated?",
                "What are the termination conditions?",
                "Under what circumstances can the agreement end?",
                "What notice is required for termination?"
            ],
            "liability": [
                "What are the liability limits?",
                "How much liability is capped at?",
                "What damages are excluded?",
                "What is the maximum liability amount?"
            ],
            "payment_terms": [
                "What is the payment amount?",
                "When are payments due?",
                "What are the payment schedules?",
                "How much does the client pay?"
            ],
            "intellectual_property": [
                "Who owns the intellectual property?",
                "What are the IP ownership rules?",
                "Who retains rights to intellectual property?",
                "What IP provisions are included?"
            ],
            "confidentiality": [
                "How long must information be kept confidential?",
                "What confidentiality obligations exist?",
                "What information must be protected?",
                "What are the non-disclosure requirements?"
            ],
            "force_majeure": [
                "What events constitute force majeure?",
                "What circumstances excuse performance?",
                "What natural disasters are covered?",
                "What uncontrollable events are included?"
            ],
            "warranty": [
                "What warranty is provided?",
                "How long is the warranty period?",
                "What does the warranty cover?",
                "What warranty disclaimers exist?"
            ],
            "dispute_resolution": [
                "How are disputes resolved?",
                "What dispute resolution process is required?",
                "Must disputes go to arbitration or court?",
                "Where are disputes resolved?"
            ],
            "renewal": [
                "How does this contract renew?",
                "What are the renewal terms?",
                "Does the contract auto-renew?",
                "What notice is needed to prevent renewal?"
            ]
        }
    
    def extract_relevant_context(self, full_context, question_category):
        """Extract the most relevant part of the contract for the question"""
        # Define section keywords for each category
        section_keywords = {
            "governing_law": ["governing law", "governed by", "jurisdiction", "laws of", "state law"],
            "termination": ["terminat", "end", "expire", "breach", "notice"],
            "liability": ["liabilit", "damages", "limit", "cap", "exclude", "indemnif"],
            "payment_terms": ["pay", "fee", "cost", "price", "invoice", "billing"],
            "intellectual_property": ["intellectual property", "IP", "copyright", "patent", "trademark", "proprietary"],
            "confidentiality": ["confidential", "non-disclosure", "NDA", "proprietary", "secret"],
            "force_majeure": ["force majeure", "act of god", "natural disaster", "uncontrollable"],
            "warranty": ["warrant", "guarantee", "defect", "performance"],
            "dispute_resolution": ["dispute", "arbitration", "litigation", "court", "mediation"],
            "renewal": ["renew", "extend", "automatic", "term", "continuation"]
        }
        
        keywords = section_keywords.get(question_category, [])
        
        # Split context into sentences
        sentences = re.split(r'[.!?]+', full_context)
        
        # Score sentences based on keyword presence
        scored_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue
                
            score = 0
            sentence_lower = sentence.lower()
            
            # Score based on keyword matches
            for keyword in keywords:
                if keyword.lower() in sentence_lower:
                    score += 2
            
            # Bonus for section headers
            if any(header in sentence.upper() for header in ["GOVERNING LAW", "TERMINATION", "LIABILITY", "PAYMENT", "INTELLECTUAL PROPERTY", "CONFIDENTIALITY", "FORCE MAJEURE", "WARRANTY", "DISPUTE", "RENEWAL"]):
                score += 3
            
            scored_sentences.append((sentence, score))
        
        # Sort by score and take top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Combine top 3-5 sentences for context
        relevant_sentences = [sent[0] for sent in scored_sentences[:5] if sent[1] > 0]
        
        if relevant_sentences:
            return '. '.join(relevant_sentences) + '.'
        else:
            # Fallback to full context if no relevant sentences found
            return full_context[:1000]  # Limit to first 1000 chars
    
    def answer_question_advanced(self, context, question_category, max_length=512):
        """Answer questions using advanced prompt engineering"""
        
        # Get relevant context
        relevant_context = self.extract_relevant_context(context, question_category)
        
        # Try multiple question formulations
        questions = self.question_templates.get(question_category, [question_category])
        
        best_answer = ""
        best_confidence = 0
        best_result = None
        
        for question in questions:
            # Enhanced context with explicit instruction
            enhanced_context = f"Contract Document: {relevant_context}"
            
            # Tokenize inputs
            inputs = self.tokenizer.encode_plus(
                question,
                enhanced_context,
                add_special_tokens=True,
                max_length=max_length,
                truncation=True,
                padding='max_length',
                return_tensors='pt'
            )
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                start_logits = outputs.start_logits
                end_logits = outputs.end_logits
            
            # Use beam search for better answer extraction
            answer, confidence = self.extract_answer_beam_search(
                inputs, start_logits, end_logits
            )
            
            # Keep the best answer
            if confidence > best_confidence and len(answer.strip()) > 3:
                best_answer = answer
                best_confidence = confidence
                best_result = {
                    "question_used": question,
                    "context_used": enhanced_context[:200] + "..."
                }
        
        # Post-process the answer
        best_answer = self.postprocess_answer(best_answer)
        
        return {
            "answer": best_answer,
            "confidence": best_confidence,
            "best_question": best_result["question_used"] if best_result else questions[0],
            "context_snippet": best_result["context_used"] if best_result else ""
        }
    
    def extract_answer_beam_search(self, inputs, start_logits, end_logits, beam_size=5):
        """Extract answer using beam search approach"""
        start_probs = torch.softmax(start_logits, dim=-1)[0]
        end_probs = torch.softmax(end_logits, dim=-1)[0]
        
        # Get top candidates
        start_candidates = torch.topk(start_probs, beam_size)
        end_candidates = torch.topk(end_probs, beam_size)
        
        best_answer = ""
        best_score = 0
        
        for start_idx, start_prob in zip(start_candidates.indices, start_candidates.values):
            for end_idx, end_prob in zip(end_candidates.indices, end_candidates.values):
                if start_idx <= end_idx and end_idx - start_idx < 50:  # Reasonable length
                    score = start_prob * end_prob
                    
                    if score > best_score:
                        answer_tokens = inputs['input_ids'][0][start_idx:end_idx+1]
                        answer = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)
                        
                        # Filter out obviously bad answers
                        if self.is_valid_answer(answer):
                            best_answer = answer
                            best_score = score.item()
        
        return best_answer, best_score
    
    def is_valid_answer(self, answer):
        """Check if the answer is valid"""
        if not answer or len(answer.strip()) < 3:
            return False
        
        # Remove common bad answers
        bad_answers = ["supplier", "client", "company", "party", "the", "this", "that"]
        if answer.strip().lower() in bad_answers:
            return False
        
        # Check for meaningful content
        if len(answer.split()) < 2 and not any(char.isdigit() for char in answer):
            if answer.strip().lower() not in ["arbitration", "court", "delaware", "california", "new york"]:
                return False
        
        return True
    
    def postprocess_answer(self, answer):
        """Enhanced answer post-processing"""
        if not answer or answer.strip() == "":
            return "No answer found"
        
        # Clean up the answer
        answer = answer.strip()
        
        # Remove artifacts
        answer = re.sub(r'<[^>]+>', '', answer)  # Remove any HTML-like tags
        answer = re.sub(r'\s+', ' ', answer)     # Normalize whitespace
        
        # Fix common formatting issues
        answer = answer.replace(' ,', ',').replace(' .', '.')
        
        # If answer starts with lowercase, try to capitalize
        if answer and answer[0].islower():
            answer = answer[0].upper() + answer[1:]
        
        return answer
    
    def analyze_contract_advanced(self, contract_text):
        """Analyze contract with advanced techniques"""
        print("Analyzing contract with advanced prompt engineering...")
        
        results = {}
        for category in self.question_templates.keys():
            print(f"Processing {category}...")
            result = self.answer_question_advanced(contract_text, category)
            results[category] = result
        
        return results
    
    def display_results(self, results):
        """Display results in a formatted way"""
        print("\n" + "="*80)
        print("ADVANCED CUAD CONTRACT ANALYSIS RESULTS")
        print("="*80)
        
        for category, result in results.items():
            print(f"\n🔍 {category.upper().replace('_', ' ')}")
            print(f"   Question: {result['best_question']}")
            print(f"   Answer: {result['answer']}")
            print(f"   Confidence: {result['confidence']:.3f}")
            if result['confidence'] < 0.5:
                print(f"   ⚠️  Low confidence - answer may be unreliable")
            print("-" * 70)

# Test with sample contract
def main():
    tester = AdvancedCUADTester()
    
    # Enhanced sample contract
    sample_contract = """
    SOFTWARE SERVICE AGREEMENT
    
    This Software Service Agreement is entered into between TechCorp Inc. and Client Corp.
    
    GOVERNING LAW: This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware.
    
    PAYMENT TERMS: Client agrees to pay Provider a monthly service fee of $5,000, payable within thirty (30) days of receipt of invoice. Late payments shall incur a penalty of 1.5% per month.
    
    TERMINATION: Either party may terminate this Agreement with sixty (60) days prior written notice. Provider may terminate immediately upon Client's material breach if such breach is not cured within fifteen (15) days of written notice.
    
    INTELLECTUAL PROPERTY: All software, documentation, and related materials provided by Provider remain the exclusive property of Provider. Client receives only a limited, non-exclusive license to use the software.
    
    LIABILITY LIMITATION: Provider's total liability shall not exceed the fees paid by Client in the twelve (12) months preceding the claim. Provider shall not be liable for any indirect, consequential, or punitive damages.
    
    CONFIDENTIALITY: Both parties agree to maintain strict confidentiality of proprietary information for a period of five (5) years after termination.
    
    WARRANTY: Provider warrants that the software will perform substantially in accordance with documentation for ninety (90) days.
    
    FORCE MAJEURE: Neither party shall be liable for delays or failures due to circumstances beyond their reasonable control, including natural disasters, government actions, or network outages.
    
    DISPUTE RESOLUTION: Any disputes shall first be addressed through good faith negotiations. If unresolved within thirty (30) days, disputes shall be settled through binding arbitration under AAA Commercial Rules in Delaware.
    
    RENEWAL: This Agreement automatically renews for successive one-year terms unless either party provides ninety (90) days written notice of non-renewal.
    """
    
    results = tester.analyze_contract_advanced(sample_contract)
    tester.display_results(results)

if __name__ == "__main__":
    main()
