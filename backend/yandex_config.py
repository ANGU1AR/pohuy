import os
import json
import requests
from typing import Dict, Optional


class YandexAuthManager:
    def __init__(self, config_file: str = "yandex_config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Загружает конфиг из файла"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_config(self):
        """Сохраняет конфиг в файл"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def setup_auth(self):
        """Интерактивная настройка ключей"""
        print("🎯 Настройка Yandex Cloud API")
        print("=" * 40)

        # Запрашиваем ключи
        self.config['YANDEX_API_KEY'] = input("YCONmRhTVqdYi8FWbinzKDIA39JgsgqI44By_Jbt").strip()
        self.config['YANDEX_VISION_KEY'] = input("YCAJEd6AzCYnqZkIpl3J1Ys8p").strip()
        self.config['YANDEX_STORAGE_BUCKET'] = input("starlirabacket").strip()
        self.config['YANDEX_STORAGE_ACCESS_KEY'] = input("YCAJEskB6LaooHZk4aAyugQPt").strip()
        self.config['YANDEX_STORAGE_SECRET_KEY'] = input("YCO5jx8QVHsEO7jyqep_CnsbhJVKzkSHKKn5jsoH").strip()

        self._save_config()
        self._create_env_file()

        print("✅ Ключи сохранены!")
        return self.config

    def _create_env_file(self):
        """Создает .env файл"""
        env_content = f"""YANDEX_API_KEY={self.config['YANDEX_API_KEY']}
YANDEX_VISION_KEY={self.config['YANDEX_VISION_KEY']}
YANDEX_STORAGE_BUCKET={self.config['YANDEX_STORAGE_BUCKET']}
YANDEX_STORAGE_ACCESS_KEY={self.config['YANDEX_STORAGE_ACCESS_KEY']}
YANDEX_STORAGE_SECRET_KEY={self.config['YANDEX_STORAGE_SECRET_KEY']}
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
"""
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)

    def get_vision_key(self) -> str:
        """Возвращает ключ для Vision API"""
        return self.config.get('YANDEX_VISION_KEY', '')

    def get_storage_keys(self) -> tuple:
        """Возвращает ключи для Storage"""
        return (
            self.config.get('YANDEX_STORAGE_ACCESS_KEY', ''),
            self.config.get('YANDEX_STORAGE_SECRET_KEY', ''),
            self.config.get('YANDEX_STORAGE_BUCKET', '')
        )


def check_vision_key(key: str) -> bool:
    """Проверяет валидность Vision API ключа"""
    try:
        response = requests.post(
            'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze',
            headers={'Authorization': f'Api-Key {key}'},
            json={'folder_id': 'test', 'analyze_specs': [{}]},
            timeout=5
        )
        return response.status_code != 401
    except:
        return False


    return None


def config_manager():
    return None


def yandex_config():
    return None