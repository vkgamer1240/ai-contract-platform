"""
Test script for fine-tuned RoBERTa model on CUAD dataset
"""
import torch
from transformers import RobertaTokenizer, RobertaForQuestionAnswering
import json

class CUADModelTester:
    def __init__(self, model_path="./"):
        """Initialize the model and tokenizer"""
        self.tokenizer = RobertaTokenizer.from_pretrained(model_path)
        self.model = RobertaForQuestionAnswering.from_pretrained(model_path)
        self.model.eval()
        
        # Enhanced CUAD questions with better prompt engineering
        self.cuad_questions = {
            "governing_law": "Which jurisdiction's laws govern this agreement?",
            "termination": "Under what conditions can this agreement be terminated?",
            "liability": "What are the liability limitations and caps in this agreement?",
            "payment_terms": "What are the specific payment amounts, schedules, and terms?",
            "intellectual_property": "Who owns the intellectual property rights?",
            "confidentiality": "What confidential information must be protected and for how long?",
            "force_majeure": "What events excuse performance under force majeure?",
            "warranty": "What warranties are provided and for what duration?",
            "dispute_resolution": "How must disputes be resolved under this agreement?",
            "renewal": "How does this agreement renew or extend?"
        }
    
    def answer_question(self, context, question, max_length=512):
        """Answer a question given a context with improved prompt engineering"""
        
        # Improved answer extraction with multiple approaches
        def get_best_answer_span(start_logits, end_logits, input_ids, top_k=5):
            """Get the best answer span using improved logic"""
            start_probs = torch.softmax(start_logits, dim=-1)
            end_probs = torch.softmax(end_logits, dim=-1)
            
            # Get top-k start and end positions
            start_top_k = torch.topk(start_probs[0], top_k)
            end_top_k = torch.topk(end_probs[0], top_k)
            
            best_score = 0
            best_start = 0
            best_end = 0
            
            for start_idx, start_score in zip(start_top_k.indices, start_top_k.values):
                for end_idx, end_score in zip(end_top_k.indices, end_top_k.values):
                    if start_idx <= end_idx and end_idx - start_idx < 100:  # Reasonable answer length
                        score = start_score * end_score
                        if score > best_score:
                            best_score = score
                            best_start = start_idx.item()
                            best_end = end_idx.item()
            
            return best_start, best_end, best_score.item()
        
        # Clean and preprocess the context
        context_clean = self.preprocess_context(context)
        
        # Tokenize inputs
        inputs = self.tokenizer.encode_plus(
            question,
            context_clean,
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
        
        # Get the best answer span using improved logic
        start_idx, end_idx, confidence = get_best_answer_span(
            start_logits, end_logits, inputs['input_ids']
        )
        
        # Extract answer
        if start_idx <= end_idx and start_idx > 0:
            answer_tokens = inputs['input_ids'][0][start_idx:end_idx+1]
            answer = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)
            answer = self.postprocess_answer(answer, question)
        else:
            answer = "No answer found"
        
        return {
            "answer": answer,
            "confidence": confidence,
            "start_position": start_idx,
            "end_position": end_idx
        }
    
    def preprocess_context(self, context):
        """Clean and preprocess the contract text"""
        # Remove extra whitespace and normalize
        context = ' '.join(context.split())
        
        # Add section markers for better understanding
        context = context.replace('GOVERNING LAW:', '\n[GOVERNING LAW]:')
        context = context.replace('PAYMENT TERMS:', '\n[PAYMENT TERMS]:')
        context = context.replace('TERMINATION:', '\n[TERMINATION]:')
        context = context.replace('LIABILITY:', '\n[LIABILITY]:')
        context = context.replace('INTELLECTUAL PROPERTY:', '\n[INTELLECTUAL PROPERTY]:')
        context = context.replace('CONFIDENTIALITY:', '\n[CONFIDENTIALITY]:')
        context = context.replace('FORCE MAJEURE:', '\n[FORCE MAJEURE]:')
        context = context.replace('WARRANTY:', '\n[WARRANTY]:')
        context = context.replace('DISPUTE RESOLUTION:', '\n[DISPUTE RESOLUTION]:')
        context = context.replace('RENEWAL:', '\n[RENEWAL]:')
        
        return context
    
    def postprocess_answer(self, answer, question):
        """Clean up the extracted answer"""
        if not answer or answer.strip() == "":
            return "No answer found"
        
        # Remove common artifacts
        answer = answer.strip()
        answer = answer.replace('<s>', '').replace('</s>', '')
        answer = answer.replace('<pad>', '').replace('<mask>', '')
        
        # Remove leading/trailing punctuation that doesn't make sense
        while answer and answer[0] in '.,;:':
            answer = answer[1:].strip()
        
        # If answer is too short or just punctuation, mark as no answer
        if len(answer.strip()) < 3 or answer.strip() in ['the', 'a', 'an', 'and', 'or']:
            return "No answer found"
        
        return answer
    
    def analyze_contract(self, contract_text):
        """Analyze a contract using all CUAD questions"""
        results = {}
        
        for category, question in self.cuad_questions.items():
            result = self.answer_question(contract_text, question)
            results[category] = result
            
        return results
    
    def save_results(self, results, output_file="contract_analysis.json"):
        """Save analysis results to a JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    # Initialize the model
    tester = CUADModelTester()
    
    # Example contract text (you can replace this with actual contract content)
    sample_contract = """
    This Software License Agreement ("Agreement") is entered into on January 1, 2024, 
    between Company A and Company B. This Agreement shall be governed by the laws of 
    California. The term of this Agreement is 3 years from the effective date. 
    Either party may terminate this Agreement with 30 days written notice. 
    The licensee agrees to pay $10,000 annually for the software license. 
    All intellectual property rights remain with the licensor. 
    Both parties agree to maintain confidentiality of proprietary information.
    """
    
    # Analyze the contract
    print("Analyzing sample contract...")
    results = tester.analyze_contract(sample_contract)
    
    # Display results
    print("\n=== Contract Analysis Results ===")
    for category, result in results.items():
        print(f"\n{category.upper()}:")
        print(f"  Answer: {result['answer']}")
        print(f"  Confidence: {result['confidence']:.3f}")
    
    # Save results
    tester.save_results(results)
    print(f"\nResults saved to contract_analysis.json")

if __name__ == "__main__":
    main()
