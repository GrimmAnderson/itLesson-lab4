"""

"""

import os
import csv
from typing import List, Dict, Any, Iterator, Optional
from datetime import datetime


class BaseRecord:
    """
    Базовый класс для всех записей.
    Демонстрирует наследование.
    """

    def __init__(self, record_id: int):
        """
        Инициализация базовой записи.

        Args:
            record_id: Идентификатор записи
        """
        self._record_id = record_id
        self._created_at = datetime.now()

    def get_id(self) -> int:
        """Возвращает идентификатор записи."""
        return self._record_id

    def get_creation_time(self) -> datetime:
        """Возвращает время создания записи."""
        return self._created_at

    def __repr__(self) -> str:
        """Перегрузка repr для базового класса."""
        return f"BaseRecord(id={self._record_id}, created={self._created_at.strftime('%Y-%m-%d %H:%M:%S')})"


class CallRecord(BaseRecord):
    """
    Класс для представления записи о звонке.
    Наследуется от BaseRecord.
    """

    # Статический счетчик для демонстрации статического метода
    _total_calls = 0
    _resolved_calls = 0

    def __init__(self, call_id: int, phone: str, reason: str, is_resolved: bool):
        """
        Инициализация записи о звонке с использованием __setattr__.

        Args:
            call_id: Номер звонка
            phone: Телефон звонящего
            reason: Причина обращения
            is_resolved: Решена проблема или нет
        """
        # Вызываем конструктор родителя
        super().__init__(call_id)

        # Используем __setattr__ для установки свойств
        self.__setattr__('_phone', phone)
        self.__setattr__('_reason', reason)
        self.__setattr__('_is_resolved', is_resolved)
        self.__setattr__('_call_id', call_id)

        # Обновляем статические счетчики
        CallRecord._total_calls += 1
        if is_resolved:
            CallRecord._resolved_calls += 1

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Перегрузка __setattr__ для контроля установки свойств.
        Все свойства защищены (начинаются с _).

        Args:
            name: Имя атрибута
            value: Значение атрибута
        """
        if name.startswith('_'):
            # Разрешаем установку защищенных атрибутов
            super().__setattr__(name, value)
        elif name in ['phone', 'reason', 'is_resolved', 'call_id']:
            # Преобразуем публичные имена в защищенные
            super().__setattr__(f'_{name}', value)
        else:
            # Запрещаем создание новых публичных атрибутов
            raise AttributeError(f"Нельзя создать новый атрибут '{name}'. Используйте существующие свойства.")

    @property
    def call_id(self) -> int:
        """Геттер для номера звонка."""
        return self._call_id

    @property
    def phone(self) -> str:
        """Геттер для телефона."""
        return self._phone

    @property
    def reason(self) -> str:
        """Геттер для причины обращения."""
        return self._reason

    @property
    def is_resolved(self) -> bool:
        """Геттер для статуса решения."""
        return self._is_resolved

    @staticmethod
    def get_total_calls() -> int:
        """
        Статический метод: возвращает общее количество звонков.

        Returns:
            int: Общее количество звонков
        """
        return CallRecord._total_calls

    @staticmethod
    def get_resolved_percentage() -> float:
        """
        Статический метод: возвращает процент решенных проблем.

        Returns:
            float: Процент решенных проблем
        """
        if CallRecord._total_calls == 0:
            return 0.0
        return (CallRecord._resolved_calls / CallRecord._total_calls) * 100

    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> 'CallRecord':
        """
        Статический метод: создает объект CallRecord из словаря.

        Args:
            data: Словарь с данными

        Returns:
            CallRecord: Новый объект звонка
        """
        return CallRecord(
            call_id=int(data['№']),
            phone=data['телефон'],
            reason=data['причина обращения'],
            is_resolved=data['решена проблема'].strip().lower() in ['да', 'true', 'yes', '1']
        )

    def __repr__(self) -> str:
        """
        Перегрузка repr для красивого представления объекта.

        Returns:
            str: Строковое представление звонка
        """
        status = "Решена" if self._is_resolved else "Не решена"
        return (f"CallRecord(id={self._call_id}, phone='{self._phone}', "
                f"reason='{self._reason[:20]}...', resolved={status})")

    def __str__(self) -> str:
        """
        Перегрузка str для удобного вывода.

        Returns:
            str: Отформатированная строка с данными звонка
        """
        status = "✓ Решена" if self._is_resolved else "✗ Не решена"
        return f"№{self._call_id:3d} | {self._phone:15s} | {self._reason:30s} | {status}"

    def __eq__(self, other: object) -> bool:
        """
        Перегрузка оператора == для сравнения звонков.

        Args:
            other: Другой объект для сравнения

        Returns:
            bool: True если звонки равны
        """
        if not isinstance(other, CallRecord):
            return False
        return self._call_id == other._call_id

    def __lt__(self, other: object) -> bool:
        """
        Перегрузка оператора < для сравнения по номеру звонка.

        Args:
            other: Другой объект для сравнения

        Returns:
            bool: True если текущий звонок меньше
        """
        if not isinstance(other, CallRecord):
            return NotImplemented
        return self._call_id < other._call_id


class CallCollection:
    """
    Класс для коллекции звонков.
    Реализует итератор и доступ по индексу.
    """

    def __init__(self, calls: Optional[List[CallRecord]] = None):
        """
        Инициализация коллекции звонков.

        Args:
            calls: Начальный список звонков
        """
        self._calls = calls if calls is not None else []
        self._index = 0  # Для итератора

    def __len__(self) -> int:
        """Возвращает количество звонков в коллекции."""
        return len(self._calls)

    def __getitem__(self, index: int) -> CallRecord:
        """
        Доступ к элементам коллекции по индексу.
        Поддерживает отрицательные индексы (например, -1 для последнего элемента).

        Args:
            index: Индекс элемента (может быть отрицательным)

        Returns:
            CallRecord: Звонок по указанному индексу

        Raises:
            IndexError: Если индекс вне диапазона
        """
        # Сохраняем оригинальный индекс для сообщения об ошибке
        original_index = index

        # Преобразуем отрицательный индекс в положительный
        if index < 0:
            index = len(self._calls) + index

        if 0 <= index < len(self._calls):
            return self._calls[index]

        # Если индекс все еще вне диапазона
        if original_index < 0:
            raise IndexError(f"Индекс {original_index} вне диапазона (от -{len(self._calls)} до -1)")
        else:
            raise IndexError(f"Индекс {original_index} вне диапазона (0-{len(self._calls) - 1})")

    def __setitem__(self, index: int, value: CallRecord) -> None:
        """
        Установка значения по индексу.
        Поддерживает отрицательные индексы.

        Args:
            index: Индекс элемента
            value: Новое значение
        """
        # Преобразуем отрицательный индекс в положительный
        if index < 0:
            index = len(self._calls) + index

        if 0 <= index < len(self._calls):
            self._calls[index] = value
        else:
            raise IndexError(f"Индекс {index} вне диапазона")

    def __iter__(self) -> Iterator[CallRecord]:
        """
        Возвращает итератор для коллекции.

        Returns:
            Iterator[CallRecord]: Итератор по звонкам
        """
        self._index = 0
        return self

    def __next__(self) -> CallRecord:
        """
        Следующий элемент для итератора.

        Returns:
            CallRecord: Следующий звонок

        Raises:
            StopIteration: Когда элементы закончились
        """
        if self._index < len(self._calls):
            result = self._calls[self._index]
            self._index += 1
            return result
        raise StopIteration

    def __repr__(self) -> str:
        """Перегрузка repr для коллекции."""
        return f"CallCollection({len(self._calls)} calls)"

    def __add__(self, other: 'CallCollection') -> 'CallCollection':
        """
        Перегрузка оператора + для объединения коллекций.

        Args:
            other: Другая коллекция

        Returns:
            CallCollection: Новая коллекция с объединенными звонками
        """
        new_calls = self._calls.copy()
        new_calls.extend(other._calls)
        return CallCollection(new_calls)

    def add_call(self, call: CallRecord) -> None:
        """Добавляет звонок в коллекцию."""
        self._calls.append(call)

    def get_calls(self) -> List[CallRecord]:
        """Возвращает список звонков."""
        return self._calls.copy()

    # Генераторы
    def generate_resolved_calls(self) -> Iterator[CallRecord]:
        """
        Генератор: возвращает только решенные звонки.

        Yields:
            CallRecord: Следующий решенный звонок
        """
        for call in self._calls:
            if call.is_resolved:
                yield call

    def generate_by_reason(self, reason_filter: str) -> Iterator[CallRecord]:
        """
        Генератор: возвращает звонки по заданной причине.

        Args:
            reason_filter: Фильтр по причине

        Yields:
            CallRecord: Следующий звонок с указанной причиной
        """
        for call in self._calls:
            if reason_filter.lower() in call.reason.lower():
                yield call

    def generate_batch(self, batch_size: int = 3) -> Iterator[List[CallRecord]]:
        """
        Генератор: возвращает звонки пакетами (для обработки больших данных).

        Args:
            batch_size: Размер пакета

        Yields:
            List[CallRecord]: Пакет звонков
        """
        for i in range(0, len(self._calls), batch_size):
            yield self._calls[i:i + batch_size]

    def generate_statistics(self) -> Iterator[tuple]:
        """
        Генератор: возвращает статистику по каждому звонку.

        Yields:
            tuple: (номер_звонка, телефон, статус, порядковый_номер)
        """
        for idx, call in enumerate(self._calls, 1):
            status = "решена" if call.is_resolved else "не решена"
            yield (call.call_id, call.phone, status, idx)

    @staticmethod
    def create_from_csv(filename: str) -> 'CallCollection':
        """
        Статический метод: создает коллекцию из CSV файла.

        Args:
            filename: Имя CSV файла

        Returns:
            CallCollection: Коллекция звонков
        """
        collection = CallCollection()

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    call = CallRecord.create_from_dict(row)
                    collection.add_call(call)

            print(f"Загружено {len(collection)} записей из файла '{filename}'")

        except FileNotFoundError:
            print(f"Файл '{filename}' не найден. Создаю пример...")
            create_example_csv(filename)
            return CallCollection.create_from_csv(filename)
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")

        return collection

    def save_to_csv(self, filename: str = "data.csv") -> bool:
        """
        Сохраняет коллекцию в CSV файл.

        Args:
            filename: Имя файла для сохранения

        Returns:
            bool: True если сохранение успешно
        """
        try:
            # Создаем резервную копию
            if os.path.exists(filename):
                backup_name = filename.replace('.csv', '_backup.csv')
                with open(filename, 'r', encoding='utf-8') as src:
                    with open(backup_name, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                print(f"Создана резервная копия: {backup_name}")

            with open(filename, 'w', encoding='utf-8', newline='') as file:
                fieldnames = ['№', 'телефон', 'причина обращения', 'решена проблема']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                for call in self._calls:
                    writer.writerow({
                        '№': call.call_id,
                        'телефон': call.phone,
                        'причина обращения': call.reason,
                        'решена проблема': 'Да' if call.is_resolved else 'Нет'
                    })

            print(f"Данные сохранены в '{filename}'")
            return True

        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False

    def sort_by_phone(self) -> None:
        """Сортирует коллекцию по телефону."""
        self._calls.sort(key=lambda x: x.phone)

    def sort_by_id(self) -> None:
        """Сортирует коллекцию по номеру звонка."""
        self._calls.sort(key=lambda x: x.call_id)

    def filter_by_resolved(self, resolved: bool) -> 'CallCollection':
        """
        Фильтрует коллекцию по статусу решения.

        Args:
            resolved: Статус решения (True/False)

        Returns:
            CallCollection: Отфильтрованная коллекция
        """
        filtered = [call for call in self._calls if call.is_resolved == resolved]
        return CallCollection(filtered)

    def display(self, title: str = "Список звонков") -> None:
        """Отображает коллекцию на экране."""
        print(f"\n{'=' * 80}")
        print(f"{title}")
        print(f"{'=' * 80}")

        if not self._calls:
            print("Нет данных для отображения")
            return

        print(f"{'№':3s} | {'Телефон':15s} | {'Причина обращения':30s} | {'Статус':10s}")
        print(f"{'-' * 80}")

        for call in self._calls:
            print(call)

        print(f"{'=' * 80}")

        # Выводим статическую статистику
        print(f"\nСтатистика (из статических методов):")
        print(f"  Всего звонков: {CallRecord.get_total_calls()}")
        print(f"  Решено проблем: {CallRecord._resolved_calls}")
        print(f"  Процент решения: {CallRecord.get_resolved_percentage():.1f}%")


def count_files_in_directory(directory_path: str = ".") -> int:
    """
    Подсчитывает количество файлов в указанной директории.

    Args:
        directory_path: Путь к директории

    Returns:
        int: Количество файлов
    """
    try:
        if not os.path.exists(directory_path):
            print(f"Директория '{directory_path}' не существует!")
            return 0

        file_count = sum(1 for item in os.listdir(directory_path)
                         if os.path.isfile(os.path.join(directory_path, item)))

        return file_count

    except Exception as e:
        print(f"Ошибка при подсчете файлов: {e}")
        return 0


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


def main():
    """
    Главная функция программы с демонстрацией всех возможностей классов.
    """
    print("=" * 80)
    print("ПРОГРАММА АНАЛИЗА ДАННЫХ CALL-ЦЕНТРА (С ИСПОЛЬЗОВАНИЕМ КЛАССОВ)")
    print("=" * 80)

    # Задание 1: Подсчет файлов в директории
    print("\n--- ЗАДАНИЕ 1: Подсчет файлов в директории ---")
    current_dir = input("Введите путь к директории (Enter для текущей папки): ").strip()
    if not current_dir:
        current_dir = "."

    file_count = count_files_in_directory(current_dir)
    print(f"В директории '{current_dir}' найдено файлов: {file_count}")

    # Задание 2: Работа с классами
    print("\n--- ЗАДАНИЕ 2: Работа с классами ---")

    # Создаем коллекцию из CSV файла (используем статический метод)
    collection = CallCollection.create_from_csv("data.csv")

    # Демонстрация __repr__
    print("\n--- Демонстрация __repr__ ---")
    print(repr(collection))
    if len(collection) > 0:
        print(repr(collection[0]))

    # Демонстрация доступа по индексу (__getitem__)
    print("\n--- Демонстрация доступа по индексу ---")
    print(f"Первый звонок: {collection[0]}")
    print(f"Последний звонок: {collection[-1]}")

    # Демонстрация итератора
    print("\n--- Демонстрация итератора ---")
    print("Перебор всех звонков через for:")
    for i, call in enumerate(collection):
        if i >= 3:  # Показываем только первые 3
            print(f"  ... и еще {len(collection) - 3} звонков")
            break
        print(f"  {call}")

    # 2.1 Сортировка по строковому полю (телефон)
    print("\n--- 2.1 Сортировка по строковому полю (телефон) ---")
    collection.sort_by_phone()
    collection.display("Сортировка по номеру телефона")

    # 2.2 Сортировка по числовому полю (номер звонка)
    print("\n--- 2.2 Сортировка по числовому полю (номер звонка) ---")
    collection.sort_by_id()
    collection.display("Сортировка по номеру звонка")

    # 2.3 Фильтрация по критерию
    print("\n--- 2.3 Фильтрация по критерию (решенные проблемы) ---")
    resolved_collection = collection.filter_by_resolved(True)
    resolved_collection.display("Звонки с РЕШЕННЫМИ проблемами")

    # Демонстрация генераторов
    print("\n--- Демонстрация генераторов ---")

    print("\nГенератор решенных звонков (generate_resolved_calls):")
    for call in collection.generate_resolved_calls():
        print(f"  {call}")
        break  # Показываем только первый
    print("  ...")

    print("\nГенератор по причине 'интернет' (generate_by_reason):")
    for call in collection.generate_by_reason("интернет"):
        print(f"  {call}")

    print("\nГенератор пакетов по 3 звонка (generate_batch):")
    for batch_num, batch in enumerate(collection.generate_batch(3), 1):
        print(f"  Пакет {batch_num}: {len(batch)} звонков")

    print("\nГенератор статистики (generate_statistics):")
    for call_id, phone, status, idx in collection.generate_statistics():
        print(f"  {idx}. Звонок №{call_id} ({phone}) - {status}")
        if idx >= 3:
            print("  ...")
            break

    # Демонстрация статических методов
    print("\n--- Демонстрация статических методов ---")
    print(f"Всего звонков (статический метод): {CallRecord.get_total_calls()}")
    print(f"Процент решения (статический метод): {CallRecord.get_resolved_percentage():.1f}%")

    # Демонстрация __setattr__ (попытка установить недопустимый атрибут)
    print("\n--- Демонстрация __setattr__ ---")
    try:
        test_call = collection[0]
        # Попытка создать новый атрибут (должна вызвать ошибку)
        test_call.new_attribute = "test"
    except AttributeError as e:
        print(f"  Ошибка (как и ожидалось): {e}")

    # Демонстрация перегрузки операторов
    print("\n--- Демонстрация перегрузки операторов ---")
    if len(collection) >= 2:
        call1 = collection[0]
        call2 = collection[1]
        print(f"  {call1}")
        print(f"  {call2}")
        print(f"  call1 == call2? {call1 == call2}")
        print(f"  call1 < call2? {call1 < call2}")

    # Задание 3: Добавление новых данных
    print("\n--- ЗАДАНИЕ 3: Добавление новых данных ---")

    # Создаем новый звонок через статический метод
    new_call_data = {
        '№': len(collection) + 1,
        'телефон': '+7-999-123-45-67',
        'причина обращения': 'Новый заказ услуги',
        'решена проблема': 'Да'
    }
    new_call = CallRecord.create_from_dict(new_call_data)
    collection.add_call(new_call)
    print(f"Добавлен новый звонок: {new_call}")

    # Сохраняем изменения
    save_choice = input("\nСохранить изменения в файл? (да/нет): ").strip().lower()
    if save_choice in ['да', 'yes', 'д', 'y']:
        collection.save_to_csv("data.csv")
        print("✓ Изменения сохранены!")

    # Итоговая статистика
    print("\n" + "=" * 80)
    print("ИТОГОВАЯ СТАТИСТИКА")
    print("=" * 80)
    collection.display("ФИНАЛЬНЫЙ СПИСОК ЗВОНКОВ")

    print("\n" + "=" * 80)
    print("ПРОГРАММА ЗАВЕРШЕНА")
    print("=" * 80)


if __name__ == "__main__":
    main()