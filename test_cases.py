"""
Comprehensive test cases for CUAD model with realistic contract examples
"""

# Test Case 1: Software Service Agreement
SOFTWARE_SERVICE_CONTRACT = """
SOFTWARE SERVICE AGREEMENT

This Software Service Agreement ("Agreement") is entered into on March 15, 2024, between TechCorp Inc., a Delaware corporation ("Provider"), and BusinessSolutions LLC, a California limited liability company ("Client").

GOVERNING LAW: This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles. Any disputes arising under this Agreement shall be subject to the exclusive jurisdiction of the courts located in New Castle County, Delaware.

PAYMENT TERMS: Client agrees to pay Provider a monthly service fee of $5,000, payable within thirty (30) days of receipt of invoice. Late payments shall incur a penalty of 1.5% per month. All payments shall be made in U.S. dollars via wire transfer or ACH.

TERMINATION: Either party may terminate this Agreement with sixty (60) days prior written notice. Provider may terminate immediately upon Client's material breach if such breach is not cured within fifteen (15) days of written notice. Upon termination, Client shall pay all outstanding fees and return or destroy all confidential information.

INTELLECTUAL PROPERTY: All software, documentation, and related materials provided by Provider remain the exclusive property of Provider. Client receives only a limited, non-exclusive license to use the software during the term. Client retains ownership of its data and content.

LIABILITY LIMITATION: Provider's total liability shall not exceed the fees paid by Client in the twelve (12) months preceding the claim. Provider shall not be liable for any indirect, consequential, or punitive damages. Client agrees to indemnify Provider against third-party claims arising from Client's use of the service.

CONFIDENTIALITY: Both parties agree to maintain strict confidentiality of proprietary information for a period of five (5) years after termination. Confidential information includes software code, business processes, customer data, and financial information.

WARRANTY: Provider warrants that the software will perform substantially in accordance with documentation for ninety (90) days. This warranty is exclusive and Provider disclaims all other warranties, express or implied, including merchantability and fitness for a particular purpose.

FORCE MAJEURE: Neither party shall be liable for delays or failures due to circumstances beyond their reasonable control, including natural disasters, government actions, or network outages, provided written notice is given within ten (10) days.

DISPUTE RESOLUTION: Any disputes shall first be addressed through good faith negotiations. If unresolved within thirty (30) days, disputes shall be settled through binding arbitration under AAA Commercial Rules in Delaware.

RENEWAL: This Agreement automatically renews for successive one-year terms unless either party provides ninety (90) days written notice of non-renewal before the current term expires.
"""

# Test Case 2: Employment Agreement
EMPLOYMENT_CONTRACT = """
EMPLOYMENT AGREEMENT

This Employment Agreement is made between DataTech Corporation ("Company") and Sarah Johnson ("Employee") effective January 1, 2024.

GOVERNING LAW: This Agreement is governed by the laws of New York State and federal law. Employee consents to jurisdiction in New York courts for any employment-related disputes.

COMPENSATION: Employee shall receive an annual salary of $120,000, paid bi-weekly. In addition, Employee is eligible for an annual performance bonus of up to 20% of base salary and stock options as determined by the Board.

TERMINATION: Company may terminate Employee's employment at any time with or without cause. If terminated without cause, Employee shall receive two (2) weeks severance pay. Employee may resign with two (2) weeks notice.

INTELLECTUAL PROPERTY: All inventions, discoveries, and works created during employment belong exclusively to Company. Employee assigns all rights in work-related intellectual property and agrees not to use Company's proprietary information for personal benefit.

CONFIDENTIALITY: Employee agrees to maintain confidentiality of all Company trade secrets, customer lists, financial data, and business strategies indefinitely, even after employment ends. Violation may result in immediate termination and legal action.

NON-COMPETE: For twelve (12) months after termination, Employee shall not work for direct competitors or solicit Company customers within the tri-state area. This restriction applies only to roles substantially similar to Employee's position at Company.

BENEFITS: Employee is entitled to health insurance (Company pays 80%), dental and vision coverage, 401(k) with 4% Company match, twenty (20) days paid vacation, and ten (10) sick days annually.
"""

