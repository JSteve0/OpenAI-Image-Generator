from dotenv import load_dotenv
from datetime import datetime
import os
import openai
import requests

load_dotenv()

openai.api_key = os.getenv('GPT_KEY')


def download_image(url, path_to_save):
    response = requests.get(url)

    if response.status_code == 200:  # Check if the request was successful
        with open(path_to_save + get_date() + ".png", 'wb') as f:
            f.write(response.content)


def add_image_url_to_file(url, filename):
    with open(filename, 'a') as f:
        f.write(url + '\n')


def get_date():
    # Get the current date
    now = datetime.now()

    # Format the date
    formatted_date = f"{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"
    return formatted_date


def generate_image(generation_prompt: object, number_of_images: object, size: object) -> object:
    try:
        response = openai.Image.create(
            prompt=generation_prompt,
            n=number_of_images,
            size=size
        )
        return response['data'][0]['url']
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)


if __name__ == '__main__':
    print('Generating image')
    response_url = generate_image("hyper-realistic image of the universe", 1, "1024x1024")
    print('Downloading image')
    download_image(response_url, 'images/')
    add_image_url_to_file(response_url, "url.txt")
    print('Finished')
