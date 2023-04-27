import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import openai
from gtts import gTTS
from io import BytesIO


voice_1 = AudioSegment.from_mp3("assets/audio/ja_mojo.mp3")
voice_2 = AudioSegment.from_mp3("assets/audio/lass_mich_das_überpruefen.mp3")

r1 = sr.Recognizer()
r2 = sr.Recognizer()

keyWord = "friday"

open_ai_key = "<your openAI API key>"


def request_ai(prompt):
    print("Prompt: " + prompt)
    print("Requesting ...")
    play(voice_2)
    completions = openai.Completion.create(model="text-davinci-002", prompt=prompt, max_tokens=1024, api_key=open_ai_key)
    message = completions.choices[0].text
    return message


def text_to_speech(text):
    mp3_fp = BytesIO()
    tts = gTTS(text=text, lang="de", tld="de", slow=False)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    playable_audio = AudioSegment.from_mp3(mp3_fp)
    play(playable_audio)


def rec():
    with sr.Microphone() as source:
        print("Listenig ...")
        play(voice_1)
        audio = r2.listen(source, timeout=10, phrase_time_limit=4)
    try:
        text = r2.recognize_google(audio, language="de-DE")
        message = request_ai(text)
        if message:
            text_to_speech(message)
    except Exception as e:
        print("Didn't understand.")


def activate():
    with sr.Microphone() as source:
        print("Please start speaking ...")
        while True:
            print("Check activation ...")
            activation_audio = r1.listen(source, timeout=10, phrase_time_limit=2)
            try:
                activation_text = r1.recognize_google(activation_audio, language="en-US")
                if keyWord.lower() in activation_text.lower():
                    rec()

            except Exception as e:
                print("Please speak again.")


def main():
    activate()


main()
