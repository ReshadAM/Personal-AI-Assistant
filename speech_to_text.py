import speech_recognition as speech
import pyttsx3
import os
from dotenv import load_dotenv
import json

class speech_to_text_converter():

    def __init__(self) -> None:
        
        self._recogniser = speech.Recognizer()
        load_dotenv() # loads the enviortment variables from the .env file 
        google_API_credentials = os.getenv("GOOGLE_API_CREDENTIALS")

        if google_API_credentials:
            credentials_json = json.loads(google_API_credentials)
        else:
            raise ValueError("No GOOGLE_API_CREDENTIALS found in .env file")

        self._recogniser = speech.Recognizer()
        # Save the credentials to a temporary file (if required by the library)
        with open('temp_google_credentials.json', 'w') as temp_json_file:
            json.dump(credentials_json, temp_json_file)

        self.credentials_path = 'temp_google_credentials.json'

    # Using google clouds speech to text api to convert speech to text. 
    #* Returns a string containing the converted speech 
    def record_text(self) -> str:
        while True:
            try: 

                with speech.Microphone(device_index=1) as mic:
                    # prepare recogniser to recieve input 
                    self._recogniser.adjust_for_ambient_noise(mic, duration=0.5)
                    # listenes for the user's input 
                    audio = self._recogniser.listen(mic, timeout=5, phrase_time_limit=10) 

                    recived_text = self._recogniser.recognize_google_cloud(audio,credentials_json=self.credentials_path)
                    recived_text = recived_text.lower()
        
                    return recived_text

            # audio cannot be understood 
            except speech.RequestError as e:
                print("Could not request results: ", e)

            except speech.UnknownValueError:
                self._recogniser = speech.Recognizer()
                print("unknwon error occured") 
                continue
