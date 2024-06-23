import speech_recognition as speech
import pyttsx3
import datetime
import requests
import os

converter = pyttsx3.init()


def text_to_speech(text):
    converter.say(text)
    converter.runAndWait()


def recognize_text():
    recognize_user_text = speech.Recognizer()
    with speech.Microphone() as source:
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


def perform_search(query):
    api_key = os.environ.get('API_KEY')
    search_engine_id = os.environ.get('SEARCH_ENGINE_ID')
    url = f'https://www.googleapis.com/customsearch/v1'
    params = {
        'key' : api_key,
        'cx' : search_engine_id,
        'q' : query,
        'num' : 3
    }

    try :
        response = requests.get(url, params=params)
        data = response.json()
        if 'items' in data:
            text_to_speech("Here are some search results:")
            for index,item in enumerate(data['items'],1):
                text_to_speech(f"{index} {item['title']}")
                text_to_speech(item['snippet'])
        else:
            text_to_speech("Sorry, I couldn't find out relevant search results.")
    except requests.RequestException as err:
        text_to_speech("Sorry, there was ana error in performing the search")

def main():
    text_to_speech("Hello! How can I assist you?")
    while True:
        command = recognize_text().lower()
        if "reminder" in command:
            to_set_reminder()
        elif "list" in command:
            create_to_do_list()
        elif "search" in command:
            query = command.replace("search", "").strip()
            if query:
                perform_search(query)
            else:
                text_to_speech("Please mention what would you like to search for?")
        elif "exit" in command:
            text_to_speech("Goodbye!")
            break
        else:
            text_to_speech("Sorry! I couldn't recognize that, Please try again")


if __name__=="__main__":
    main()
