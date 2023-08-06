import speech_recognition as speech
import pyttsx3
import datetime
import requests

converter = pyttsx3.init()


def text_to_speech(text):
    converter.say(text)
    converter.runAndWait()


def recognize_text():
    recognize_user_text = speech.Recognizer()
    with speech.Microphone as source:
        print("Listening to the Instruction...")
        recognize_user_text.adjust_for_ambient_noise(source)
        audio_instruction = recognize_user_text.listen(source)

    try:
        print("Recognizing the command...")
        instruction = recognize_user_text.recognize_google(audio_instruction)
        print(f"The instruction: {audio_instruction}")
        return instruction
    except speech.UnknownValueError:
        print("Sorry, I couldn't understand what you said. Please try again")
    except speech.RequestError as err:
        print(f"Error during speech recognition: {err}")
    return ""


def to_set_reminder():
    text_to_speech("What would you like me to remind you about, Sir?")
    reminder = recognize_text()
    if reminder:
        text_to_speech("Please specify the time when I should remind you about this")
        time = recognize_text()
        try:
            time_object = datetime.datetime.strptime(time, "%H:%M")
            present_time = datetime.datetime.now()
            if time_object.time() > present_time.time():
                seconds = (time_object-present_time).total_seconds()
                text_to_speech(f"I'll remind you in {int(seconds/60)} minutes.")
            else:
                text_to_speech("Are you complete dumb? The time has already passed.")
        except ValueError:
            text_to_speech("Sorry, I couldn't understand the time format that you mentioned.")


def create_to_do_list():
    array_of_list = []
    text_to_speech("Please add the tasks that you want to add.Say 'stop' when you are done.")
    while True:
        element = recognize_text()
        if element.lower() == "stop":
            break
        elif element:
            array_of_list.append(element)
            text_to_speech(f"Added '{element}' to your list.")
    if array_of_list:
        text_to_speech("Here is your final to-do-list:")
        for index,task in enumerate(array_of_list, 1):
            text_to_speech(f"{index}.{task}")



