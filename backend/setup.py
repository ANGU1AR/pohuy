#!/usr/bin/env python3
from yandex_config import yandex_config  # Импортируем экземпляр, а не класс


def main():
    print("🚀 Настройка конфигурации Yandex Cloud")
    print("=" * 50)

    if yandex_config.check_config_exists():
        print("Найдена существующая конфигурация")
        choice = input("Хотите перезаписать? (y/n): ")
        if choice.lower() != 'y':
            print("Настройка отменена")
            return

    yandex_config.setup_auth()
    print("\n✅ Настройка завершена! Запускайте: python main.py")


if __name__ == "__main__":
    main()