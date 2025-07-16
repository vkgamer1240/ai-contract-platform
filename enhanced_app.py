"""
Enhanced Flask Web Interface with Groq API Integration and Risk Assessment
"""
from flask import Flask, render_template, request, jsonify
import os
from enhanced_analyzer import EnhancedCUADAnalyzer

app = Flask(__name__)

# Global analyzer
enhanced_analyzer = None

def load_enhanced_model():
    """Load the enhanced analyzer"""
    global enhanced_analyzer
    groq_api_key = os.getenv('GROQ_API_KEY')  # Set this in environment or pass directly
    enhanced_analyzer = EnhancedCUADAnalyzer('./', groq_api_key=groq_api_key)

@app.route('/')
def home():
    return render_template('enhanced_index.html')

@app.route('/analyze_comprehensive', methods=['POST'])
def analyze_comprehensive():
    """Comprehensive analysis using both CUAD and Groq"""
    data = request.json
    contract_text = data.get('contract_text', '')
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    try:
        results = enhanced_analyzer.analyze_contract_comprehensive(contract_text)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/analyze_risks', methods=['POST'])
def analyze_risks():
    """Risk-focused analysis"""
    data = request.json
    contract_text = data.get('contract_text', '')
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    try:
        # Get CUAD results first
        contract_type = enhanced_analyzer.detect_contract_type(contract_text)
        relevant_categories = enhanced_analyzer.get_relevant_categories(contract_type)
        
        cuad_results = {}
        for category in relevant_categories:
            if category in enhanced_analyzer.question_templates:
                result = enhanced_analyzer.answer_question_advanced(contract_text, category)
                cuad_results[category] = result
        
        # Risk assessment
        risk_assessment = enhanced_analyzer.assess_risks(contract_text, cuad_results)
        
        # Groq risk analysis
        groq_analysis = enhanced_analyzer.analyze_with_groq(contract_text, "risk_assessment")
        
        return jsonify({
            "contract_type": contract_type,
            "risk_assessment": risk_assessment,
            "groq_analysis": groq_analysis,
            "recommendations": enhanced_analyzer.generate_recommendations(risk_assessment, contract_type)
        })
    except Exception as e:
        return jsonify({'error': f'Risk analysis failed: {str(e)}'}), 500

@app.route('/analyze_app_specific', methods=['POST'])
def analyze_app_specific():
    """App/software specific analysis"""
    data = request.json
    contract_text = data.get('contract_text', '')
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    try:
        # App-specific categories
        app_categories = [
            "data_privacy", "app_permissions", "subscription_terms", 
            "user_content", "governing_law", "liability"
        ]
        
        cuad_results = {}
        for category in app_categories:
            if category in enhanced_analyzer.question_templates:
                result = enhanced_analyzer.answer_question_advanced(contract_text, category)
                cuad_results[category] = result
        
        # App-specific Groq analysis
        groq_analysis = enhanced_analyzer.analyze_with_groq(contract_text, "app_specific")
        
        # Risk assessment
        risk_assessment = enhanced_analyzer.assess_risks(contract_text, cuad_results)
        
        return jsonify({
            "cuad_analysis": cuad_results,
            "groq_analysis": groq_analysis,
            "risk_assessment": risk_assessment,
            "contract_type": "app_agreement"
        })
    except Exception as e:
        return jsonify({'error': f'App analysis failed: {str(e)}'}), 500

