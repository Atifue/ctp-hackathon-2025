from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
from transcription import transcription
from image_gen import image_gen
import json

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:3000"])

# Make sure outputs directory exists
OUTPUTS_DIR = "outputs"
if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Test endpoint
@app.route('/test')
def test():
    return jsonify({"status": "Backend is working!", "message": "Connection successful"})

@app.route('/api/create-story', methods=['POST'])
def create_story():
    try:
        print("Received request to create story")
        
        # Check if audio file is in request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        print(f"Received audio file: {audio_file.filename}")
        
        # Save temporary audio file
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
        audio_file.save(temp_audio.name)
        print(f"Saved temp audio to: {temp_audio.name}")
        
        # Step 1: Transcribe audio
        print("Starting transcription...")
        transcript = transcription(temp_audio.name)
        
        if not transcript:
            os.unlink(temp_audio.name)  # Clean up
            return jsonify({'error': 'Could not transcribe audio. Please try recording again.'}), 400
        
        print(f"Transcription successful: {transcript}")
        
        # Step 2: Generate story and images
        print("Starting story and image generation...")
        
        # Make sure transcript.json exists for image_gen
        transcript_json_path = os.path.join(os.path.dirname(__file__), 'transcript.json')
        
        story_data = image_gen(transcript_json_path)
        
        if not story_data:
            os.unlink(temp_audio.name)  # Clean up
            return jsonify({'error': 'Could not generate story. Please try again.'}), 500
        
        print(f"Generated {len(story_data)} pages")
        
        # Clean up temp file
        os.unlink(temp_audio.name)
        
        # Return success response
        return jsonify({
            'success': True,
            'transcript': transcript,
            'pages': story_data,
            'message': 'Story created successfully!'
        })
        
    except Exception as e:
        print(f"Error in create_story: {str(e)}")
        
        # Clean up temp file if it exists
        try:
            if 'temp_audio' in locals():
                os.unlink(temp_audio.name)
        except:
            pass
            
        return jsonify({
            'error': f'Server error: {str(e)}',
            'success': False
        }), 500

@app.route('/outputs/<filename>')
def serve_image(filename):
    """Serve generated images"""
    try:
        return send_from_directory(OUTPUTS_DIR, filename)
    except Exception as e:
        return jsonify({'error': 'Image not found'}), 404

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'whisper': 'loaded',
        'openai': 'configured' if os.environ.get('OPENAI_API_KEY') else 'missing_key'
    })

if __name__ == '__main__':
    # Check if OpenAI API key is set
    if not os.environ.get('OPENAI_API_KEY'):
        print("⚠️  WARNING: OPENAI_API_KEY not found in environment!")
        print("   Make sure your .env file is set up correctly.")
    
    print("🚀 Starting Story Maker backend...")
    print("📡 Frontend should connect to: http://localhost:5000")
    
    app.run(debug=True, port=5002, host='0.0.0.0')