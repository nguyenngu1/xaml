import speech_recognition as sr
from gtts import gTTS
import os
import google.generativeai as genai

# Define API
GOOGLE_API_KEY = "AIzaSyBnBDcquhkJ1g3bX6ZH14yZzR87w-UtpD4"
genai.configure(api_key=GOOGLE_API_KEY)

# Define the model
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Initialize the recognizer
recognizer = sr.Recognizer()

# Keyword to trigger action and stop action
KEYWORD = "hey"
STOP_WORD = "goodbye"

# Function to handle speech-to-text
def speech_to_text():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        try:
            print("Listening...")
            audio = recognizer.listen(source)  # Listen to the microphone
            print("Processing...")
            text = recognizer.recognize_google(audio)  # Use Google's API to convert speech to text
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Error: Could not understand the audio")
        except sr.RequestError as e:
            print(f"Error: Could not request results from Google Speech Recognition service; {e}")
        return ""

# Function to check if recognized text contains the keyword
def contains_keyword(text, keyword):
    return keyword.lower() in text.lower()

# Function to convert text to speech
def text_to_speech(response_text):
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    os.system("start response.mp3")  # Voice KILL LAASY PRECESS id
    

# Function to get chatbot response
def get_chatbot_response(user_input):
    PROMPT = "Assume that your name is B and you are a children friend. Try to answer the question below in a simple way to children can understand easily and can have a conversation with the children. Do not add emoji in your answer, remember what did you answer last time. "
    # Send request and get the response
    response = model.generate_content(f"{PROMPT}. Question: {user_input}")
    return response.text

# Main loop to listen for keyword and respond
def main():
    print("Say 'hey buddy' to start interaction or 'goodbye' to stop...")
    
    while True:
        recognized_text = speech_to_text()
        if recognized_text:
            if contains_keyword(recognized_text, KEYWORD):
                print(f"Trigger word '{KEYWORD}' recognized. Listening for your input...")
                user_input = speech_to_text()
                if user_input:
                    print(f"You: {user_input}")
                    response = get_chatbot_response(user_input)
                    print(f"Buddy: {response}")
                    # Convert response to speech
                    text_to_speech(response)
            elif contains_keyword(recognized_text, STOP_WORD):
                text_to_speech("Goodbye. Have a nice day!")
                print("Goodbye. Have a nice day!")
                break

if __name__ == "__main__":
    main()
