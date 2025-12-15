import os
import io
import base64
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Try to import analytics, but don't crash if it fails
try:
    from analytics import track_visit, track_generation, get_analytics_summary
    ANALYTICS_ENABLED = True
except Exception as e:
    print(f"Analytics disabled: {e}")
    ANALYTICS_ENABLED = False
    # Dummy functions if analytics fails
    def track_visit(*args, **kwargs): pass
    def track_generation(*args, **kwargs): pass
    def get_analytics_summary(): return {"error": "Analytics not available"}

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

# Create uploads directory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Serve static files
@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def styles():
    """Serve CSS file"""
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def scripts():
    """Serve JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon - return empty response"""
    return '', 204

@app.route('/analytics')
def analytics_dashboard():
    """Serve analytics dashboard HTML"""
    return send_from_directory('.', 'analytics_dashboard.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Track visit
    try:
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        track_visit(ip_address, user_agent)
    except Exception as e:
        print(f"Analytics tracking error: {e}")
    
    return jsonify({'status': 'healthy', 'message': 'Server is running'})

@app.route('/api/generate', methods=['POST'])
def generate_portrait():
    """Generate metallic portrait with Arabic calligraphy"""
    start_time = time.time()
    include_text_flag = False
    
    try:
        # Check if image and name are provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        if 'arabicName' not in request.form:
            return jsonify({'error': 'No Arabic name provided'}), 400
        
        image_file = request.files['image']
        arabic_name = request.form['arabicName']
        include_text = request.form.get('includeText', 'true').lower() == 'true'
        
        if image_file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Read and process the image
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert image to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Create the prompt based on whether text should be included
        if include_text:
            prompt = f"""Create a professional digital portrait artwork with the following specifications:

Art Style: Metallic silver/chrome illustration with dramatic lighting on a dark teal-to-black gradient background

Source: Use the provided image as the base for the portrait

Typography: Large, elegant 3D metallic Arabic calligraphy text displaying "{arabic_name}" positioned prominently below and slightly overlapping the portrait. The Arabic text should have:
- Polished chrome/silver finish
- Smooth, flowing calligraphic style
- 3D depth and dimension
- Subtle highlights and shadows

Overall Composition:
- Portrait positioned in upper center
- Artistic, sophisticated aesthetic
- High contrast between subject and dark background
- Professional branding/personal brand style
- Cinematic lighting emphasizing facial features
- Monochromatic silver/chrome color scheme

Technical specifications: High resolution, smooth metallic textures, professional graphic design quality"""
        else:
            prompt = f"""Create a professional digital portrait artwork with the following specifications:

Art Style: Metallic silver/chrome illustration with dramatic lighting on a dark teal-to-black gradient background

Source: Use the provided image as the base for the portrait

Overall Composition:
- Portrait positioned in center
- Artistic, sophisticated aesthetic
- High contrast between subject and dark background
- Professional branding/personal brand style
- Cinematic lighting emphasizing facial features
- Monochromatic silver/chrome color scheme
- NO TEXT OR TYPOGRAPHY - clean portrait only

Technical specifications: High resolution, smooth metallic textures, professional graphic design quality, no text overlays"""

        # Try to use the Gemini image generation model
        try:
            # Use Nano Banana Pro - this is the correct model for image generation!
            # Model name: nano-banana-pro-preview or gemini-3-pro-image-preview
            model = genai.GenerativeModel('nano-banana-pro-preview')
            
            # Generate content with the prompt and image
            response = model.generate_content(
                contents=[prompt, image]
            )
            
            # Extract image from response parts
            if hasattr(response, 'parts'):
                for part in response.parts:
                    # Check if this part contains image data
                    if hasattr(part, 'inline_data'):
                        mime_type = part.inline_data.mime_type
                        if mime_type and mime_type.startswith('image/'):
                            # Found the image!
                            img_base64 = base64.b64encode(part.inline_data.data).decode('utf-8')
                            
                            # Track successful generation
                            try:
                                processing_time = time.time() - start_time
                                track_generation(True, include_text_flag, None, processing_time)
                            except Exception as e:
                                print(f"Analytics error: {e}")
                            
                            return jsonify({
                                'success': True,
                                'image': f'data:{mime_type};base64,{img_base64}',
                                'message': 'Portrait generated successfully with Nano Banana Pro!'
                            })
            
            # If no image found in parts, check the response text
            if hasattr(response, 'text'):
                return jsonify({
                    'success': False,
                    'error': 'Model returned text instead of image',
                    'model_response': response.text[:500]
                }), 500
                
            return jsonify({
                'success': False,
                'error': 'No image data found in response',
                'response_info': str(response)[:500]
            }), 500
                
        except Exception as e:
            error_msg = str(e)
            print(f"Nano Banana Pro error: {error_msg}")
            
            # Try alternative model name
            try:
                print("Trying alternative model: gemini-3-pro-image-preview")
                model = genai.GenerativeModel('gemini-3-pro-image-preview')
                
                response = model.generate_content(
                    contents=[prompt, image]
                )
                
                # Extract image from response
                if hasattr(response, 'parts'):
                    for part in response.parts:
                        if hasattr(part, 'inline_data'):
                            mime_type = part.inline_data.mime_type
                            if mime_type and mime_type.startswith('image/'):
                                img_base64 = base64.b64encode(part.inline_data.data).decode('utf-8')
                                return jsonify({
                                    'success': True,
                                    'image': f'data:{mime_type};base64,{img_base64}',
                                    'message': 'Portrait generated successfully!'
                                })
                
                return jsonify({
                    'success': False,
                    'error': 'No image found in alternative model response'
                }), 500
                    
            except Exception as e2:
                error_msg2 = str(e2)
                print(f"Alternative model error: {error_msg2}")
                
                # Last resort fallback: return helpful error message
                return jsonify({
                    'success': False,
                    'error': 'Image generation failed',
                    'details': {
                        'primary_error': error_msg[:200],
                        'secondary_error': error_msg2[:200],
                        'models_tried': ['nano-banana-pro-preview', 'gemini-3-pro-image-preview'],
                        'suggestion': 'The models are available but may require specific configuration or permissions. Check API quotas and limits.'
                    }
                }), 500
            
    except Exception as e:
        # Track failed generation
        try:
            processing_time = time.time() - start_time
            track_generation(False, include_text_flag, str(e)[:200], processing_time)
        except:
            pass
        
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/analytics', methods=['GET'])
def analytics():
    """Get analytics summary - Simple auth with query parameter"""
    auth_key = request.args.get('key')
    if auth_key != os.getenv('ANALYTICS_KEY', 'metalise2025'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        stats = get_analytics_summary()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Arabic Portrait Generator Server...")
    print(f"📁 Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"🔑 API Key configured: {'Yes' if GEMINI_API_KEY else 'No'}")
    app.run(debug=True, host='0.0.0.0', port=5000)
