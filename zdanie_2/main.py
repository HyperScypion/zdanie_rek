import io
import flickrapi
import argparse
import numpy as np

from tqdm import tqdm
import requests


API_KEY = "1"
API_SECRET = ""

parser = argparse.ArgumentParser(description="Download images from Flickr")
parser.add_argument("--keyword", type=str, help="Search for images based on keyword")
parser.add_argument(
    "--num", type=int, help="Number of images to be downloaded (default: 100)"
)
args = parser.parse_args()


def save_image(img_string):
    image_array = np.array(io.BytesIO(img_string))


def enumerate_tqdm(y):
    i = 0
    for j in tqdm(y):
        yield i, j
        i += 1


def parse_images(photos, num=100):
    for idx, photo in enumerate_tqdm(photos):
        if idx == num:
            break

        url = photo.get("url_c")
        image_string = requests.get(url).content
        with open(f"{args.keyword}_{idx}.jpg", "wb") as fopen:
            fopen.write(image_string)


if __name__ == "__main__":
    flick = flickrapi.FlickrAPI(API_KEY, API_SECRET)
    if args.keyword is not None:
        if args.num is not None:
            photos = flick.walk(
                text=args.keyword, tag_mode="all", extras="url_c", per_page=100
            )
            print("photos")
            parse_images(photos)
