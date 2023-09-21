import speech_recognition as sr
import requests
import pygame
import wave
import numpy as np
import base64
from gtts import gTTS
import os


class Speech:
    @staticmethod
    def transcribe_audio():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print(" Listening...")
            audio = recognizer.listen(source)

        try:
            input_text = recognizer.recognize_google(audio)
            return input_text.strip()
        except sr.UnknownValueError:
            return ""

    @staticmethod
    def text_to_speech(text):
        CHUNK_SIZE = 1024

        emily = "LcfcDJNUP1GQjkzn1xUU"
        bella = "EXAVITQu4vr4xnSDxMaL"
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{bella}/stream"

        headers = {
            "xi-api-key": "59bcf2b6780c78c17ef45ee7f58881c9",
        }

        data = {
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
        }

        response = requests.post(url, json=data, headers=headers)

        output_filename = "reply.mp3"
        with open(output_filename, "wb") as output:
            output.write(response.content)

        # output_filename="output.wav"

        # # Decode the audio content from base64
        # audio_content = np.frombuffer(base64.b64decode(response), dtype=np.int16)

        # # Open the WAV file in write mode
        # with open(output_filename, 'wb') as wav_file:
        #     # Set the parameters
        #     sample_width = 2  # 16-bit audio
        #     sample_rate = 44100  # Replace with the appropriate sample rate
        #     num_channels = 1  # Mono audio

        #     wav_file.setparams((num_channels, sample_width, sample_rate, 0, 'NONE', 'not compressed'))

        #     # Write the audio data
        #     wav_file.writeframes(audio_content.tobytes())

        # Initialize pygame mixer
        pygame.mixer.init()
        try:
            # Load the audio file
            pygame.mixer.music.load(output_filename)

            # Play the audio
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except pygame.error as e:
            print("Error loading MP3 file:", str(e))

        finally:
            # Clean up and remove the temporary audio file
            pygame.mixer.quit()
            os.remove(output_filename)

    @staticmethod
    def synthesize_and_play_speech(response_text):
        # Convert text to speech
        tts = gTTS(text=response_text, lang="en")
        tts.save("response.mp3")

        # Initialize pygame mixer
        pygame.mixer.init()

        try:
            # Load the audio file
            pygame.mixer.music.load("response.mp3")

            # Play the audio
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        finally:
            # Clean up and remove the temporary audio file
            pygame.mixer.quit()
            os.remove("response.mp3")
