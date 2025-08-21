# ctp-hackathon-2025

the option to record yourself <-- mp3 <-
^ we need to call the whisper api --> return json text
we send that json text to openai gpt model
this sends it to the web app (front end)

front end <--



steps:
0) basic front end with a button that lets you start and stop

1) option to record yourself

^^^^ later

step 1) hardcode audio mp3 file to call whisper to return json text - subah

step 2) json text into openai api model  (save whatever response) use 512x512  - atif (1024x1024 now since 512 isnt supported)

step 3) send response to frontend to display <-- last step

for later:

## Setup
1. Upgrade pip  
   `python3 -m pip install --upgrade pip`

2. Install system deps (ffmpeg)  
   - Mac: `brew install ffmpeg`  
   - Linux: `sudo apt-get install ffmpeg`  
   - Windows: [download ffmpeg.org binaries]

3. Install Python deps  
   `pip install -r requirements.txt`

4. Run transcription  
   `cd backend && python3 transcription.py`

