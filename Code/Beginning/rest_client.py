from dotenv import load_dotenv
import os
import http.client, base64, json, urllib
from urllib import request, parse, error

def main():
    global ai_endpoint
    global ai_key

    try:
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        user_text = ''
        while user_text != 'quit':
            user_text = input('Enter your text to detect the language ("quit" to exit !)\n')
            if user_text != 'quit':
                get_language(user_text)
    except Exception as e:
        print('Something went wrong when processing your input text!!')

def get_language(user_text):
    try:
        jsonBody = {
            "Documents":[
                {
                    "id":1,
                    "text":user_text
                },
                {
                    "id":2,
                    "text":user_text.split(' ')[:-1]
                }
            ]
        }

        print(json.dumps(jsonBody, indent=2))

        uri = ai_endpoint.rstrip('/').replace('https://','')
        print(uri)
        conn = http.client.HTTPConnection(uri)

        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': ai_key
        }

        conn.request('POST', '/text/analytics/v3.1/languages?', str(jsonBody).encode('utf-8'), headers)

        response = conn.getresponse()
        data = response.read()

        if response.status == 200:
            results = json.loads(data)
            print(json.dumps(results, indent=2))

            for document in results['documents']:
                print(" The text is written in : ", document['detectedLanguage']['name'])

        else:
            print(data)
        conn.close()

    except Exception as e:
        print('Something went wrong when translating your text!!')


if __name__ == '__main__':
    main()