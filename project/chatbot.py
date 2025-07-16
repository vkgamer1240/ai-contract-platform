from flask import Flask, render_template, request, jsonify, send_from_directory
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from diffusers import DiffusionPipeline
import torch
import re
import os
import time
from PIL import Image, ImageDraw, ImageFont

app = Flask(_name_, static_folder='static')

print(f"Is CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Current device: {torch.cuda.current_device()}")
    print(f"Device name: {torch.cuda.get_device_name(torch.cuda.current_device())}")

print("Loading models...")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load fine-tuned Phi-2 model
llm_model_name = "microsoft/phi-2"
finetuned_model_path = "./phi2_finetuned"

print("Loading fine-tuned Phi-2 model...")
try:
    # Check if fine-tuned model exists
    if os.path.exists(finetuned_model_path):
        print("Loading fine-tuned model with LoRA adapter...")
        
        # Load tokenizer
        llm_tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
        if llm_tokenizer.pad_token is None:
            llm_tokenizer.pad_token = llm_tokenizer.eos_token
        
        # Configure quantization for inference
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        
        # Load base model with quantization
        llm_model = AutoModelForCausalLM.from_pretrained(
            llm_model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16
        )
        
        # Load LoRA adapter
        llm_model = PeftModel.from_pretrained(llm_model, finetuned_model_path)
        print("✅ Fine-tuned model loaded successfully!")
        
    else:
        print("Fine-tuned model not found, loading base model...")
        llm_tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
        llm_model = AutoModelForCausalLM.from_pretrained(
            llm_model_name,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
        print("✅ Base model loaded successfully!")
        
except Exception as e:
    print(f"Error loading model: {e}")
    print("Falling back to base model...")
    llm_tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
    llm_model = AutoModelForCausalLM.from_pretrained(
        llm_model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )

print("Loading image generation model...")
try:
    print("Loading existing Stable Diffusion model...")
    image_pipeline = DiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16,
    )
    print("Model loaded successfully!")
    
    if torch.cuda.is_available():
        print("Moving model to GPU...")
        image_pipeline = image_pipeline.to("cuda")
        print(f"Model loaded on GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("Using CPU for image generation (will be slower)")
        image_pipeline.enable_attention_slicing()
    
    IMAGE_GENERATION_AVAILABLE = True
    print("Image generation model loaded successfully!")
except Exception as e:
    print(f"Image generation model not loaded: {e}")
    IMAGE_GENERATION_AVAILABLE = False

print("Loading FAISS index and texts...")
index = faiss.read_index('rag_index.faiss')
with open('rag_texts.pkl', 'rb') as f:
    texts = pickle.load(f)

def retrieve(query, k=2, max_tokens=1000):
    query_embedding = embed_model.encode(query).reshape(1, -1)
    distances, indices = index.search(query_embedding, k)
    retrieved_chunks = []
    total_tokens = 0
    
    for idx in indices[0]:
        chunk = texts[idx]
        chunk_tokens = len(llm_tokenizer.encode(chunk))
        if total_tokens + chunk_tokens > max_tokens:
            break
        retrieved_chunks.append(chunk)
        total_tokens += chunk_tokens
    
    return retrieved_chunks

# Format prompt for fine-tuned model
def format_prompt(context_chunks, user_query):
    context = "\n\n".join(context_chunks)
    prompt = f"""You are a friendly teacher chatbot for kids (age 8-12). Answer the question clearly and simply.

Context:
{context}

Question: {user_query}
Answer:"""
    return prompt

# Generate answer with fine-tuned model
def generate_answer(prompt, max_tokens=512):
    inputs = llm_tokenizer(prompt, return_tensors="pt").to(llm_model.device)
    
    with torch.no_grad():
        outputs = llm_model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            pad_token_id=llm_tokenizer.eos_token_id,
            repetition_penalty=1.1
        )
    
    answer = llm_tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the answer part
    if "Answer:" in answer:
        answer = answer.split("Answer:")[-1].strip()
    else:
        # If no "Answer:" found, take everything after the prompt
        answer = answer[len(prompt):].strip()
    
    return answer

def generate_simple_image(prompt, filename):
    """Generate a simple text-based image as fallback"""
    try:
        # Create a simple image with text
        width, height = 400, 300
        image = Image.new('RGB', (width, height), color='lightblue')
        draw = ImageDraw.Draw(image)
        
        # Add a border
        draw.rectangle([0, 0, width-1, height-1], outline='darkblue', width=3)
        
        # Add text
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Split text into lines
        words = prompt.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + word) < 30:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        # Draw text
        y_position = 50
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) // 2
            draw.text((x_position, y_position), line, fill='darkblue', font=font)
            y_position += 30
        
        # Add a simple icon
        draw.ellipse([150, 200, 250, 250], fill='orange', outline='darkorange', width=2)
        
        # Save the image
        image_path = f"static/{filename}"
        image.save(image_path)
        return f"/static/{filename}", None
        
    except Exception as e:
        return None, f"Error creating simple image: {str(e)}"

