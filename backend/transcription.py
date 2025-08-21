import whisper
import json
import os


def transcription(audio_file_path=None):
   """
   Transcribe audio file using Whisper
   Args:
       audio_file_path: Path to audio file (supports MP3, WebM, WAV, etc.)
   Returns:
       Transcribed text string
   """
  
   if audio_file_path:
       # Use provided file path
       audio_file = audio_file_path
       if not os.path.exists(audio_file):
           print(f"Audio file not found: {audio_file}")
           return None
   else:
       # Fallback to hardcoded logic for testing
       base_dir = os.path.dirname(__file__)
       audio_dir = os.path.join(base_dir, "audio")
      
       if not os.path.exists(audio_dir):
           print("Audio directory not found!")
           return None
          
       mp3_files = [f for f in os.listdir(audio_dir) if f.lower().endswith((".mp3", ".webm", ".wav"))]
       if not mp3_files:
           print("No audio files found in audio folder!")
           return None
       audio_file = os.path.join(audio_dir, mp3_files[0])


   print(f"Using audio file: {audio_file}")


   try:
       # Load Whisper model
       model = whisper.load_model("small")  # small for speed
       result = model.transcribe(audio_file)


       text = result['text'].strip()
       print("\nTranscribed Audio:")
       print(text)


       # Save transcript to JSON (for image_gen compatibility)
       transcript_data = {"transcript": text}
       transcript_path = os.path.join(os.path.dirname(__file__), "transcript.json")
       with open(transcript_path, "w", encoding="utf-8") as f:
           json.dump(transcript_data, f, ensure_ascii=False, indent=4)


       print(f"\nTranscript saved to {transcript_path}")
       return text
      
   except Exception as e:
       print(f"Error during transcription: {e}")
       return None


if __name__ == "__main__":
   # Test with hardcoded file
   result = transcription()
   if result:
       print("Transcription successful!")
   else:
       print("Transcription failed!")




"""
INSGTALL BEFORE RUNNING. APPARENTLTY. idk if i got a virus or .

 # install pip
python3 -m pip install --upgrade pip

# 2️Install torch and whisper in user environment
python3 -m pip install --user torch
python3 -m pip install --user git+https://github.com/openai/whisper.git

# install Homebrew (required for FFmpeg) 
which brew >/dev/null 2>&1 || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

#follow the directions given in terminal^

# install FFmpeg via Homebrew
brew install ffmpeg

# run (on mac)
cd backend
python3 transcription.py


"""