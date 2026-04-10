import random

def get_list():
    print("\n1. Ручной ввод")
    print("2. Автоматическая генерация")
    choice = input("Выберите способ (1 или 2): ").strip()

    if choice == '1':
        while True:
            try:
                text = input("Введите числа через пробел: ").strip()
                if not text:
                    print("Список не может быть пустым!")
                    continue

                numbers = []
                for x in text.split():
                    numbers.append(int(x))

                print(f"Ваш список: {numbers}")
                return numbers

            except ValueError:
                print("Ошибка! Введите только целые числа через пробел.")

    elif choice == '2':
        while True:
            try:
                size = int(input("Введите размер списка: "))
                if size <= 0:
                    print("Размер должен быть больше 0!")
                    continue

                min_val = int(input("Минимальное значение: "))
                max_val = int(input("Максимальное значение: "))

                if min_val > max_val:
                    print("Минимум не может быть больше максимума!")
                    continue

                numbers = [random.randint(min_val, max_val) for _ in range(size)]
                print(f"Сгенерированный список: {numbers}")
                return numbers

            except ValueError:
                print("Ошибка! Введите целые числа.")

    else:
        print("Неверный выбор! Использую ручной ввод.")
        return get_list()


def bubble_sort(arr):
    sorted_arr = arr.copy()
    n = len(sorted_arr)

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            if sorted_arr[j] > sorted_arr[j + 1]:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped = True

        if not swapped:
            break

    return sorted_arr


def bubble_sort_with_sort(arr):
    return sorted(arr.copy())

def main():
    print("ПУЗЫРЬКОВАЯ СОРТИРОВКА")

    original_list = get_list()

    print("\n1. Сортировка (без стандартных функций)")
    print("2. Сортировка (с использованием)")

    choice = input("Выберите метод (1 или 2): ").strip()

    if choice == '1':
        sorted_list = bubble_sort(original_list)
        print("\n--- Сортировка без стандартных функций ---")
    else:
        sorted_list = bubble_sort_with_sort(original_list)
        print("\n--- Сортировка с использованием ---")

    print(f"Исходный список:    {original_list}")
    print(f"Отсортированный:    {sorted_list}")

if __name__ == "__main__":
    main()