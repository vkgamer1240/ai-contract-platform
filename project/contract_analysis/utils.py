import os
import docx2txt
import PyPDF2
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_key)

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type")

def analyze_contract(contract_text):
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal AI assistant. Analyze the contract for potential loopholes, legal risks, and areas of concern. Provide a structured analysis with specific recommendations."
                },
                {
                    "role": "user",
                    "content": f"Please analyze this contract:\n\n{contract_text}"
                }
            ],
            temperature=0.2,
        )
        
        analysis = response.choices[0].message.content
        
        return {
            "success": True,
            "analysis": analysis,
            "summary": {
                "total_risks": len([line for line in analysis.split('\n') if 'risk' in line.lower() or 'loophole' in line.lower()]),
                "severity": "medium" if "high risk" in analysis.lower() else "low" if "low risk" in analysis.lower() else "medium"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis": "Unable to analyze contract due to an error."
        } 