def generate_image(prompt, filename=None):
    """Generate an image from a text prompt"""
    print(f"Attempting to generate image for: {prompt}")
    
    # Generate unique filename
    if filename is None:
        filename = f"generated_image_{int(time.time())}.png"
    
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)
    
    if not IMAGE_GENERATION_AVAILABLE:
        print("AI image generation not available, using simple fallback")
        return generate_simple_image(prompt, filename)
    
    try:
        # Clean and enhance the prompt for better image generation
        enhanced_prompt = f"simple, colorful, {prompt}, digital art"
        print(f"Enhanced prompt: {enhanced_prompt}")
        
        # Generate the image with GPU acceleration
        print("Generating AI image on GPU...")
        image = image_pipeline(
            enhanced_prompt,
            num_inference_steps=30,  # Increased steps for better quality on GPU
            guidance_scale=7.5
        ).images[0]
        print("AI image generated successfully!")
        
        # Save the image
        image_path = f"static/{filename}"
        print(f"Saving image to: {image_path}")
        image.save(image_path)
        print(f"Image saved successfully!")
        
        return f"/static/{filename}", None
    except Exception as e:
        print(f"AI image generation failed: {str(e)}")
        print("Trying simple fallback image...")
        return generate_simple_image(prompt, filename)

def detect_image_request(user_query):
    """Detect if user wants an image generated"""
    image_keywords = [
        'draw', 'picture', 'image', 'photo', 'illustration', 'art', 'painting',
        'show me', 'create', 'generate', 'make', 'visual', 'see', 'look like',
        'draw me', 'picture of', 'image of', 'photo of', 'paint', 'sketch'
    ]
    
    query_lower = user_query.lower()
    print(f"🔍 Checking for image request in: {query_lower}")
    
    # Check for image keywords
    for keyword in image_keywords:
        if keyword in query_lower:
            print(f"Found image keyword: {keyword}")
            return True
    
    # Check for specific patterns
    patterns = [
        r'draw\s+(?:me\s+)?(?:a\s+)?(.+)',
        r'picture\s+of\s+(.+)',
        r'image\s+of\s+(.+)',
        r'show\s+me\s+(?:a\s+)?(.+)',
        r'create\s+(?:a\s+)?(.+)',
        r'generate\s+(?:a\s+)?(.+)',
        r'paint\s+(?:me\s+)?(?:a\s+)?(.+)',
        r'sketch\s+(?:me\s+)?(?:a\s+)?(.+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query_lower)
        if match:
            print(f"Found image pattern: {pattern}")
            return True
    
    print("No image request detected")
    return False

def extract_image_prompt(user_query):
    """Extract the image description from user query"""
    query_lower = user_query.lower()
    
    # Remove common prefixes
    prefixes_to_remove = [
        'draw me', 'draw a', 'picture of', 'image of', 'photo of',
        'show me', 'create a', 'generate a', 'make a', 'visual of'
    ]
    
    for prefix in prefixes_to_remove:
        if query_lower.startswith(prefix):
            return user_query[len(prefix):].strip()
    
    # If no prefix found, return the whole query
    return user_query.strip()

def get_chatbot_response(user_query):
    # Check if user wants an image generated
    wants_image = detect_image_request(user_query)
    
    # Regular text response
    chunks = retrieve(user_query)
    prompt = format_prompt(chunks, user_query)
    response = generate_answer(prompt)
    
    # Return both response and image flag
    return response, wants_image

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    print(f"Received message: {user_message}")
    
    try:
        response, wants_image = get_chatbot_response(user_message)
        print(f"Response: {response}")
        print(f"Wants image: {wants_image}")
        
        # Only generate image if user specifically requests it
        if wants_image and IMAGE_GENERATION_AVAILABLE:
            print("User requested image, generating...")
            image_prompt = extract_image_prompt(user_message)
            print(f"Image prompt: {image_prompt}")
            
            image_path, error = generate_image(image_prompt)
            if not error:
                print(f"Image generated successfully: {image_path}")
                response_data = {
                    'response': response,
                    'image_path': image_path,
                    'is_image': True
                }
                print(f"Sending response: {response_data}")
                return jsonify(response_data)
            else:
                print(f"Image generation failed: {error}")
        
        # No image requested or image generation failed
        response_data = {'response': response, 'is_image': False}
        print(f"📤 Sending response: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/test-image')
def test_image():
    """Test endpoint to check if image generation is working"""
    if not IMAGE_GENERATION_AVAILABLE:
        return jsonify({'error': 'Image generation not available'})
    
    try:
        image_path, error = generate_image("a simple red circle")
        if error:
            return jsonify({'error': error})
        return jsonify({'success': True, 'image_path': image_path})
    except Exception as e:
        return jsonify({'error': str(e)})

if _name_ == '_main_':
    print("Chatbot is ready!")
    app.run(debug=True)