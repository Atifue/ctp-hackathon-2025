import whisper
import json
import os

def transcription():

    #the hardcoded audio
    base_dir = os.path.dirname(__file__)
    audio_dir = os.path.join(base_dir, "audio")

    #find first MP3 in audio folder if we want to test more
    mp3_files = [f for f in os.listdir(audio_dir) if f.lower().endswith(".mp3")]
    if not mp3_files:
        print("No MP3 files found in audio folder!")
        return
    audio_file = os.path.join(audio_dir, mp3_files[0])

    print(f"Using audio file: {audio_file}")

    #load in Whisper model
    model = whisper.load_model("small")  #small means fast allegedly
    result = model.transcribe(audio_file)

    text = result['text']
    print("\nTranscribed Audio:\n")
    print(text)

    #save transcript into JSON
    transcript_data = {"transcript": text}
    with open("transcript.json", "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, ensure_ascii=False, indent=4)

    print("\nTranscript saved to transcript.json")
    return text

if __name__ == "__main__":
    transcription()



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