"""
Interactive test script for CUAD model with multiple contract examples
"""
import torch
from transformers import RobertaTokenizer, RobertaForQuestionAnswering
import json

class InteractiveCUADTester:
    def __init__(self, model_path="./"):
        """Initialize the model and tokenizer"""
        print("Loading CUAD model...")
        self.tokenizer = RobertaTokenizer.from_pretrained(model_path)
        self.model = RobertaForQuestionAnswering.from_pretrained(model_path)
        self.model.eval()
        print("Model loaded successfully!")
        
        # Sample contracts for testing
        self.contracts = {
            "software": """
SOFTWARE SERVICE AGREEMENT

This Software Service Agreement ("Agreement") is entered into on March 15, 2024, between TechCorp Inc., a Delaware corporation ("Provider"), and BusinessSolutions LLC, a California limited liability company ("Client").

GOVERNING LAW: This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles.

PAYMENT TERMS: Client agrees to pay Provider a monthly service fee of $5,000, payable within thirty (30) days of receipt of invoice. Late payments shall incur a penalty of 1.5% per month.

TERMINATION: Either party may terminate this Agreement with sixty (60) days prior written notice. Provider may terminate immediately upon Client's material breach if such breach is not cured within fifteen (15) days of written notice.

INTELLECTUAL PROPERTY: All software, documentation, and related materials provided by Provider remain the exclusive property of Provider. Client receives only a limited, non-exclusive license to use the software.

LIABILITY LIMITATION: Provider's total liability shall not exceed the fees paid by Client in the twelve (12) months preceding the claim. Provider shall not be liable for any indirect, consequential, or punitive damages.

CONFIDENTIALITY: Both parties agree to maintain strict confidentiality of proprietary information for a period of five (5) years after termination.

WARRANTY: Provider warrants that the software will perform substantially in accordance with documentation for ninety (90) days.

FORCE MAJEURE: Neither party shall be liable for delays or failures due to circumstances beyond their reasonable control, including natural disasters, government actions, or network outages.

DISPUTE RESOLUTION: Any disputes shall first be addressed through good faith negotiations. If unresolved within thirty (30) days, disputes shall be settled through binding arbitration under AAA Commercial Rules in Delaware.

RENEWAL: This Agreement automatically renews for successive one-year terms unless either party provides ninety (90) days written notice of non-renewal.
""",
            
            "employment": """
EMPLOYMENT AGREEMENT

This Employment Agreement is made between DataTech Corporation ("Company") and Sarah Johnson ("Employee") effective January 1, 2024.

GOVERNING LAW: This Agreement is governed by the laws of New York State. Employee consents to jurisdiction in New York courts for employment-related disputes.

COMPENSATION: Employee shall receive an annual salary of $120,000, paid bi-weekly. Employee is eligible for an annual performance bonus of up to 20% of base salary.

TERMINATION: Company may terminate Employee at any time with or without cause. If terminated without cause, Employee shall receive two (2) weeks severance pay. Employee may resign with two (2) weeks notice.

INTELLECTUAL PROPERTY: All inventions, discoveries, and works created during employment belong exclusively to Company. Employee assigns all rights in work-related intellectual property.

CONFIDENTIALITY: Employee agrees to maintain confidentiality of all Company trade secrets, customer lists, financial data, and business strategies indefinitely, even after employment ends.

NON-COMPETE: For twelve (12) months after termination, Employee shall not work for direct competitors or solicit Company customers within the tri-state area.

BENEFITS: Employee is entitled to health insurance, 401(k) with 4% Company match, twenty (20) days paid vacation, and ten (10) sick days annually.
""",
            
            "vendor": """
VENDOR SUPPLY AGREEMENT

This Supply Agreement is between Manufacturing Corp ("Buyer") and Industrial Supplies Inc ("Supplier"), effective April 1, 2024.

GOVERNING LAW: This Agreement shall be governed by the Uniform Commercial Code and the laws of Texas. All disputes shall be resolved in Harris County, Texas courts.

PAYMENT TERMS: Buyer shall pay within net 45 days of delivery. Payments delayed beyond 60 days incur 2% monthly late fees. Supplier may suspend deliveries for accounts more than 90 days overdue.

PRICING: Current unit price is $15.50 per component for quantities of 1,000+ units. Prices are firm for six (6) months.

TERMINATION: Either party may terminate with 120 days written notice. Immediate termination is permitted for material breach, insolvency, or failure to meet quality standards.

QUALITY ASSURANCE: All products must meet ISO 9001 standards and pass Buyer's inspection. Supplier warrants products against defects for eighteen (18) months from delivery.

LIABILITY: Supplier's liability is limited to replacement cost of defective goods. Neither party is liable for consequential damages exceeding $100,000 annually.

FORCE MAJEURE: Performance is excused for acts of God, war, government regulation, labor disputes, or supplier failures beyond reasonable control.

INTELLECTUAL PROPERTY: Supplier retains rights to its manufacturing processes. Buyer owns rights to custom specifications and designs.

CONFIDENTIALITY: All pricing, specifications, and business terms are confidential for three (3) years post-termination.
"""
        }
        
        # Good test questions
        self.sample_questions = [
            "What is the governing law?",
            "What are the payment terms?",
            "How can this agreement be terminated?",
            "What are the confidentiality requirements?",
            "What intellectual property provisions apply?",
            "What is the liability limitation?",
            "What are the force majeure provisions?",
            "What dispute resolution mechanisms are specified?",
            "What are the renewal terms?",
            "What warranty is provided?"
        ]
    
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
            "confidence": confidence
        }
    
    def test_contract(self, contract_type):
        """Test a specific contract with sample questions"""
        if contract_type not in self.contracts:
            print(f"Contract type '{contract_type}' not found!")
            return
        
        contract = self.contracts[contract_type]
        print(f"\n{'='*60}")
        print(f"TESTING {contract_type.upper()} CONTRACT")
        print(f"{'='*60}")
        
        results = {}
        for question in self.sample_questions:
            result = self.answer_question(contract, question)
            results[question] = result
            
            print(f"\n❓ Question: {question}")
            print(f"💡 Answer: {result['answer']}")
            print(f"📊 Confidence: {result['confidence']:.3f}")
            print("-" * 50)
        
        return results
    
    def interactive_test(self):
        """Interactive testing mode"""
        print("\n🔍 CUAD Model Interactive Tester")
        print("Available contracts: software, employment, vendor")
        print("Type 'quit' to exit\n")
        
        while True:
            contract_type = input("Choose contract type (software/employment/vendor): ").strip().lower()
            
            if contract_type == 'quit':
                break
            
            if contract_type in self.contracts:
                self.test_contract(contract_type)
                
                # Ask for custom question
                custom_q = input("\nEnter a custom question (or press Enter to continue): ").strip()
                if custom_q:
                    result = self.answer_question(self.contracts[contract_type], custom_q)
                    print(f"\n❓ Your Question: {custom_q}")
                    print(f"💡 Answer: {result['answer']}")
                    print(f"📊 Confidence: {result['confidence']:.3f}")
            else:
                print("Invalid contract type! Choose from: software, employment, vendor")
    
    def run_all_tests(self):
        """Run tests on all contracts"""
        print("\n🚀 Running tests on all contracts...")
        
        for contract_type in self.contracts.keys():
            self.test_contract(contract_type)
        
        print("\n✅ All tests completed!")

def main():
    tester = InteractiveCUADTester()
    
    print("\nChoose an option:")
    print("1. Run all tests")
    print("2. Interactive testing")
    print("3. Test specific contract type")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        tester.run_all_tests()
    elif choice == "2":
        tester.interactive_test()
    elif choice == "3":
        contract_type = input("Enter contract type (software/employment/vendor): ").strip().lower()
        tester.test_contract(contract_type)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
