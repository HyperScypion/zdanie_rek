import io
import json
import flickrapi
import argparse
from database import db, ImageDB
from PIL import Image
import numpy as np
import cv2
from tqdm import tqdm
import requests
from pony.orm import *


API_KEY = ""
API_SECRET = ""

LOWER_RED_DOWN = np.array([0, 50, 50])
UPPER_RED_DOWN = np.array([10, 255, 255])

LOWER_RED_UP = np.array([170, 50, 50])
UPPER_RED_UP = np.array([180, 255, 255])

db.bind("sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)


parser = argparse.ArgumentParser(description="Download images from Flickr")
parser.add_argument("--keyword", type=str, help="Search for images based on keyword")
parser.add_argument(
    "--num", type=int, help="Number of images to be downloaded (default: 100)"
)
args = parser.parse_args()


def get_red(image):
    image = np.array(Image.open(io.BytesIO(image)))
    size = image.shape[0] * image.shape[1]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask0 = cv2.inRange(image, LOWER_RED_DOWN, UPPER_RED_DOWN)
    mask1 = cv2.inRange(image, LOWER_RED_UP, UPPER_RED_UP)
    mask = mask0 + mask1
    thresh = cv2.bitwise_and(image, image, mask=mask)
    red = np.count_nonzero(thresh)
    return round(red / size, 4)


@db_session
def get_max_red():
    _max = max(img.red for img in ImageDB)
    data = ImageDB.select(lambda img: img.red == _max)
    return data[0]


def enumerate_tqdm(y):
    i = 0
    for j in tqdm(y):
        yield i, j
        i += 1


@db_session
def parse_images(photos, num=100):
    for idx, photo in enumerate_tqdm(photos):
        if idx == num:
            break

        url = photo.get("url_c")
        if url is None:
            continue
        name = photo.get("title")
        image_string = requests.get(url).content
        red = get_red(image_string)
        ImageDB(name=name, image=image_string, red=red)
        db.commit()


if __name__ == "__main__":
    flick = flickrapi.FlickrAPI(API_KEY, API_SECRET)
    if args.keyword is not None:
        if args.num is not None:
            photos = flick.walk(
                text=args.keyword,
                tags=args.keyword,
                tag_mode="all",
                extras="url_c",
                per_page=100,
            )
            parse_images(photos, args.num)
        else:
            print("Wrong usage exiting...")
    else:
        params = {
            "api_key": API_KEY,
            "extras": "url_c",
            "per_page": 100,
            "format": "json",
        }

        photos = requests.get(
            f"https://www.flickr.com/services/rest/?method=flickr.photos.getRecent",
            params=params,
        ).content

    data = get_max_red()
    cv2.imshow("img", data.img)
    if cv2.waitKey(0) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
