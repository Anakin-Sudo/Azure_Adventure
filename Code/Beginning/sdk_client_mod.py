from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    global ai_endpoint, ai_key

    try:
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        user_text = ''
        while user_text != 'quit':
            user_text = input('Enter two lines of text so that we tell you the language in which it is written (enter "quit" to exit)\n')
            user_text_2 = input('')
            if user_text != 'quit' and user_text_2 != 'quit':
                languages = get_language(user_text, user_text_2)
                print(f'The Language of the first text is  : {languages[0]}\n The Language of the second text is :{languages[1]}')

    except Exception as e:
        print('Something went wrong processing your input')

def get_language(user_text, user_text_2):

    credential = AzureKeyCredential(ai_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

    detected_languages = client.detect_language(documents=[user_text, user_text_2])[0:2]
    actual_languages = []
    for detected_language in detected_languages:
        actual_languages.append(detected_language.primary_language.name)

    return actual_languages

if __name__ == '__main__':
    main()