@app.route('/get_enhanced_samples', methods=['GET'])
def get_enhanced_samples():
    """Get enhanced sample contracts including app agreements"""
    samples = {
        "app_terms": """MOBILE APP TERMS OF SERVICE

By downloading and using our mobile application ("App"), you agree to these Terms of Service.

GOVERNING LAW: This agreement is governed by the laws of California, USA. Any disputes will be resolved in California courts.

DATA COLLECTION: We collect your location data, device information, contacts, photos, and usage patterns. This data may be shared with third-party advertising partners and analytics services.

APP PERMISSIONS: The app requires access to:
- Camera and photo library for image uploads
- Microphone for voice features  
- Location services for geo-tagging
- Contacts for social features
- Device storage for caching

SUBSCRIPTION TERMS: Premium features cost $9.99/month with automatic renewal every 30 days. You can cancel through your device's app store settings. No refunds for partial months.

USER CONTENT: Any content you upload (photos, videos, text) becomes our property. We can use, modify, and distribute your content for any commercial purpose without compensation.

LIABILITY: We disclaim all warranties and limit our liability to $10. We are not responsible for data loss, privacy breaches, or device damage.

TERMINATION: We can terminate your account immediately without notice for any reason. You lose access to all content and premium features.

PRIVACY POLICY: We collect personal information including but not limited to name, email, location, device ID, and behavioral data for advertising purposes.

AUTOMATIC UPDATES: The app may automatically download and install updates that can change functionality or remove features.

THIRD-PARTY SERVICES: We integrate with social media platforms and may share your data with them according to their privacy policies.""",

        "software_saas": """SOFTWARE AS A SERVICE AGREEMENT

This SaaS Agreement is between CloudTech Solutions ("Provider") and Customer ("Client").

GOVERNING LAW: This Agreement shall be governed by Delaware law. Disputes must be resolved through binding arbitration in Delaware.

PAYMENT TERMS: Client pays $500/month for unlimited users. Payment is due within 10 days of invoice. Late fees of 5% per month apply. No refunds.

DATA OWNERSHIP: All customer data remains property of Client. Provider has right to access and analyze data for service improvements and may create anonymized datasets.

SERVICE LEVELS: 99.5% uptime guarantee. No credits for downtime under 4 hours per month. Provider may suspend service for non-payment.

INTELLECTUAL PROPERTY: Provider retains all rights to software. Client receives non-exclusive license during subscription term only.

CONFIDENTIALITY: Both parties protect confidential information for 5 years post-termination. Provider may disclose data if legally required.

LIABILITY LIMITATION: Provider's liability capped at 3 months of fees paid. No liability for indirect damages or data loss exceeding $10,000.

TERMINATION: Either party may terminate with 30 days notice. Provider may terminate immediately for breach. All data deleted within 30 days.

AUTOMATIC RENEWAL: Agreement auto-renews annually unless cancelled 60 days prior to renewal date.

COMPLIANCE: Client responsible for ensuring their use complies with applicable laws including GDPR, HIPAA, SOX as applicable.""",

        "mobile_game": """MOBILE GAME TERMS OF SERVICE

Welcome to our mobile game! By playing, you accept these terms.

GOVERNING LAW: Terms governed by UK law. Disputes resolved in London courts only.

IN-APP PURCHASES: Game currency costs real money. No refunds except as required by law. Purchases are final. Currency has no real-world value.

USER ACCOUNTS: We can ban accounts for any reason without notice. All virtual items and progress lost permanently upon ban.

USER CONTENT: Any usernames, avatars, or chat messages become our property. We can use them in marketing without permission or payment.

DATA COLLECTION: We collect device info, gameplay data, location, contacts, and may record gameplay sessions. Data shared with advertising partners.

PRIVACY: Players must be 13+ years old. We do not knowingly collect data from children under 13.

ADVERTISING: Game contains third-party ads that may collect additional data. We're not responsible for advertiser data practices.

VIRTUAL CURRENCY: In-game currency can only be used within the game. No cash value. Currency may expire. We can modify currency rates anytime.

LIABILITY: Game provided "as is" with no warranties. We're not liable for addiction, time lost, or negative impacts on health or relationships.

UPDATES: We may modify game features, remove content, or shut down servers at any time without notice or refund.

SOCIAL FEATURES: Chat and multiplayer features monitored. Inappropriate behavior results in immediate ban.

THIRD-PARTY LINKS: Game may link to external websites. We're not responsible for external content or privacy practices.""",

        "employment_tech": """TECHNOLOGY EMPLOYMENT AGREEMENT

Agreement between TechStartup Inc. ("Company") and Employee effective immediately.

GOVERNING LAW: Agreement governed by California law. Employee waives right to jury trial for employment disputes.

COMPENSATION: Base salary $150,000 annually plus equity options. Salary reviews at Company discretion only.

INTELLECTUAL PROPERTY: All work product, ideas, inventions created during employment (even on personal time) belongs to Company. This includes personal projects using Company resources.

CONFIDENTIALITY: Employee protects all Company information indefinitely, including after termination. Violation results in immediate termination and legal action.

NON-COMPETE: Employee cannot work for competitors for 2 years after termination within 50-mile radius. Applies to any tech company with similar products.

WORK REQUIREMENTS: Employee expected to work nights and weekends as needed. On-call availability 24/7 for production issues.

TERMINATION: Company can terminate without cause or notice. No severance pay unless specifically agreed. Employee must give 4 weeks notice to resign.

BENEFITS: Health insurance (employee pays 30%), no dental/vision. 10 vacation days annually, no rollover allowed.

STOCK OPTIONS: Options vest over 4 years with 1-year cliff. Options forfeit if terminated for any reason. Exercise within 90 days of termination or forfeit.

ASSIGNMENT OF INVENTIONS: Employee assigns all past, present, and future inventions to Company, even if created outside work hours.

MONITORING: Company may monitor all communications, computer usage, and location during work hours."""
    }
    
    return jsonify(samples)

@app.route('/detect_contract_type', methods=['POST'])
def detect_contract_type():
    """Detect contract type for appropriate analysis"""
    data = request.json
    contract_text = data.get('contract_text', '')
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    contract_type = enhanced_analyzer.detect_contract_type(contract_text)
    relevant_categories = enhanced_analyzer.get_relevant_categories(contract_type)
    
    return jsonify({
        "contract_type": contract_type,
        "relevant_categories": relevant_categories,
        "analysis_suggestions": get_analysis_suggestions(contract_type)
    })

def get_analysis_suggestions(contract_type):
    """Get analysis suggestions based on contract type"""
    suggestions = {
        "app_agreement": [
            "Focus on data privacy and permissions",
            "Check subscription and billing terms carefully",
            "Review content ownership policies",
            "Verify cancellation procedures"
        ],
        "employment": [
            "Review IP assignment clauses",
            "Check non-compete restrictions",
            "Verify termination and severance terms",
            "Understand confidentiality obligations"
        ],
        "vendor_supply": [
            "Analyze payment terms and late fees",
            "Review quality standards and warranties",
            "Check liability limitations",
            "Verify delivery and performance requirements"
        ],
        "service_agreement": [
            "Review service levels and guarantees",
            "Check liability and indemnification",
            "Verify termination procedures",
            "Understand intellectual property rights"
        ]
    }
    
    return suggestions.get(contract_type, [
        "Review governing law and jurisdiction",
        "Check termination conditions",
        "Analyze liability limitations",
        "Verify confidentiality requirements"
    ])

if __name__ == '__main__':
    load_enhanced_model()
    app.run(debug=True, host='0.0.0.0', port=5001)  # Different port to avoid conflicts
