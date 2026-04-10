"""
Программа для анализа данных call-центра.
Обрабатывает файл data.csv с информацией о входящих звонках.
"""

import os
import csv
from typing import List, Dict, Any


class CallRecord:
    """
    Класс для представления записи о звонке.
    """

    def __init__(self, call_id: int, phone: str, reason: str, is_resolved: bool):
        """
        Инициализация записи о звонке.

        Args:
            call_id: Номер звонка
            phone: Телефон звонящего
            reason: Причина обращения
            is_resolved: Решена проблема или нет
        """
        self.call_id = call_id
        self.phone = phone
        self.reason = reason
        self.is_resolved = is_resolved

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует запись в словарь для сохранения в CSV.

        Returns:
            Dict[str, Any]: Словарь с данными звонка
        """
        return {
            '№': self.call_id,
            'телефон': self.phone,
            'причина обращения': self.reason,
            'решена проблема': 'Да' if self.is_resolved else 'Нет'
        }

    def __repr__(self) -> str:
        """
        Строковое представление записи.

        Returns:
            str: Отформатированная строка с данными звонка
        """
        status = "Решена" if self.is_resolved else "Не решена"
        return f"№{self.call_id:3d} | {self.phone:15s} | {self.reason:30s} | {status}"


def count_files_in_directory(directory_path: str = ".") -> int:
    """
    Подсчитывает количество файлов в указанной директории.

    Args:
        directory_path: Путь к директории (по умолчанию текущая папка)

    Returns:
        int: Количество файлов в директории
    """
    try:
        # Проверяем, существует ли директория
        if not os.path.exists(directory_path):
            print(f"Ошибка: Директория '{directory_path}' не существует!")
            return 0

        # Подсчитываем количество файлов (исключая папки)
        file_count = 0
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                file_count += 1

        return file_count

    except PermissionError:
        print(f"Ошибка: Нет доступа к директории '{directory_path}'!")
        return 0
    except Exception as e:
        print(f"Ошибка при подсчете файлов: {e}")
        return 0


def load_calls_from_csv(filename: str = "data.csv") -> List[CallRecord]:
    """
    Загружает данные о звонках из CSV файла.

    Args:
        filename: Имя CSV файла

    Returns:
        List[CallRecord]: Список записей о звонках
    """
    calls = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Читаем CSV файл
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                # Извлекаем данные из строки
                call_id = int(row['№'])
                phone = row['телефон']
                reason = row['причина обращения']
                is_resolved = row['решена проблема'].strip().lower() in ['да', 'true', 'yes', '1']

                # Создаем объект CallRecord
                call = CallRecord(call_id, phone, reason, is_resolved)
                calls.append(call)

        print(f"Загружено {len(calls)} записей из файла '{filename}'")
        return calls

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден!")
        print("Создаю пример файла data.csv...")
        create_example_csv(filename)
        return load_calls_from_csv(filename)

    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return []


def create_example_csv(filename: str = "data.csv") -> None:
    """
    Создает пример CSV файла с данными о звонках.

    Args:
        filename: Имя файла для создания
    """
    example_data = [
        {'№': 1, 'телефон': '+7-912-345-67-89', 'причина обращения': 'Проблема с интернетом', 'решена проблема': 'Да'},
        {'№': 2, 'телефон': '+7-922-456-78-90', 'причина обращения': 'Не работает телевидение',
         'решена проблема': 'Нет'},
        {'№': 3, 'телефон': '+7-932-567-89-01', 'причина обращения': 'Смена тарифа', 'решена проблема': 'Да'},
        {'№': 4, 'телефон': '+7-942-678-90-12', 'причина обращения': 'Плохая связь', 'решена проблема': 'Да'},
        {'№': 5, 'телефон': '+7-952-789-01-23', 'причина обращения': 'Переезд и подключение', 'решена проблема': 'Нет'},
        {'№': 6, 'телефон': '+7-962-890-12-34', 'причина обращения': 'Проблема с интернетом', 'решена проблема': 'Да'},
        {'№': 7, 'телефон': '+7-972-901-23-45', 'причина обращения': 'Смена тарифа', 'решена проблема': 'Нет'},
        {'№': 8, 'телефон': '+7-982-012-34-56', 'причина обращения': 'Плохая связь', 'решена проблема': 'Да'},
        {'№': 9, 'телефон': '+7-992-123-45-67', 'причина обращения': 'Не работает телевидение',
         'решена проблема': 'Нет'},
        {'№': 10, 'телефон': '+7-902-234-56-78', 'причина обращения': 'Проблема с интернетом', 'решена проблема': 'Да'},
    ]

    try:
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['№', 'телефон', 'причина обращения', 'решена проблема']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(example_data)

        print(f"Создан пример файла '{filename}' с {len(example_data)} записями")

    except Exception as e:
        print(f"Ошибка при создании файла: {e}")


def sort_by_string_field(calls: List[CallRecord], field: str = 'phone') -> List[CallRecord]:
    """
    Сортирует звонки по строковому полю.

    Args:
        calls: Список звонков
        field: Поле для сортировки ('phone' или 'reason')

    Returns:
        List[CallRecord]: Отсортированный список
    """
    if field == 'phone':
        return sorted(calls, key=lambda x: x.phone)
    elif field == 'reason':
        return sorted(calls, key=lambda x: x.reason)
    else:
        print(f"Ошибка: Неизвестное поле '{field}'")
        return calls


def sort_by_numeric_field(calls: List[CallRecord]) -> List[CallRecord]:
    """
    Сортирует звонки по числовому полю (номер звонка).

    Args:
        calls: Список звонков

    Returns:
        List[CallRecord]: Отсортированный список
    """
    return sorted(calls, key=lambda x: x.call_id)


def filter_by_criteria(calls: List[CallRecord], resolved_status: bool = None,
                       reason_filter: str = None) -> List[CallRecord]:
    """
    Фильтрует звонки по заданному критерию.

    Args:
        calls: Список звонков
        resolved_status: Статус решения проблемы (True - решена, False - не решена)
        reason_filter: Фильтр по причине обращения

    Returns:
        List[CallRecord]: Отфильтрованный список
    """
    filtered_calls = calls.copy()

    if resolved_status is not None:
        filtered_calls = [call for call in filtered_calls if call.is_resolved == resolved_status]

    if reason_filter:
        filtered_calls = [call for call in filtered_calls if reason_filter.lower() in call.reason.lower()]

    return filtered_calls


def save_calls_to_csv(calls: List[CallRecord], filename: str = "data.csv") -> bool:
    """
    Сохраняет данные о звонках в CSV файл.

    Args:
        calls: Список звонков
        filename: Имя файла для сохранения

    Returns:
        bool: True если сохранение успешно, False в противном случае
    """
    try:
        # Создаем резервную копию
        if os.path.exists(filename):
            backup_name = filename.replace('.csv', '_backup.csv')
            with open(filename, 'r', encoding='utf-8') as src:
                with open(backup_name, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"Создана резервная копия: {backup_name}")

        # Сохраняем данные
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['№', 'телефон', 'причина обращения', 'решена проблема']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for call in calls:
                writer.writerow(call.to_dict())

        print(f"Данные успешно сохранены в файл '{filename}'")
        return True

    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False


def add_new_call(calls: List[CallRecord]) -> List[CallRecord]:
    """
    Добавляет новый звонок в список.

    Args:
        calls: Список звонков

    Returns:
        List[CallRecord]: Обновленный список звонков
    """
    print("\n--- Добавление нового звонка ---")

    try:
        # Определяем новый ID
        new_id = max([call.call_id for call in calls], default=0) + 1

        # Вводим телефон
        phone = input("Введите номер телефона: ").strip()
        if not phone:
            print("Ошибка: Телефон не может быть пустым!")
            return calls

        # Вводим причину обращения
        reason = input("Введите причину обращения: ").strip()
        if not reason:
            print("Ошибка: Причина обращения не может быть пустой!")
            return calls

        # Вводим статус решения
        while True:
            resolved_input = input("Проблема решена? (да/нет): ").strip().lower()
            if resolved_input in ['да', 'yes', 'true', '1', 'д']:
                is_resolved = True
                break
            elif resolved_input in ['нет', 'no', 'false', '0', 'н']:
                is_resolved = False
                break
            else:
                print("Пожалуйста, введите 'да' или 'нет'")

        # Создаем новую запись
        new_call = CallRecord(new_id, phone, reason, is_resolved)
        calls.append(new_call)

        print(f"✓ Звонок №{new_id} успешно добавлен!")

    except Exception as e:
        print(f"Ошибка при добавлении звонка: {e}")

    return calls


def display_calls(calls: List[CallRecord], title: str = "Список звонков") -> None:
    """
    Отображает список звонков на экране.

    Args:
        calls: Список звонков
        title: Заголовок для вывода
    """
    print(f"\n{'=' * 80}")
    print(f"{title}")
    print(f"{'=' * 80}")

    if not calls:
        print("Нет данных для отображения")
        return

    print(f"{'№':3s} | {'Телефон':15s} | {'Причина обращения':30s} | {'Статус':10s}")
    print(f"{'-' * 80}")

    for call in calls:
        status = "Решена" if call.is_resolved else "Не решена"
        print(f"{call.call_id:3d} | {call.phone:15s} | {call.reason:30s} | {status}")

    print(f"{'=' * 80}")

    # Выводим статистику
    total = len(calls)
    resolved = sum(1 for call in calls if call.is_resolved)
    unresolved = total - resolved

    print(f"\nСтатистика:")
    print(f"  Всего звонков: {total}")
    print(f"  Решено проблем: {resolved} ({resolved / total * 100:.1f}%)")
    print(f"  Не решено: {unresolved} ({unresolved / total * 100:.1f}%)")


def main():
    """
    Главная функция программы.
    """
    print("=" * 80)
    print("ПРОГРАММА АНАЛИЗА ДАННЫХ CALL-ЦЕНТРА")
    print("=" * 80)

    # Задание 1: Подсчет файлов в директории
    print("\n--- ЗАДАНИЕ 1: Подсчет файлов в директории ---")
    current_dir = input("Введите путь к директории (Enter для текущей папки): ").strip()
    if not current_dir:
        current_dir = "."

    file_count = count_files_in_directory(current_dir)
    print(f"В директории '{current_dir}' найдено файлов: {file_count}")

    # Задание 2: Работа с CSV файлом
    print("\n--- ЗАДАНИЕ 2: Работа с данными call-центра ---")

    # Загружаем данные
    calls = load_calls_from_csv("data.csv")

    if not calls:
        print("Нет данных для обработки. Программа завершена.")
        return

    # 2.1 Сортировка по строковому полю (телефон)
    display_calls(calls, "Исходные данные")

    print("\n--- 2.1 Сортировка по строковому полю (телефон) ---")
    sorted_by_phone = sort_by_string_field(calls, 'phone')
    display_calls(sorted_by_phone, "Сортировка по номеру телефона")

    print("\n--- 2.1 Сортировка по строковому полю (причина обращения) ---")
    sorted_by_reason = sort_by_string_field(calls, 'reason')
    display_calls(sorted_by_reason, "Сортировка по причине обращения")

    # 2.2 Сортировка по числовому полю (номер звонка)
    print("\n--- 2.2 Сортировка по числовому полю (номер звонка) ---")
    sorted_by_id = sort_by_numeric_field(calls)
    display_calls(sorted_by_id, "Сортировка по номеру звонка")

    # 2.3 Фильтрация по критерию (проблема решена)
    print("\n--- 2.3 Фильтрация по критерию ---")

    # Фильтр: решенные проблемы
    resolved_calls = filter_by_criteria(calls, resolved_status=True)
    display_calls(resolved_calls, "Звонки с РЕШЕННЫМИ проблемами")

    # Фильтр: нерешенные проблемы
    unresolved_calls = filter_by_criteria(calls, resolved_status=False)
    display_calls(unresolved_calls, "Звонки с НЕРЕШЕННЫМИ проблемами")

    # Фильтр по причине обращения
    reason_filter = input("\nВведите причину обращения для фильтрации (или Enter для пропуска): ").strip()
    if reason_filter:
        filtered_by_reason = filter_by_criteria(calls, reason_filter=reason_filter)
        display_calls(filtered_by_reason, f"Звонки с причиной '{reason_filter}'")

    # Задание 3: Добавление новых данных и сохранение
    print("\n--- ЗАДАНИЕ 3: Добавление новых данных ---")

    while True:
        add_more = input("\nХотите добавить новый звонок? (да/нет): ").strip().lower()
        if add_more in ['да', 'yes', 'д', 'y']:
            calls = add_new_call(calls)
        elif add_more in ['нет', 'no', 'н', 'n']:
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'")

    # Сохраняем изменения
    print("\n--- Сохранение данных ---")
    save_choice = input("Сохранить изменения в файл data.csv? (да/нет): ").strip().lower()

    if save_choice in ['да', 'yes', 'д', 'y']:
        if save_calls_to_csv(calls, "data.csv"):
            print("✓ Данные успешно сохранены!")

            # Показываем обновленные данные
            print("\nОбновленные данные:")
            display_calls(calls, "ИТОГОВЫЙ СПИСОК ЗВОНКОВ")
    else:
        print("Изменения не сохранены.")

    print("\n" + "=" * 80)
    print("ПРОГРАММА ЗАВЕРШЕНА")
    print("=" * 80)


# Точка входа в программу
if __name__ == "__main__":
    main()