# Test Case 3: Vendor Supply Agreement
VENDOR_SUPPLY_CONTRACT = """
VENDOR SUPPLY AGREEMENT

This Supply Agreement is between Manufacturing Corp ("Buyer") and Industrial Supplies Inc ("Supplier"), effective April 1, 2024.

GOVERNING LAW: This Agreement shall be governed by the Uniform Commercial Code and the laws of Texas. All disputes shall be resolved in Harris County, Texas courts.

PAYMENT TERMS: Buyer shall pay within net 45 days of delivery. Payments delayed beyond 60 days incur 2% monthly late fees. Supplier may suspend deliveries for accounts more than 90 days overdue.

PRICING: Current unit price is $15.50 per component for quantities of 1,000+ units. Prices are firm for six (6) months, after which Supplier may adjust with 60 days notice. Volume discounts apply for orders exceeding 10,000 units.

TERMINATION: Either party may terminate with 120 days written notice. Immediate termination is permitted for material breach, insolvency, or failure to meet quality standards after 30-day cure period.

QUALITY ASSURANCE: All products must meet ISO 9001 standards and pass Buyer's inspection. Defective products will be replaced at Supplier's expense. Supplier warrants products against defects for eighteen (18) months from delivery.

LIABILITY: Supplier's liability is limited to replacement cost of defective goods. Neither party is liable for consequential damages exceeding $100,000 annually. Supplier carries $2 million product liability insurance.

FORCE MAJEURE: Performance is excused for acts of God, war, government regulation, labor disputes, or supplier failures beyond reasonable control. Party must notify within 48 hours and use best efforts to minimize impact.

INTELLECTUAL PROPERTY: Supplier retains rights to its manufacturing processes. Buyer owns rights to custom specifications and designs. Neither party may reverse engineer the other's proprietary technology.

CONFIDENTIALITY: All pricing, specifications, and business terms are confidential for three (3) years post-termination. Information may only be shared with employees having legitimate business need.
"""

# Test Questions for different scenarios
TEST_QUESTIONS = {
    "basic": [
        "What is the governing law?",
        "What are the payment terms?", 
        "How can this agreement be terminated?",
        "What are the confidentiality requirements?",
        "What intellectual property provisions apply?"
    ],
    
    "specific": [
        "What is the monthly fee amount?",
        "How many days notice is required for termination?",
        "What is the late payment penalty rate?",
        "How long does the confidentiality obligation last?",
        "What is the liability cap amount?",
        "What courts have jurisdiction over disputes?",
        "What is the automatic renewal period?",
        "What warranty period is provided?",
        "What happens in case of force majeure events?",
        "What are the volume discount thresholds?"
    ],
    
    "complex": [
        "Under what circumstances can the agreement be terminated immediately?",
        "What happens to intellectual property rights upon termination?",
        "What damages are excluded from liability coverage?",
        "What dispute resolution process must be followed before litigation?",
        "What constitutes a material breach requiring cure period?",
        "What insurance requirements must the supplier maintain?",
        "What geographic restrictions apply to non-compete clauses?",
        "What quality standards must products meet?"
    ]
}

def print_test_cases():
    """Print all test cases for easy copying"""
    print("=" * 80)
    print("COMPREHENSIVE CONTRACT TEST CASES FOR CUAD MODEL")
    print("=" * 80)
    
    print("\n📄 TEST CASE 1: SOFTWARE SERVICE AGREEMENT")
    print("-" * 50)
    print(SOFTWARE_SERVICE_CONTRACT)
    
    print("\n📄 TEST CASE 2: EMPLOYMENT AGREEMENT") 
    print("-" * 50)
    print(EMPLOYMENT_CONTRACT)
    
    print("\n📄 TEST CASE 3: VENDOR SUPPLY AGREEMENT")
    print("-" * 50)
    print(VENDOR_SUPPLY_CONTRACT)
    
    print("\n❓ SUGGESTED TEST QUESTIONS")
    print("-" * 50)
    
    print("\n🔹 BASIC QUESTIONS:")
    for q in TEST_QUESTIONS["basic"]:
        print(f"   • {q}")
    
    print("\n🔹 SPECIFIC QUESTIONS:")
    for q in TEST_QUESTIONS["specific"]:
        print(f"   • {q}")
        
    print("\n🔹 COMPLEX QUESTIONS:")
    for q in TEST_QUESTIONS["complex"]:
        print(f"   • {q}")

if __name__ == "__main__":
    print_test_cases()
