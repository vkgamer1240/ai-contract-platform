"""
Premium Flask Web Interface with Advanced Contract Analysis Features
===================================================================
Includes batch processing, contract comparison, compliance checking, and detailed reporting
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import tempfile
from datetime import datetime
from enhanced_analyzer import EnhancedCUADAnalyzer
from advanced_features import AdvancedContractProcessor, create_sample_app_agreements

app = Flask(__name__)

# Global variables
enhanced_analyzer = None
processor = None

def load_enhanced_system():
    """Load the enhanced analyzer and processor"""
    global enhanced_analyzer, processor
    groq_api_key = os.getenv('GROQ_API_KEY')
    enhanced_analyzer = EnhancedCUADAnalyzer('./', groq_api_key=groq_api_key)
    processor = AdvancedContractProcessor(enhanced_analyzer)

@app.route('/')
def landing_page():
    """Landing page with service selection"""
    return render_template('landing.html')

@app.route('/analysis')
def analysis_page():
    """Contract analysis page"""
    return render_template('premium_index.html')

@app.route('/batch_analysis')
def batch_analysis_page():
    """Batch analysis interface"""
    return render_template('batch_analysis.html')

@app.route('/contract_comparison')
def comparison_page():
    """Contract comparison interface"""
    return render_template('contract_comparison.html')

@app.route('/compliance_check')
def compliance_page():
    """App store compliance checking interface"""
    return render_template('compliance_check.html')

# API Endpoints

@app.route('/api/analyze_single', methods=['POST'])
def analyze_single_contract():
    """Single contract comprehensive analysis"""
    data = request.json
    contract_text = data.get('contract_text', '')
    contract_name = data.get('contract_name', 'Unnamed Contract')
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    try:
        # Comprehensive analysis
        results = enhanced_analyzer.analyze_contract_comprehensive(contract_text)
        
        # Generate report
        report = processor.generate_contract_report(results, contract_name)
        
        return jsonify({
            'analysis': results,
            'report': report,
            'contract_name': contract_name,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
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

@app.route('/api/groq_analysis', methods=['POST'])
def groq_analysis():
    """Direct Groq API analysis"""
    data = request.json
    contract_text = data.get('contract_text', '')
    analysis_type = data.get('analysis_type', 'comprehensive')
    
    if not contract_text:
        return jsonify({'error': 'Contract text is required'}), 400
    
    try:
        groq_result = enhanced_analyzer.analyze_with_groq(contract_text, analysis_type)
        
        return jsonify({
            'groq_analysis': groq_result,
            'analysis_type': analysis_type,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Groq analysis failed: {str(e)}'}), 500

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
        'groq_available': enhanced_analyzer.groq_api_key is not None,
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == '__main__':
    # Load the enhanced system
    print("Loading Enhanced Contract Analysis System...")
    load_enhanced_system()
    print("System loaded successfully!")
    
    # Check if Groq API is available
    if enhanced_analyzer.groq_api_key:
        print("✅ Groq API is configured")
    else:
        print("⚠️  Groq API key not found - some features will be limited")
        print("   Set GROQ_API_KEY environment variable for full functionality")
    
    print("\nStarting Premium Contract Analysis Web Interface...")
    print("Available at: http://localhost:5000")
    print("\nFeatures available:")
    print("- Single contract analysis")
    print("- Batch contract processing")
    print("- Contract comparison")
    print("- App store compliance checking")
    print("- Risk assessment")
    print("- Report generation")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
