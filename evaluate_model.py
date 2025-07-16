"""
Evaluation script for the fine-tuned CUAD model
"""
import torch
import json
from transformers import RobertaTokenizer, RobertaForQuestionAnswering
from sklearn.metrics import f1_score
import numpy as np

class CUADEvaluator:
    def __init__(self, model_path="./"):
        """Initialize the model and tokenizer"""
        self.tokenizer = RobertaTokenizer.from_pretrained(model_path)
        self.model = RobertaForQuestionAnswering.from_pretrained(model_path)
        self.model.eval()
    
    def evaluate_predictions(self, predictions_file="predictions_.json"):
        """Evaluate model predictions against ground truth"""
        try:
            with open(predictions_file, 'r', encoding='utf-8') as f:
                predictions = json.load(f)
            
            print(f"Loaded {len(predictions)} predictions")
            
            # Basic statistics
            non_empty_predictions = [p for p in predictions.values() if p.strip()]
            empty_predictions = len(predictions) - len(non_empty_predictions)
            
            print(f"\nPrediction Statistics:")
            print(f"Total predictions: {len(predictions)}")
            print(f"Non-empty predictions: {len(non_empty_predictions)}")
            print(f"Empty predictions: {empty_predictions}")
            print(f"Answer rate: {len(non_empty_predictions)/len(predictions)*100:.2f}%")
            
            # Average answer length
            answer_lengths = [len(p.split()) for p in non_empty_predictions]
            if answer_lengths:
                print(f"Average answer length: {np.mean(answer_lengths):.2f} words")
                print(f"Min answer length: {min(answer_lengths)} words")
                print(f"Max answer length: {max(answer_lengths)} words")
            
            return predictions
            
        except FileNotFoundError:
            print(f"Predictions file {predictions_file} not found")
            return None
    
    def analyze_model_performance(self):
        """Analyze the model's performance based on available files"""
        print("=== CUAD Model Analysis ===\n")
        
        # Check model configuration
        print("Model Configuration:")
        print(f"Model type: {self.model.config.model_type}")
        print(f"Hidden size: {self.model.config.hidden_size}")
        print(f"Number of layers: {self.model.config.num_hidden_layers}")
        print(f"Number of attention heads: {self.model.config.num_attention_heads}")
        print(f"Vocabulary size: {self.model.config.vocab_size}")
        
        # Evaluate predictions if available
        predictions = self.evaluate_predictions()
        
        # Show sample predictions
        if predictions:
            print(f"\nSample Predictions:")
            sample_keys = list(predictions.keys())[:5]
            for i, key in enumerate(sample_keys, 1):
                answer = predictions[key]
                print(f"{i}. ID: {key}")
                print(f"   Answer: {answer[:100]}{'...' if len(answer) > 100 else ''}")
                print()
    
    def test_on_sample_data(self):
        """Test the model on sample contract data"""
        sample_contracts = [
            {
                "context": "This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of laws principles.",
                "question": "What is the governing law?",
                "expected": "laws of the State of California"
            },
            {
                "context": "Either party may terminate this Agreement at any time with thirty (30) days prior written notice to the other party.",
                "question": "What are the termination clauses?",
                "expected": "Either party may terminate this Agreement at any time with thirty (30) days prior written notice"
            },
            {
                "context": "The License fee shall be $50,000 per year, payable in quarterly installments of $12,500 each.",
                "question": "What are the payment terms?",
                "expected": "$50,000 per year, payable in quarterly installments of $12,500 each"
            }
        ]
        
        print("\n=== Testing on Sample Data ===")
        
        for i, sample in enumerate(sample_contracts, 1):
            result = self.answer_question(sample["context"], sample["question"])
            
            print(f"\nTest {i}:")
            print(f"Question: {sample['question']}")
            print(f"Expected: {sample['expected']}")
            print(f"Predicted: {result['answer']}")
            print(f"Confidence: {result['confidence']:.3f}")
            print("-" * 50)
    
    def answer_question(self, context, question, max_length=512):
        """Answer a question given a context"""
        inputs = self.tokenizer.encode_plus(
            question,
            context,
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
        
        start_idx = torch.argmax(start_logits)
        end_idx = torch.argmax(end_logits)
        
        if start_idx <= end_idx:
            answer_tokens = inputs['input_ids'][0][start_idx:end_idx+1]
            answer = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)
        else:
            answer = "No answer found"
        
        start_score = torch.softmax(start_logits, dim=-1)[0][start_idx].item()
        end_score = torch.softmax(end_logits, dim=-1)[0][end_idx].item()
        confidence = (start_score + end_score) / 2
        
        return {
            "answer": answer,
            "confidence": confidence,
            "start_position": start_idx.item(),
            "end_position": end_idx.item()
        }

def main():
    evaluator = CUADEvaluator()
    evaluator.analyze_model_performance()
    evaluator.test_on_sample_data()

if __name__ == "__main__":
    main()
