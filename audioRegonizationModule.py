import speech_recognition as sr


def voice_to_text():

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Adjust for ambient noise
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)

    # Capture audio from the microphone
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=6)
        except sr.WaitTimeoutError:
            return "No speech detected. Please try again."
    try:
        text = recognizer.recognize_google(audio)
        print("Inference complete.")
        return text
    
    except sr.UnknownValueError:
        return "Could not understand the audio. Please speak clearly."
    except sr.RequestError as e:
        return f"Could not request results from Google Web Speech API; {e}"
    

