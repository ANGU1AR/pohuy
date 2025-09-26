# Building Detection API (Backend)

## Описание
Микросервис для автоматизации определения координат (WGS84) и адресов зданий на фотоматериалах из БПЛА, КИНС, соцсетей. Основан на ТЗ: распознавание bbox с ИНС (YOLO + Places365 для архитектуры/ландшафтов/signs), геопривязка (EXIF + Yandex Vision/Geocoder), экспорт XLSX, импорт ZIP, поиск bidirectional (coords ↔️ photo, до 5 фото, filters: time/source/resolution/score), история запросов, скачивание (presigned URLs). Интеграция Yandex Cloud (Storage/Vision/Geocoder). Масштабируемость: Celery для 176k объектов 2x/месяц. Безопасность: JWT, разграничение по users.

## Для Frontend Devs
- Split Screen: Left - data (table with filters, history), right - photos (thumbnails/previews from /search, up to 5, chrono order). Use Ag-Grid/TanStack for tables.
- Search Bidirectional: POST /search with lat/lon or address. Principle: "radius" (default), "time", "source". Filters in body.
- Preview Uploads: After POST /uploads, return thumbnail URLs (generate on backend if needed, but suggest client-side).
- Download: Use presigned URLs from responses (expires 1h).
- Maps: GET /maps/generate - returns Folium HTML (embed in iframe).
- Auth: POST /auth/register, /auth/token. Use JWT in headers.
- History: GET /search/history - list queries.
- Export: POST /export - returns XLSX URL.
- Integration: OpenAPI at /docs. Example: fetch('/uploads', {method: 'POST', body: formData}). For Yandex, no client-side needed.
- Errors: Handle 400/401/404, e.g., "Invalid format" for images.

## Установка
1. Git clone.
2. pip install -r requirements.txt
3. Setup .env (Yandex keys from cloud.yandex.ru, get API keys for Geocoder/Vision/Storage).
4. alembic init migrations; alembic revision --autogenerate -m "init"; alembic upgrade head
5. uvicorn app.main:app --reload
6. Celery: celery -A celery_worker worker -l info; celery -A celery_worker beat

Для PostGIS: Docker compose up db; psql -U user -d db -c "CREATE EXTENSION postgis;"

## API Endpoints (/docs for Swagger)
- Auth: /auth/register, /auth/token
- Uploads: POST /uploads - files/ZIP, any formats (Pillow convert), async Celery if batch.
- Search: POST /search - filters/principle, bidirectional, history auto-save.
- History: GET /search/history
- Maps: POST /maps/generate - Folium HTML with markers/heat.
- Export: POST /export - XLSX URL (columns per TZ).
- Download: GET /download/{task_id} - presigned photo.
- Admin: POST /admin/backdoor - reset (password-protected).

## Дообучение YOLO (на основе Ultralytics docs)
1. Подготовь dataset: YAML как data.yaml (classes: ['building'], train/val paths).
   - Используй Google Landmark: bash download-dataset.sh train 499 (5M images, filter Moscow landmarks).
   - Places365: torch.hub.load for scenes, fine-tune on urban/building categories.
   - NextGIS: Скачай GeoJSON для RU-MOW (buildings layer), annotate images.
2. Code:
`python
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
results = model.train(data='data.yaml', epochs=100, imgsz=640)