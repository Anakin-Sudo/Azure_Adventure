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
            user_text = input('Enter your text so that we tell you the language in which it is written (enter "quit" to exit)\n')
            if user_text !='quit':
                language = get_language(user_text)
                print(f'The Language is : {language}')

    except Exception as e:
        print('Something went wrong processing your input')

def get_language(user_text):

    credential = AzureKeyCredential(ai_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

    detected_language = client.detect_language(documents=[user_text])[0]
    return detected_language.primary_language.name

if __name__ == '__main__':
    main()