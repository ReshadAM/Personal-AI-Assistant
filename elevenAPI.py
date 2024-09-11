# Standard library imports
import warnings 
import os
# warning handling 
warnings.filterwarnings("ignore", category=UserWarning)



# Third-party imports
from dotenv import load_dotenv  
from elevenlabs import play, Voice, VoiceSettings  
from elevenlabs.client import ElevenLabs  



class ElevenAPI:


    def __init__(self) -> None:
        load_dotenv()
        
        ## ElevenLabs API integration

        self._client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))  # Eleven labs API key integration 


    def __str__(self) -> str:
        return "Eleven Labs API custom classs"
    

    # Generate Bruce Wayne's voice by calling on the Eleven labs API  
    def generate_voice(self,prompt) -> None:
        audio = self._client.generate(
            text = prompt,
            # Using a specefic audio log created in the eleven labs environment   
            voice=Voice(
                voice_id="ThT5KcBeYPX3keUQqHPh", # June's voice ID
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)

            ),
        
            model = "eleven_multilingual_v2"

        )

        play(audio)

