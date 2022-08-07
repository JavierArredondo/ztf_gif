from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from typing import List

import imageio
import os
import pandas as pd
import requests

PATH_FILE = os.path.dirname(os.path.abspath(__file__))
ARIAL_PATH = os.path.join(PATH_FILE, "arial.ttf")


def get_detections(oid: str) -> [dict, None]:
    url = f"https://api.alerce.online/ztf/v1/objects/{oid}/lightcurve"
    querystring = {"survey_id": "ztf"}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)
    if response.status_code == 200:
        data = response.json()
        detections = data["detections"]
        return detections
    return None


def get_stamp(oid: str, candid: str, source="science"):
    url = "https://avro.alerce.online/get_stamp"
    querystring = {"oid": oid, "candid": candid, "type": source, "format": "png"}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    return None


def make_gif(oid: str, path: str = "./") -> List:
    detections = get_detections(oid)
    detections = pd.DataFrame(detections)
    detections.sort_values(by="mjd", inplace=True, ascending=True)
    t_0 = detections["mjd"].values[0]
    stamps = []

    progress_bar = tqdm(detections.iterrows(), total=len(detections))
    for i, d in progress_bar:
        progress_bar.set_description(f"Retrieving {oid}: {d['candid']}")
        stamp = get_stamp(oid, d["candid"])
        if stamp is not None:
            draw = ImageDraw.Draw(stamp)
            font = ImageFont.truetype(ARIAL_PATH, 20)
            mjd = d["mjd"]
            delta = mjd - t_0
            mjd = f"{mjd:0.5f} Δ{delta:0.3f}"
            draw.text((10, 10), mjd, (255, 255, 255), font=font)
            stamps.append(stamp)
    output_path = os.path.join(path, f"{oid}.gif")
    imageio.mimsave(output_path, stamps, duration=0.5)
    return stamps
