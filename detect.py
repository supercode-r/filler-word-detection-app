import time
from threading import Thread

# Expanded filler word list - add more based on research or user input!
filler_words = [
    "um", "uh", "ah", "er", "like", "you know", "so", "basically", 
    "actually", "literally", "kinda", "sorta", "well", "right"
]

def speech_callback(transcription):
    """
    Process transcribed speech and trigger vibration if filler words are detected.
    """
    if not transcription:  # Handle empty transcriptions
        return
    
    words = transcription.lower().split()
    for word in words:
        # Strip punctuation in case speech-to-text includes it (e.g., "um,")
        word = word.strip(".,!?")
        if word in filler_words:
            print(f"Filler word detected: '{word}'")
            vibrate_device()
            # Add a tiny delay to avoid spamming vibrations if multiple fillers hit at once
            time.sleep(0.2)

def vibrate_device():
    """
    Trigger device vibration - this would be platform-specific.
    For Android (via Python with Kivy/PyJNIus) or iOS (via PyObjC), you'd call native APIs.
    """
    try:
        # Placeholder for actual vibration code
        # Android example with PyJNIus:
        # from jnius import autoclass
        # Vibrator = autoclass('android.os.Vibrator')
        # vibrator = context.getSystemService(Context.VIBRATOR_SERVICE)
        # vibrator.vibrate(100)  # Vibrate for 100ms
        print("Vibrating...")
    except Exception as e:
        print(f"Vibration failed: {e}")

def start_speech_recognition():
    """
    Start real-time speech recognition and pass results to callback.
    Using something like Google's Speech Recognition API or PocketSphinx for offline use.
    """
    try:
        # Simulated speech input for now (replace with real mic input)
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Listening for speech...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Calibrate for noise
            while True:
                audio = recognizer.listen(source, timeout=None)
                try:
                    transcription = recognizer.recognize_google(audio)  # Or use recognize_sphinx for offline
                    print(f"Heard: {transcription}")
                    speech_callback(transcription)
                except sr.UnknownValueError:
                    print("Couldn’t understand the audio")
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
    except Exception as e:
        print(f"Error starting recognition: {e}")

# Run the recognition in a separate thread so it doesn’t block
if __name__ == "__main__":
    recognition_thread = Thread(target=start_speech_recognition)
    recognition_thread.daemon = True  # Stops when main program exits
    recognition_thread.start()

    # Keep the main thread alive (e.g., for a GUI or app loop)
    while True:
        time.sleep(1)
