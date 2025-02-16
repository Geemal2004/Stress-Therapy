from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from gtts import gTTS
import os
from config import GROQ_API_KEY, MODEL_NAME

class ChatHandler:
    def __init__(self):
        self.chat_instance = self._setup_groq()

    def _setup_groq(self):
        """Initialize the Groq client"""
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=MODEL_NAME
        )

    def process_message(self, text):
        """Process user message and return AI response"""
        try:
            messages = [
                SystemMessage(content="""
                You are a compassionate AI therapist designed to help users manage stress.
                Provide caring, supportive responses with practical advice for stress management.
                Keep responses concise and focused on immediate relief strategies.
                """),
                HumanMessage(content=text)
            ]

            # Get AI response
            response = self.chat_instance.invoke(messages)
            
            # Convert to speech
            audio_file = self._text_to_speech(response.content)
            
            return {
                'text_response': response.content,
                'audio_file': audio_file
            }

        except Exception as e:
            raise Exception(f"Error processing message: {str(e)}")

    def _text_to_speech(self, text):
        """Convert text to speech and save as audio file"""
        try:
            audio_file = 'response.mp3'
            tts = gTTS(text=text, lang='en')
            tts.save(audio_file)
            return audio_file
        except Exception as e:
            raise Exception(f"Error converting text to speech: {str(e)}")