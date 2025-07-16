"""
Advanced Flask web interface for CUAD contract analysis with prompt engineering
"""
from flask import Flask, render_template, request, jsonify
import torch
from transformers import RobertaTokenizer, RobertaForQuestionAnswering
import json
import re

app = Flask(__name__)

# Global advanced tester
advanced_tester = None

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
        sentences = re.split(r'[.!?]+', full_context)
        
        scored_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
                
            score = 0
            sentence_lower = sentence.lower()
            
            for keyword in keywords:
                if keyword.lower() in sentence_lower:
                    score += 2
            
            if any(header in sentence.upper() for header in ["GOVERNING LAW", "TERMINATION", "LIABILITY", "PAYMENT", "INTELLECTUAL PROPERTY", "CONFIDENTIALITY", "FORCE MAJEURE", "WARRANTY", "DISPUTE", "RENEWAL"]):
                score += 3
            
            scored_sentences.append((sentence, score))
        
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        relevant_sentences = [sent[0] for sent in scored_sentences[:5] if sent[1] > 0]
        
        if relevant_sentences:
            return '. '.join(relevant_sentences) + '.'
        else:
            return full_context[:1000]
    
    def answer_question_advanced(self, context, question_category, max_length=512):
        """Answer questions using advanced prompt engineering"""
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
    
    def extract_answer_beam_search(self, inputs, start_logits, end_logits, beam_size=5):
        """Extract answer using beam search approach"""
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
    
    def is_valid_answer(self, answer):
        """Check if the answer is valid"""
        if not answer or len(answer.strip()) < 3:
            return False
        
        bad_answers = ["supplier", "client", "company", "party", "the", "this", "that"]
        if answer.strip().lower() in bad_answers:
            return False
        
        if len(answer.split()) < 2 and not any(char.isdigit() for char in answer):
            if answer.strip().lower() not in ["arbitration", "court", "delaware", "california", "new york"]:
                return False
        
        return True
    
    def postprocess_answer(self, answer):
        """Enhanced answer post-processing"""
        if not answer or answer.strip() == "":
            return "No answer found"
        
        answer = answer.strip()
        answer = re.sub(r'<[^>]+>', '', answer)
        answer = re.sub(r'\s+', ' ', answer)
        answer = answer.replace(' ,', ',').replace(' .', '.')
        
        if answer and answer[0].islower():
            answer = answer[0].upper() + answer[1:]
        
        return answer
    
    def answer_single_question(self, context, question):
        """Answer a single custom question"""
        inputs = self.tokenizer.encode_plus(
            question,
            context,
            add_special_tokens=True,
            max_length=512,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            start_logits = outputs.start_logits
            end_logits = outputs.end_logits
        
        answer, confidence = self.extract_answer_beam_search(inputs, start_logits, end_logits)
        answer = self.postprocess_answer(answer)
        
        return {
            "answer": answer,
            "confidence": confidence
        }

def load_model():
    """Load the advanced model"""
    global advanced_tester
    advanced_tester = AdvancedCUADTester('./')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    contract_text = data.get('contract_text', '')
    question = data.get('question', '')
    
    if not contract_text or not question:
        return jsonify({'error': 'Both contract text and question are required'}), 400
    
    result = advanced_tester.answer_single_question(contract_text, question)
    return jsonify(result)

@app.route('/analyze_full', methods=['POST'])
def analyze_full():
    """Analyze contract with all common CUAD questions using advanced techniques"""
    data = request.json
    contract_text = data.get('contract_text', '')
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    # Use advanced question categories
    question_categories = [
        "governing_law", "termination", "liability", "payment_terms",
        "intellectual_property", "confidentiality", "force_majeure",
        "warranty", "dispute_resolution", "renewal"
    ]
    
    results = {}
    for category in question_categories:
        result = advanced_tester.answer_question_advanced(contract_text, category)
        results[category] = result
    
    return jsonify(results)

@app.route('/get_sample_contracts', methods=['GET'])
def get_sample_contracts():
    """Get sample contracts for testing"""
    samples = {
        "software": """SOFTWARE SERVICE AGREEMENT

This Software Service Agreement ("Agreement") is entered into on March 15, 2024, between TechCorp Inc., a Delaware corporation ("Provider"), and BusinessSolutions LLC, a California limited liability company ("Client").

GOVERNING LAW: This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles.

PAYMENT TERMS: Client agrees to pay Provider a monthly service fee of Five Thousand Dollars ($5,000), payable within thirty (30) days of receipt of invoice. Late payments shall incur a penalty of one and one-half percent (1.5%) per month.

TERMINATION: Either party may terminate this Agreement with sixty (60) days prior written notice. Provider may terminate immediately upon Client's material breach if such breach is not cured within fifteen (15) days of written notice.

INTELLECTUAL PROPERTY: All software, documentation, and related materials provided by Provider remain the exclusive property of Provider. Client receives only a limited, non-exclusive license to use the software.

LIABILITY LIMITATION: Provider's total liability shall not exceed the fees paid by Client in the twelve (12) months preceding the claim. Provider shall not be liable for any indirect, consequential, or punitive damages.

CONFIDENTIALITY: Both parties agree to maintain strict confidentiality of proprietary information for a period of five (5) years after termination.

WARRANTY: Provider warrants that the software will perform substantially in accordance with documentation for ninety (90) days.

FORCE MAJEURE: Neither party shall be liable for delays or failures due to circumstances beyond their reasonable control, including natural disasters, government actions, or network outages.

DISPUTE RESOLUTION: Any disputes shall first be addressed through good faith negotiations. If unresolved within thirty (30) days, disputes shall be settled through binding arbitration under AAA Commercial Rules in Delaware.

RENEWAL: This Agreement automatically renews for successive one-year terms unless either party provides ninety (90) days written notice of non-renewal.""",

        "employment": """EMPLOYMENT AGREEMENT

This Employment Agreement is made effective January 1, 2024, between DataTech Corporation ("Company") and Sarah Johnson ("Employee").

GOVERNING LAW: This Agreement shall be governed by the laws of New York State. Employee consents to jurisdiction in New York courts.

COMPENSATION: Employee shall receive an annual salary of $120,000, paid bi-weekly. Employee is eligible for an annual performance bonus of up to 20% of base salary.

TERMINATION: Company may terminate Employee at any time with or without cause. If terminated without cause, Employee shall receive two (2) weeks severance pay.

INTELLECTUAL PROPERTY: All inventions and works created during employment belong exclusively to Company.

CONFIDENTIALITY: Employee agrees to maintain confidentiality of all Company trade secrets indefinitely.

NON-COMPETE: For twelve (12) months after termination, Employee shall not work for direct competitors within the tri-state area.""",

        "vendor": """VENDOR SUPPLY AGREEMENT

This Supply Agreement is between Manufacturing Corp ("Buyer") and Industrial Supplies Inc ("Supplier"), effective April 1, 2024.

GOVERNING LAW: This Agreement shall be governed by the laws of Texas. All disputes shall be resolved in Harris County, Texas courts.

PAYMENT TERMS: Buyer shall pay within net 45 days of delivery. Payments delayed beyond 60 days incur 2% monthly late fees.

PRICING: Current unit price is $15.50 per component for quantities of 1,000+ units. Prices are firm for six (6) months.

TERMINATION: Either party may terminate with 120 days written notice. Immediate termination permitted for material breach.

LIABILITY: Supplier's liability is limited to replacement cost of defective goods. Neither party liable for consequential damages exceeding $100,000 annually.

CONFIDENTIALITY: All pricing and specifications are confidential for three (3) years post-termination."""
    }
    
    return jsonify(samples)

if __name__ == '__main__':
    load_model()
    app.run(debug=True, host='0.0.0.0', port=5000)
