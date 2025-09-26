from geopy.geocoders import Yandex
from geopy.distance import geodesic
from utils.exif import extract_exif_coords
from yandexcloud import SDK  # Yandex Vision
from os import getenv
import requests  # For IM2GPS-like matching (dummy)

yandex_key = getenv("YANDEX_API_KEY")
vision_key = getenv("YANDEX_VISION_KEY")
sdk = SDK(iam_token=vision_key)  # Setup per docs

def get_coords_from_image(file_path: str, metadata: dict) -> tuple:
    coords = extract_exif_coords(metadata)
    if coords:
        return coords
    # Yandex Vision OCR for signs
    with open(file_path, "rb") as f:
        response = sdk.vision().analyze(f.read(), features=["TEXT_DETECTION"])
    # Extract location hints from text
    # IM2GPS: Match scene to landmark DB (e.g., Google Landmark)
    return (55.7558, 37.6175)  # Fallback

def get_address_from_coords(latitude: float, longitude: float) -> str:
    geocoder = Yandex(api_key=yandex_key)
    location = geocoder.reverse((latitude, longitude))
    return location.address if location else "Not found"

def get_coords_from_address(address: str) -> tuple:
    geocoder = Yandex(api_key=yandex_key)
    location = geocoder.geocode(address)
    return (location.latitude, location.longitude) if location else None

def calculate_distance(coord1: tuple, coord2: tuple) -> float:
    return geodesic(coord1, coord2).meters