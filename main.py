from dotenv import load_dotenv
from datetime import datetime
import os
import openai
import requests
from ImageSize import ImageSize

load_dotenv()

openai.api_key = os.getenv('GPT_KEY')


def download_image(url: str, path_to_save: str) -> str:
    response = requests.get(url)

    generated_path = path_to_save + get_date() + ".png"

    if response.status_code == 200:  # Check if the request was successful
        with open(generated_path, 'wb') as f:
            f.write(response.content)
            f.flush()
            os.fsync(f.fileno())

    return generated_path


def add_image_url_to_file(url: str, filename: str):
    with open(filename, 'a') as f:
        f.write(url + '\n')
        f.flush()
        os.fsync(f.fileno())


def get_date() -> str:
    # Get the current date
    now = datetime.now()

    # Format the date
    formatted_date = f"{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"
    return formatted_date


def generate_image(generation_prompt: str, number_of_images: int, size: object) -> str:
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


def repl():
    while True:
        print("Enter a prompt for OpenAI to generate an image for. Type Help for other usage.")
        user_input = input("CLI: ").lower()
        if user_input == "help":
            print("Usage: ")
            print("\tType exit, quit, q, e to exit")
            input("Press Enter to continue...")
            os.system('cls||clear')
        elif user_input == "quit" or user_input == "q" or user_input == "exit" or user_input == "e":
            return
        else:
            print('Generating image for prompt: ' + user_input)
            response_url = generate_image(user_input, 1, ImageSize.LARGE)
            print('Image created at link: ' + response_url)
            print('Downloading image')
            image_location = download_image(response_url, 'images/')
            add_image_url_to_file(response_url, "url.txt")
            print('Finished image can be found at: ' + image_location)


if __name__ == '__main__':
    repl()
    print("Bye!")
