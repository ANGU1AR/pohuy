from openpyxl import Workbook
from pathlib import Path
from typing import List
from models import Task
from services.storage import upload_to_yandex_storage, get_presigned_url


async def export_to_xlsx(tasks: List[Task], filename: str = "export.xlsx") -> str:
    wb = Workbook()
    ws = wb.active
    ws.append(["Фото (link)", "Здание ID", "Адрес", "Координаты (WGS84)"])

    for task in tasks:
        coords = f"{task.location.y}, {task.location.x}" if task.location else ""
        photo_link = await get_presigned_url(task.storage_key)
        ws.append([photo_link, task.id, task.address, coords])

    local_path = Path("exports") / filename
    wb.save(str(local_path))
    storage_key = await upload_to_yandex_storage(str(local_path))
    local_path.unlink()
    return await get_presigned_url(storage_key)