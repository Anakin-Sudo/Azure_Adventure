from dotenv import load_dotenv
import os
import sys
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from azure.core.exceptions import HttpResponseError
import requests
from http.client import HTTPSConnection
import requests

#Important imports relative to context

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def main():
    load_dotenv()
    ai_key = os.getenv('AI_SERVICE_KEY')
    ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')

    image_file = '/home/okaliagd/PycharmProjects/Azure_Adventure/Images/young_people_drinking.jpg'
    if len(sys.argv)>1:
        image_file = sys.argv[1]

    with open(image_file, 'rb') as im_file:
        image_data = im_file.read()

    credential = AzureKeyCredential(ai_key)
    cv_client = ImageAnalysisClient(endpoint=ai_endpoint, credential=credential)

    user_task = ''
    while (user_task != 'quit'):
        user_task = input(
            'Enter what you want to get from your image (captions, tags, object, people, bg to process backgroud, fg for foreground or type "quit" to exit !)\n')

        if user_task == 'bg' or user_task == 'fg':
            background_foreground_with_requests(ai_endpoint, ai_key, image_file, user_task)

        elif user_task != 'quit':
            analyze_image(image_file, image_data, cv_client, user_task)

def analyze_image(image_file, image_data, cv_client, task):

    result = cv_client.analyze(image_data=image_data, visual_features=[VisualFeatures.CAPTION, VisualFeatures.DENSE_CAPTIONS,
                                                                             VisualFeatures.TAGS, VisualFeatures.OBJECTS, VisualFeatures.PEOPLE])

    #Display analysis results

    #Get_Captions
    if task == 'captions':
        if result.caption is not None and result.dense_captions is not None:
            print(f'The caption for this image is : "{result.caption.text}", we are {result.caption.confidence*100:.2f}% sure about this !')
            print('More captions are :')
            for caption in result.dense_captions.list:
                print(f'"{caption.text}", {caption.confidence*100:.2f}% sure !')


    #Get_Tags
    if task == 'tags':
        if result.tags is not None:
            print('The tags we got for this image are : ')
            for tag in result.tags.list:
                print(f'"{tag.name}", {tag.confidence*100:.2f}% sure !')

    #Detect objects
    if task == 'objects':
        if result.objects is not None:

            #Remember box_plotting_in_image.py

            image = Image.open(image_file)
            fig = plt.figure(figsize=(image.width/100, image.height/100))
            plt.axis('off')

            draw = ImageDraw.Draw(image)
            color = 'cyan'

            for detected_object in result.objects.list:
                coordinates = detected_object.bounding_box
                bounding_box = ((coordinates.x, coordinates.y),(coordinates.x + coordinates.width, coordinates.y + coordinates.height))
                draw.rectangle(bounding_box, outline=color, width=5)
                plt.annotate(detected_object.tags[0].name, (coordinates.x, coordinates.y), backgroundcolor = color)

            plt.imshow(image)
            plt.tight_layout(pad=0)
            # plt.show()
            output_file_name = image_file.split('/')[-1].split('.')[0]+'_analysis.jpg'
            output_file = '/home/okaliagd/PycharmProjects/Azure_Adventure/Outputs/Object Detection/'+output_file_name
            fig.savefig(output_file)
            print('Result saved in', output_file)

    #Get_People
    if task == 'people':
        if result.people is not None:

            # Remember box_plotting_in_image.py
            image = Image.open(image_file)
            fig = plt.figure(figsize=(image.width / 100, image.height / 100))
            plt.axis('off')

            draw = ImageDraw.Draw(image)
            color = 'cyan'

            for detected_people in result.people.list:
                coordinates = detected_people.bounding_box
                bounding_box = ((coordinates.x, coordinates.y), (coordinates.x + coordinates.width, coordinates.y + coordinates.height))
                draw.rectangle(bounding_box, outline=color, width=5)
                #plt annotate is commented because there isn't any tag for people
                # plt.annotate(detected_object.tags[0].name, (coordinates.x, coordinates.y), backgroundcolor=color)

            plt.imshow(image)
            plt.tight_layout(pad=0)
            # plt.show()
            output_file_name = image_file.split('/')[-1].split('.')[0] + '_analysis.jpg'
            output_file = '/home/okaliagd/PycharmProjects/Azure_Adventure/Outputs/People Detection/' + output_file_name
            fig.savefig(output_file)
            print('Result saved in', output_file)

def background_foreground(ai_endpoint, ai_key, image_file, user_task):

    api_version = '2023-02-01-preview'
    if user_task == 'bg':
        mode = 'backgroundRemoval'
        output_file_name = image_file.split('/')[-1].split('.')[0] + '_background.jpg'
    elif user_task == 'fg':
        mode = 'foregroundMatting'
        output_file_name = image_file.split('/')[-1].split('.')[0] + '_foreground.jpg'

    with open(image_file, 'rb') as im_file:
        image_data = im_file.read()

    uri = ai_endpoint.rstrip('/').replace('https://', '')
    conn = HTTPSConnection(uri)

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': ai_key
    }
    conn.request(method='POST',url='/computervision/imageanalysis:segment?api-version={}&mode={}'.format(api_version,mode), body=image_data, headers=headers)
    response = conn.getresponse()
    if(response.status == 200):

        image = response.read()
        output_file = '/home/okaliagd/PycharmProjects/Azure_Adventure/Outputs/Background Foreground/'+output_file_name
        with open(output_file, 'wb') as out_file:
            out_file.write(image)
        print('Result saved in', output_file)

def background_foreground_with_requests(ai_endpoint, ai_key, image_file, user_task):

    api_version = '2023-02-01-preview'
    if user_task == 'bg':
        mode = 'backgroundRemoval'
        output_file_name = image_file.split('/')[-1].split('.')[0] + '_background.jpg'
    elif user_task == 'fg':
        mode = 'foregroundMatting'
        output_file_name = image_file.split('/')[-1].split('.')[0] + '_foreground.jpg'

    with open(image_file, 'rb') as im_file:
        image_data = im_file.read()

    url = ai_endpoint+ 'computervision/imageanalysis:segment?api-version={}&mode={}'.format(api_version,mode)

    # uri = ai_endpoint.rstrip('/').replace('https://', '')
    # conn = HTTPSConnection(uri)

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': ai_key
    }

    response = requests.post(url, data=image_data, headers=headers)
    # conn.request(method='POST',url='/computervision/imageanalysis:segment?api-version={}&mode={}'.format(api_version,mode), body=image_data, headers=headers)
    # response = conn.getresponse()

    if(response.status_code == 200):

        image = response.content
        output_file = '/home/okaliagd/PycharmProjects/Azure_Adventure/Outputs/Background Foreground/'+output_file_name
        with open(output_file, 'wb') as out_file:
            out_file.write(image)
        print('Result saved in', output_file)


if __name__ == '__main__':
    main()