# Premium Contract Analysis Platform

## 🚀 Overview

The Premium Contract Analysis Platform is an advanced AI-powered system for analyzing contracts, agreements, and legal documents. It combines the power of the fine-tuned CUAD (Contract Understanding Attentive Dataset) RoBERTa model with Groq API integration for comprehensive contract analysis, risk assessment, and compliance checking.

## ✨ Features

### Core Analysis Features
- **📄 Single Contract Analysis**: Comprehensive analysis of individual contracts
- **📚 Batch Processing**: Analyze multiple contracts simultaneously with comparative insights
- **⚖️ Contract Comparison**: Side-by-side comparison of two contracts with detailed differences
- **✅ Compliance Check**: App Store and Google Play compliance verification for mobile apps
- **🚨 Advanced Risk Assessment**: Detailed risk scoring with categorized findings

### Enhanced AI Capabilities
- **🤖 CUAD Model Integration**: Fine-tuned RoBERTa model for contract understanding
- **🧠 Groq API Enhancement**: Advanced AI analysis for deeper insights
- **📊 Multi-Model Validation**: Cross-validation between CUAD and Groq for accuracy
- **🎯 Specialized Prompts**: Optimized prompts for different contract types

### Web Interface Features
- **🌐 Modern Web UI**: Responsive, intuitive interface with tabbed navigation
- **📱 Mobile-Friendly**: Works on desktop, tablet, and mobile devices
- **🎨 Visual Results**: Color-coded risk levels, progress bars, and interactive elements
- **💾 Export Capabilities**: Generate and download detailed reports in Markdown format

### Advanced Features
- **🔍 Contract Type Detection**: Automatic identification of contract categories
- **📈 Risk Scoring**: Numerical risk assessment with detailed breakdown
- **💡 Recommendations**: AI-generated suggestions for contract improvements
- **🏪 App Store Compliance**: Specialized checks for iOS and Android app agreements
- **📋 Report Generation**: Comprehensive reports with executive summaries

## � Project Screenshots

### Live Application Interface

Here are the key interfaces and outputs of the AI Contract Platform:

#### 1. Platform Landing Page
![Platform Landing Page](./image1.jpg)
*Modern, responsive landing page showcasing the AI Contract Platform's capabilities and features*

#### 2. Contract Analysis Dashboard
![Contract Analysis Interface](./image2.jpg)
*Interactive contract analysis dashboard with upload functionality and real-time processing*

#### 3. AI Analysis Results
![Analysis Results Display](./image3.jpg)
*Comprehensive analysis results showing extracted contract terms, risk assessment, and AI insights*

#### 4. Advanced Features & Reports
![Advanced Features Interface](./image4.jpg)
*Advanced features including report generation, compliance checking, and detailed contract breakdowns*

### Key Visual Features Demonstrated:
- ✅ **Responsive Design**: Modern UI that works across all devices
- ✅ **Real-time Processing**: Live contract analysis with progress indicators
- ✅ **Interactive Results**: Color-coded risk levels and detailed findings
- ✅ **Professional Reports**: Clean, exportable analysis reports
- ✅ **User-friendly Interface**: Intuitive navigation and clear information hierarchy

## �🛠️ Installation & Setup

### Quick Start

1. **Run the setup script**:
   ```bash
   python setup_premium.py
   ```

2. **Start the web interface**:
   ```bash
   python premium_app.py
   ```

3. **Access the platform**:
   Open your browser and go to `http://localhost:5000`

### Manual Setup

1. **Install dependencies**:
   ```bash
   pip install torch transformers flask requests pandas numpy
   ```

2. **Set up Groq API** (optional but recommended):
   - Get your free API key from [Groq Console](https://console.groq.com/)
   - Set environment variable: `export GROQ_API_KEY=your_api_key`

3. **Verify model files**:
   Ensure you have the CUAD model files:
   - `config.json`
   - `pytorch_model.bin`
   - `tokenizer_config.json`
   - `vocab.json`
   - `merges.txt`

Then open your browser to `http://localhost:5000` to access the web interface where you can:
- Upload contract text
- Ask specific questions
- Get full contract analysis

### 3. Model Evaluation

Evaluate your model's performance:

```bash
python evaluate_model.py
```

This will show:
- Model statistics
- Prediction analysis
- Performance on sample data

## Model Capabilities

The model can extract various types of information from legal contracts:

- **Governing Law**: Which jurisdiction's laws govern the contract
- **Termination Clauses**: Conditions under which the contract can be terminated
- **Liability Provisions**: Limitations and allocations of liability
- **Payment Terms**: Payment schedules, amounts, and conditions
- **Intellectual Property**: IP ownership and licensing terms
- **Confidentiality**: Non-disclosure and confidentiality requirements
- **Force Majeure**: Extraordinary circumstances provisions
- **Warranty**: Warranties and guarantees provided
- **Dispute Resolution**: Methods for resolving disputes
- **Renewal Terms**: Contract renewal and extension conditions

## API Usage

### Single Question Analysis

```python
from transformers import RobertaTokenizer, RobertaForQuestionAnswering

tokenizer = RobertaTokenizer.from_pretrained('./')
model = RobertaForQuestionAnswering.from_pretrained('./')

context = "Your contract text here..."
question = "What are the payment terms?"

inputs = tokenizer.encode_plus(question, context, return_tensors='pt')
outputs = model(**inputs)
# Process outputs to get answer...
```

### Web API Endpoints

- `POST /analyze` - Analyze single question
- `POST /analyze_full` - Full contract analysis

## Performance Tips

1. **Text Length**: The model has a maximum sequence length of 512 tokens. For longer contracts, consider chunking the text.

2. **Question Formulation**: Use clear, specific questions for better results:
   - Good: "What are the payment terms?"
   - Better: "What is the payment schedule and amount?"

3. **Confidence Scores**: The model provides confidence scores. Lower scores may indicate:
   - The information isn't in the contract
   - The question is ambiguous
   - The text is unclear

## Customization

To adapt the model for other legal document types:

1. **Fine-tune further**: Use additional domain-specific data
2. **Adjust questions**: Modify the predefined questions in the scripts
3. **Post-processing**: Add domain-specific post-processing rules

## Next Steps

1. **Deploy to Production**: Use services like AWS, Azure, or Google Cloud
2. **Create API**: Build a RESTful API for integration
3. **Mobile App**: Develop mobile applications
4. **Integration**: Integrate with document management systems
5. **Batch Processing**: Process multiple contracts simultaneously

## Troubleshooting

**Common Issues:**

1. **Memory Errors**: Reduce batch size or text length
2. **Slow Performance**: Use GPU if available (`model.to('cuda')`)
3. **Poor Results**: Check if the contract language matches training data

## Model Limitations

- Trained primarily on English contracts
- Performance may vary with non-standard contract language
- Cannot understand context beyond the provided text
- May struggle with highly technical or domain-specific terms

## Citation

If you use this model, please cite the original CUAD paper:
```
@article{hendrycks2021cuad,
  title={CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review},
  author={Hendrycks, Dan and Burns, Collin and Chen, Anya and Ball, Spencer},
  journal={arXiv preprint arXiv:2103.06268},
  year={2021}
}
```
