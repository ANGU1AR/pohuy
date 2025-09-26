import folium
from folium.plugins import MiniMap, Fullscreen, HeatMap
from pathlib import Path


def generate_map(tasks: list, center=(55.7558, 37.6175), zoom=10) -> str:
    m = folium.Map(location=center, zoom_start=zoom)

    points = []
    for task in tasks:
        if task.latitude and task.longitude:
            folium.Marker(
                [task.latitude, task.longitude],
                popup=f"Адрес: {task.address}<br>Источник: {task.source}",
                icon=folium.Icon(color="red", icon="home")
            ).add_to(m)
            points.append([task.latitude, task.longitude])

    if points:
        HeatMap(points).add_to(m)

    MiniMap().add_to(m)
    Fullscreen().add_to(m)

    filepath = Path("static") / "map.html"
    m.save(str(filepath))
    return "/static/map.html"