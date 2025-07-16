"""
Unified Flask Server - Serves both Landing Page and Contract Analysis
===================================================================
This combines your React landing page with the premium contract analysis app
"""
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import json
import tempfile
from datetime import datetime
from enhanced_analyzer import EnhancedCUADAnalyzer
from advanced_features import AdvancedContractProcessor, create_sample_app_agreements
from pathlib import Path
from contract_creator import ContractCreator
from whatsapp_integration import WhatsAppContractSender, AdvancedWhatsAppSender

app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')

# Enable CORS for all routes
CORS(app)

# Global variables
enhanced_analyzer = None
processor = None

def load_enhanced_system():
    """Load YOUR enhanced analyzer and processor"""
    global enhanced_analyzer, processor
    try:
        print("Loading YOUR fine-tuned CUAD analyzer...")
        # Load YOUR fine-tuned model (Groq enhancement disabled by default)
        enhanced_analyzer = EnhancedCUADAnalyzer('./', enable_groq_enhancement=False)
        print("✅ YOUR fine-tuned analyzer loaded successfully")
        
        print("Loading advanced processor...")
        processor = AdvancedContractProcessor(enhanced_analyzer)
        print("✅ Advanced processor loaded successfully")
        
    except Exception as e:
        print(f"❌ Error loading YOUR enhanced system: {str(e)}")
        import traceback
        traceback.print_exc()
        # Don't let the server fail to start, but log the error
        enhanced_analyzer = None
        processor = None

# Serve React App (Landing Page)
@app.route('/')
def serve_landing_page():
    """Serve the React landing page"""
    return render_template('landing.html')

# Contract Analysis Routes
@app.route('/contract-analysis')
def contract_analysis_dashboard():
    """Main contract analysis interface"""
    return render_template('premium_index.html')

