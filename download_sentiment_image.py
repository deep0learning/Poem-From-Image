import sys, os, multiprocessing, csv
from urllib import request, error
from PIL import Image
from io import BytesIO
import json
import pandas as pd

out_dir = 'data/sentiment_image/'

def download_image(row):
    key = row[1]['id']
    url = row[1]['url']

    filename = os.path.join(out_dir, '{}.jpg'.format(key))

    if os.path.exists(filename):
        print('Image {} already exists. Skipping download.'.format(filename))
        return

    try:
        response = request.urlopen(url)
        if response.geturl() != url:
            print('Warning: Image {} unavailable'.format(key))
            return
        image_data = response.read()
    except:
        print('Warning: Could not download image {} from {}'.format(key, url))
        return

    try:
        pil_image = Image.open(BytesIO(image_data))
    except:
        print('Warning: Failed to parse image {}'.format(key))
        return

    try:
        pil_image_rgb = pil_image.convert('RGB')
    except:
        print('Warning: Failed to convert image {} to RGB'.format(key))
        return

    try:
        pil_image_rgb.save(filename, format='JPEG', quality=90)
    except:
        print('Warning: Failed to save image {}'.format(filename))
        return


if __name__ == '__main__':
    df = pd.read_csv('data/visual_sentiment_cat.csv')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    pool = multiprocessing.Pool(12)
    pool.map(download_image, df.iterrows())
    # for row in df.itertuples():
    #     pool.apply_async(download_image, args=(row))
    # pool.terminate()
    # pool.join()
