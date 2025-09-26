import exifread

def extract_metadata(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        tags = exifread.process_file(f)
    return {k: str(v) for k, v in tags.items()}

def extract_exif_coords(metadata: dict) -> tuple:
    if "GPS GPSLatitude" in metadata and "GPS GPSLongitude" in metadata:
        lat = eval(metadata["GPS GPSLatitude"])
        lon = eval(metadata["GPS GPSLongitude"])
        return (lat[0] + lat[1]/60 + lat[2]/3600, lon[0] + lon[1]/60 + lon[2]/3600)
    return None