@app.route('/api/analyze_single', methods=['POST'])
def analyze_single_contract():
    """Single contract comprehensive analysis"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        contract_text = data.get('contract_text', '')
        contract_name = data.get('contract_name', 'Unnamed Contract')
        
        if not contract_text:
            return jsonify({'error': 'Contract text is required'}), 400
        
        # Check if analyzer is loaded
        if not enhanced_analyzer:
            return jsonify({'error': 'Analyzer not initialized'}), 500
        
        print(f"Starting analysis for contract: {contract_name}")
        
        # Comprehensive analysis with error handling
        try:
            results = enhanced_analyzer.analyze_contract_comprehensive(contract_text)
            print("CUAD analysis completed successfully")
        except Exception as e:
            print(f"CUAD analysis failed: {str(e)}")
            return jsonify({'error': f'CUAD analysis failed: {str(e)}'}), 500
        
        # Generate report with error handling
        try:
            if processor:
                report = processor.generate_contract_report(results, contract_name)
                print("Report generation completed")
            else:
                report = "Report generation not available"
                print("Processor not available, skipping report generation")
        except Exception as e:
            print(f"Report generation failed: {str(e)}")
            report = f"Report generation failed: {str(e)}"
        
        return jsonify({
            'analysis': results,
            'report': report,
            'contract_name': contract_name,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Analysis endpoint error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/batch_analyze', methods=['POST'])
def batch_analyze_contracts():
    """Batch analysis of multiple contracts"""
    data = request.json
    contracts = data.get('contracts', [])
    
    if not contracts:
        return jsonify({'error': 'At least one contract is required'}), 400
    
    try:
        # Validate contract format
        for contract in contracts:
            if 'name' not in contract or 'text' not in contract:
                return jsonify({'error': 'Each contract must have name and text fields'}), 400
        
        results = processor.batch_analyze_contracts(contracts)
        
        return jsonify({
            'batch_results': results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Batch analysis failed: {str(e)}'}), 500

@app.route('/api/compare_contracts', methods=['POST'])
def compare_contracts():
    """Compare two contracts"""
    data = request.json
    contract1 = data.get('contract1', {})
    contract2 = data.get('contract2', {})
    
    if not contract1.get('text') or not contract2.get('text'):
        return jsonify({'error': 'Both contracts must have text'}), 400
    
    try:
        names = (
            contract1.get('name', 'Contract A'),
            contract2.get('name', 'Contract B')
        )
        
        comparison = processor.compare_contracts(
            contract1['text'],
            contract2['text'],
            names
        )
        
        return jsonify({
            'comparison': comparison,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Comparison failed: {str(e)}'}), 500

@app.route('/api/check_compliance', methods=['POST'])
def check_app_compliance():
    """Check app store compliance"""
    data = request.json
    contract_text = data.get('contract_text', '')
    platform = data.get('platform', 'both')  # ios, android, or both
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    try:
        compliance_results = processor.analyze_app_store_compliance(contract_text, platform)
        
        return jsonify({
            'compliance': compliance_results,
            'platform': platform,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Compliance check failed: {str(e)}'}), 500

@app.route('/api/get_sample_contracts')
def get_sample_contracts():
    """Get sample contracts for testing"""
    samples = create_sample_app_agreements()
    
    # Convert to list format for frontend
    contract_list = []
    for key, text in samples.items():
        contract_list.append({
            'id': key,
            'name': key.replace('_', ' ').title(),
            'text': text,
            'type': 'app_agreement' if 'app' in key or 'game' in key or 'social' in key else 'saas'
        })
    
    return jsonify({'samples': contract_list})

@app.route('/api/enhanced_analysis', methods=['POST'])
def enhanced_analysis():
    """Enhanced analysis using YOUR fine-tuned model"""
    data = request.json
    contract_text = data.get('contract_text', '')
    analysis_type = data.get('analysis_type', 'comprehensive')
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    try:
        # Use YOUR model for enhanced analysis
        enhanced_result = enhanced_analyzer.get_optional_enhancement(contract_text, analysis_type)
        
        return jsonify({
            'enhanced_analysis': enhanced_result,
            'analysis_type': analysis_type,
            'model_used': 'YOUR_FINE_TUNED_ROBERTA',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Enhanced analysis failed: {str(e)}'}), 500

@app.route('/api/export_report', methods=['POST'])
def export_report():
    """Export analysis report as markdown file"""
    data = request.json
    analysis_results = data.get('analysis_results')
    contract_name = data.get('contract_name', 'Contract')
    
    if not analysis_results:
        return jsonify({'error': 'Analysis results required'}), 400
    
    try:
        # Generate report
        report = processor.generate_contract_report(analysis_results, contract_name)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(report)
            temp_path = f.name
        
        # Return file
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f"{contract_name.replace(' ', '_')}_analysis_report.md",
            mimetype='text/markdown'
        )
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/api/risk_assessment', methods=['POST'])
def detailed_risk_assessment():
    """Detailed risk assessment with scoring"""
    data = request.json
    contract_text = data.get('contract_text', '')
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    try:
        # Detect contract type
        contract_type = enhanced_analyzer.detect_contract_type(contract_text)
        relevant_categories = enhanced_analyzer.get_relevant_categories(contract_type)
        
        # Get CUAD analysis
        cuad_results = {}
        for category in relevant_categories:
            if category in enhanced_analyzer.question_templates:
                result = enhanced_analyzer.answer_question_advanced(contract_text, category)
                cuad_results[category] = result
        
        # Risk assessment
        risk_assessment = enhanced_analyzer.assess_risks(contract_text, cuad_results)
        
        # Groq risk analysis
        groq_analysis = enhanced_analyzer.analyze_with_groq(contract_text, "risk_assessment")
        
        # Generate recommendations
        recommendations = enhanced_analyzer.generate_recommendations(risk_assessment, contract_type)
        
        return jsonify({
            'contract_type': contract_type,
            'risk_assessment': risk_assessment,
            'cuad_analysis': cuad_results,
            'groq_analysis': groq_analysis,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Risk assessment failed: {str(e)}'}), 500

@app.route('/api/health_check')
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'your_model_loaded': enhanced_analyzer is not None,
        'groq_enhancement': enhanced_analyzer.groq_enhancer is not None if enhanced_analyzer else False,
        'primary_model': 'YOUR_FINE_TUNED_ROBERTA_CUAD',
        'timestamp': datetime.now().isoformat()
    })

# Authentication API endpoints (for React frontend)
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Handle login for React frontend"""
    data = request.json
    email = data.get('email', '')
    password = data.get('password', '')
    
    # Simple demo authentication - replace with real auth
    if email and password:
        return jsonify({
            'success': True,
            'user': {
                'id': 1,
                'email': email,
                'name': email.split('@')[0]
            },
            'token': 'demo_token_123'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """Handle signup for React frontend"""
    data = request.json
    email = data.get('email', '')
    password = data.get('password', '')
    name = data.get('name', '')
    
    # Simple demo signup - replace with real auth
    if email and password and name:
        return jsonify({
            'success': True,
            'message': 'Account created successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'All fields are required'
        }), 400

@app.route('/api/test_analyzer')
def test_analyzer():
    """Test if YOUR analyzer is working"""
    try:
        if not enhanced_analyzer:
            return jsonify({'error': 'YOUR analyzer not loaded', 'status': 'failed'}), 500
        
        # Simple test with YOUR model
        test_text = "This is a test contract. The governing law is California law."
        result = enhanced_analyzer.detect_contract_type(test_text)
        
        return jsonify({
            'status': 'working',
            'your_model_loaded': True,
            'processor_loaded': processor is not None,
            'enhancement_available': enhanced_analyzer.groq_enhancer is not None,
            'test_result': result,
            'primary_model': 'YOUR_FINE_TUNED_ROBERTA_CUAD'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    # For React routing, serve landing.html for unknown routes
    if request.path.startswith('/api/'):
        return jsonify({'error': 'API endpoint not found'}), 404
    else:
        try:
            return render_template('landing.html')
        except:
            return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/enhance_contract', methods=['POST'])
def enhance_contract():
    """Enhance contract analysis with visual risk highlighting"""
    print("🚀 ENHANCE ENDPOINT CALLED!")
    try:
        data = request.json
        print(f"📊 Received data: {data is not None}")
        if not data:
            print("❌ No data provided")
            return jsonify({'error': 'No data provided'}), 400
            
        contract_text = data.get('contract_text', '')
        contract_name = data.get('contract_name', 'Unnamed Contract')
        print(f"📋 Processing enhancement for: {contract_name}")
        print(f"📄 Contract text length: {len(contract_text)} characters")
        existing_analysis = data.get('existing_analysis', {})
        
        if not contract_text:
            return jsonify({'error': 'Contract text is required'}), 400
        
        print(f"Starting enhancement for contract: {contract_name}")
        
        # STEP 1: Always run YOUR model analysis first
        print("🤖 Step 1: Running YOUR fine-tuned RoBERTa analysis...")
        
        # Get comprehensive analysis from YOUR model
        if existing_analysis and 'risk_assessment' in existing_analysis:
            print("✅ Using existing analysis from YOUR model")
            your_model_analysis = existing_analysis
            risk_assessment = existing_analysis['risk_assessment']
        else:
            print("🔄 Running fresh analysis with YOUR fine-tuned model...")
            # Run complete analysis with YOUR model
            your_model_analysis = enhanced_analyzer.analyze_contract_comprehensive(contract_text)
            risk_assessment = your_model_analysis.get('risk_assessment', {})
        
        # STEP 2: Use Groq API for simple summary and detailed highlighting
        print("⚡ Step 2: Getting Groq enhancement...")
        
        # Initialize Groq enhancer specifically for enhancement
        groq_summary = None
        groq_highlighting = None
        
        try:
            from groq_enhancement import GroqEnhancement
            groq_enhancer = GroqEnhancement()
            
            if groq_enhancer.is_available():
                print("✅ Groq API available, getting enhancements...")
                
                print("🔍 Getting simple summary from Groq...")
                groq_summary_result = groq_enhancer.enhance_analysis(contract_text, "simple_summary")
                groq_summary = groq_summary_result.get('analysis', None) if groq_summary_result else None
                
                print("🎨 Getting detailed highlighting from Groq...")
                groq_highlighting_result = groq_enhancer.enhance_analysis(contract_text, "risk_highlighting")
                groq_highlighting = groq_highlighting_result.get('analysis', None) if groq_highlighting_result else None
                
                print("✅ Groq enhancements completed successfully")
            else:
                print("⚠️ Groq API key not available")
                
        except Exception as e:
            print(f"⚠️ Groq enhancement failed: {str(e)}")
            import traceback
            traceback.print_exc()
            groq_summary = None
            groq_highlighting = None
        
        # STEP 3: Combine YOUR model results with Groq enhancements
        enhanced_result = {
            "contract_name": contract_name,
            "your_model_analysis": {
                "complete_analysis": your_model_analysis,
                "risk_assessment": risk_assessment,
                "risk_score": risk_assessment.get('risk_score', 0),
                "overall_risk": risk_assessment.get('overall_risk', 'LOW'),
                "contract_type": your_model_analysis.get('contract_type', 'Unknown'),
                "cuad_analysis": your_model_analysis.get('cuad_analysis', {}),
                "high_risk": risk_assessment.get('high_risk', []),
                "medium_risk": risk_assessment.get('medium_risk', []),
                "low_risk": risk_assessment.get('low_risk', [])
            },
            "groq_simple_summary": groq_summary,
            "groq_detailed_highlighting": groq_highlighting,
            "highlighted_contract": generate_highlighted_contract(contract_text, risk_assessment, groq_highlighting),
            "enhancement_summary": generate_enhancement_summary(risk_assessment, groq_highlighting, groq_summary),
            "model_used": "YOUR_FINE_TUNED_ROBERTA + GROQ_ENHANCEMENT",
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(enhanced_result)
        
    except Exception as e:
        print(f"Enhancement endpoint error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Enhancement failed: {str(e)}'}), 500

@app.route('/contract-creation')
def contract_creation():
    """Contract Creation interface - Dynamic Wizard"""
    return render_template('contract_creation_dynamic.html')

@app.route('/api/create_contract', methods=['POST'])
def create_contract():
    """Create a new contract using RoBERTa + Groq AI"""
    print("🚀 CONTRACT CREATION ENDPOINT CALLED!")
    try:
        data = request.json
        print(f"📊 Received contract parameters: {data is not None}")
        
        if not data:
            return jsonify({'error': 'No contract parameters provided'}), 400
        
        # Initialize contract creator
        creator = ContractCreator()
        
        if not creator.available:
            return jsonify({
                'error': 'Contract creation service unavailable. Groq API key required.',
                'success': False
            }), 503
        
        # Create the contract
        print("📄 Generating contract...")
        creation_result = creator.create_contract(data)
        
        if not creation_result['success']:
            return jsonify(creation_result), 500
        
        # Analyze the generated contract with YOUR RoBERTa model
        print("🤖 Analyzing generated contract with YOUR fine-tuned model...")
        contract_text = creation_result['contract']
        risk_analysis = creator.analyze_contract_risks(contract_text)
        
        # Combine results
        final_result = {
            **creation_result,
            'risk_analysis': risk_analysis,
            'analysis_engine': 'YOUR_FINE_TUNED_ROBERTA',
            'generation_engine': f"GROQ_{creation_result.get('model_used', 'UNKNOWN')}",
            'combined_analysis': True
        }
        
        print("✅ Contract creation and analysis completed!")
        return jsonify(final_result)
        
    except Exception as e:
        print(f"❌ Contract creation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Contract creation failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/share_contract_whatsapp', methods=['POST'])
def share_contract_whatsapp():
    """Share generated contract via WhatsApp"""
    print("📱 WHATSAPP SHARING ENDPOINT CALLED!")
    try:
        data = request.json
        print(f"📊 Received sharing data: {data is not None}")
        
        if not data:
            return jsonify({'error': 'No sharing data provided'}), 400
        
        contract_data = data.get('contract_data')
        recipient_info = data.get('recipient_info', {})
        sharing_method = data.get('sharing_method', 'whatsapp_web')
        
        if not contract_data:
            return jsonify({'error': 'No contract data provided'}), 400
        
        if not recipient_info.get('phone'):
            return jsonify({'error': 'Recipient phone number required'}), 400
        
        # Initialize WhatsApp sender
        sender = WhatsAppContractSender()
        
        # Create sharing options
        print("📱 Creating WhatsApp sharing options...")
        sharing_options = sender.create_contract_sharing_options(contract_data, recipient_info)
        
        # Handle specific sharing methods
        result = {
            'success': True,
            'sharing_options': sharing_options,
            'recipient': recipient_info.get('name', 'Client'),
            'phone': recipient_info.get('phone'),
            'message': 'WhatsApp sharing options generated successfully!'
        }
        
        # If advanced sending is requested and available
        if sharing_method == 'send_now':
            advanced_sender = AdvancedWhatsAppSender()
            if advanced_sender.available:
                send_result = advanced_sender.schedule_contract_message(
                    recipient_info.get('phone'),
                    contract_data,
                    send_time_minutes=1  # Send in 1 minute
                )
                result['advanced_sending'] = send_result
            else:
                result['advanced_sending'] = {
                    'success': False,
                    'error': 'Advanced sending not available - use WhatsApp Web option'
                }
        
        print("✅ WhatsApp sharing options created!")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ WhatsApp sharing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'WhatsApp sharing failed: {str(e)}',
            'success': False
        }), 500

def generate_highlighted_contract(contract_text, risk_assessment, groq_highlighting):
    """Generate HTML with highlighted risk areas"""
    try:
        highlighted_html = contract_text
        
        # Define color classes for different risk levels
        risk_colors = {
            'high': 'background-color: #ffebee; border-left: 4px solid #f44336; padding: 2px 4px; margin: 1px;',
            'medium': 'background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 2px 4px; margin: 1px;',
            'low': 'background-color: #e8f5e8; border-left: 4px solid #4caf50; padding: 2px 4px; margin: 1px;',
            'neutral': 'background-color: #f5f5f5; border-left: 4px solid #9e9e9e; padding: 2px 4px; margin: 1px;'
        }
        
        # First, highlight based on YOUR model's risk assessment
        high_risk_terms = [
            "unlimited liability", "no termination", "perpetual", "irrevocable", 
            "exclusive rights", "no warranty", "class action waiver"
        ]
        
        medium_risk_terms = [
            "arbitration", "automatic renewal", "third party", "modify unilaterally",
            "governing law", "indemnification"
        ]
        
        low_risk_terms = [
            "limited liability", "30 days notice", "clear termination", 
            "specific payment terms", "data protection"
        ]
        
        # Apply highlighting for YOUR model's findings
        for term in high_risk_terms:
            if term.lower() in contract_text.lower():
                highlighted_html = highlighted_html.replace(
                    term, 
                    f'<span style="{risk_colors["high"]}" title="High Risk: {term}">{term}</span>'
                )
        
        for term in medium_risk_terms:
            if term.lower() in contract_text.lower():
                highlighted_html = highlighted_html.replace(
                    term, 
                    f'<span style="{risk_colors["medium"]}" title="Medium Risk: {term}">{term}</span>'
                )
        
        for term in low_risk_terms:
            if term.lower() in contract_text.lower():
                highlighted_html = highlighted_html.replace(
                    term, 
                    f'<span style="{risk_colors["low"]}" title="Low Risk: {term}">{term}</span>'
                )
        
        # Add Groq enhancements if available
        if groq_highlighting and isinstance(groq_highlighting, dict):
            try:
                if 'high_risk_segments' in groq_highlighting:
                    for segment in groq_highlighting['high_risk_segments']:
                        text = segment.get('text', '')
                        reason = segment.get('reason', 'High risk identified')
                        if text and text in highlighted_html:
                            highlighted_html = highlighted_html.replace(
                                text,
                                f'<span style="{risk_colors["high"]}" title="Groq Analysis: {reason}">{text}</span>'
                            )
                
                if 'medium_risk_segments' in groq_highlighting:
                    for segment in groq_highlighting['medium_risk_segments']:
                        text = segment.get('text', '')
                        reason = segment.get('reason', 'Medium risk identified')
                        if text and text in highlighted_html:
                            highlighted_html = highlighted_html.replace(
                                text,
                                f'<span style="{risk_colors["medium"]}" title="Groq Analysis: {reason}">{text}</span>'
                            )
                
                if 'low_risk_segments' in groq_highlighting:
                    for segment in groq_highlighting['low_risk_segments']:
                        text = segment.get('text', '')
                        reason = segment.get('reason', 'Low risk/safe clause')
                        if text and text in highlighted_html:
                            highlighted_html = highlighted_html.replace(
                                text,
                                f'<span style="{risk_colors["low"]}" title="Groq Analysis: {reason}">{text}</span>'
                            )
            except Exception as e:
                print(f"Error applying Groq highlights: {str(e)}")
        
        # Convert line breaks to HTML
        highlighted_html = highlighted_html.replace('\n', '<br>')
        
        return highlighted_html
        
    except Exception as e:
        print(f"Error generating highlighted contract: {str(e)}")
        return contract_text.replace('\n', '<br>')

def generate_enhancement_summary(risk_assessment, groq_highlighting, groq_simple_summary):
    """Generate summary of the enhancement analysis"""
    summary = {
        "your_model_findings": {
            "total_risks_found": len(risk_assessment.get('high_risk', [])) + len(risk_assessment.get('medium_risk', [])),
            "risk_score": risk_assessment.get('risk_score', 0),
            "primary_concerns": risk_assessment.get('high_risk', [])[:3]  # Top 3 high risks
        },
        "groq_simple_summary": groq_simple_summary if groq_simple_summary else "Simple summary not available",
        "groq_enhancement": {
            "available": groq_highlighting is not None,
            "additional_insights": "Detailed segment-level risk analysis" if groq_highlighting else "Not available"
        },
        "enhancement_benefits": [
            "Simple plain-English summary from Groq AI",
            "Visual highlighting of risk areas", 
            "Detailed explanations for each risk segment",
            "Combined analysis from YOUR fine-tuned model and Groq AI",
            "Interactive risk exploration"
        ]
    }
    
    if groq_highlighting and isinstance(groq_highlighting, dict):
        summary["groq_enhancement"]["segments_analyzed"] = (
            len(groq_highlighting.get('high_risk_segments', [])) +
            len(groq_highlighting.get('medium_risk_segments', [])) +
            len(groq_highlighting.get('low_risk_segments', []))
        )
    
    return summary

# Initialize the enhanced analyzer system
print("Initializing enhanced contract analysis system...")
load_enhanced_system()

if __name__ == '__main__':
    print("🚀 Starting Unified Contract Analysis Server...")
    print("📊 Landing Page: http://localhost:5000")
    print("🔍 Contract Analysis: http://localhost:5000/contract-analysis")
    print("💡 Uses YOUR fine-tuned RoBERTa model as primary engine")
    print("⚡ Optional Groq enhancement available")
    app.run(host='0.0.0.0', port=5000, debug=True)
