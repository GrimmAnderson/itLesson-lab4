import numpy as np
from datetime import datetime


def generate_matrix_numpy(n: int, min_val: int = 0, max_val: int = 100) -> np.ndarray:
    matrix = np.random.randint(min_val, max_val + 1, size=(n, n))
    return matrix


def sum_above_main_diagonal(matrix: np.ndarray) -> float:
    n = matrix.shape[0]
    total_sum = 0

    for i in range(n):
        for j in range(i + 1, n):  # j > i
            total_sum += matrix[i, j]

    return total_sum


def product_above_secondary_diagonal(matrix: np.ndarray) -> float:
    n = matrix.shape[0]
    product = 1.0

    for i in range(n):
        for j in range(n - 1 - i):  # j < n-1-i
            product *= matrix[i, j]

    return product


def save_results_to_file(filename: str, matrix: np.ndarray,
                        sum_above_main: float, product_above_secondary: float) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("РЕЗУЛЬТАТЫ ОБРАБОТКИ КВАДРАТНОЙ МАТРИЦЫ\n")
            f.write("ИСХОДНАЯ МАТРИЦА:\n")
            for i in range(matrix.shape[0]):
                row_str = " ".join(f"{matrix[i, j]:8d}" for j in range(matrix.shape[1]))
                f.write(row_str + "\n")

            f.write("РЕЗУЛЬТАТЫ ВЫЧИСЛЕНИЙ:\n")
            f.write(f"Сумма элементов ВЫШЕ ГЛАВНОЙ диагонали: {sum_above_main:.2f}\n")
            f.write(f"Произведение элементов ВЫШЕ ПОБОЧНОЙ диагонали: {product_above_secondary:.2e}\n")


        print(f"\nРезультаты успешно сохранены в файл: {filename}")

    except Exception as e:
        print(f"\nОшибка при сохранении файла: {e}")


def display_matrix(matrix: np.ndarray) -> None:
    n = matrix.shape[0]
    print(f"СГЕНЕРИРОВАННАЯ МАТРИЦА {n} x {n}:")

    for i in range(n):
        row_str = " ".join(f"{matrix[i, j]:6d}" for j in range(n))
        print(f"{row_str}")



def get_matrix_size() -> int:
    while True:
        try:
            n = int(input("Введите размер квадратной матрицы N (N > 0): "))
            if n <= 0:
                print("Размер матрицы должен быть положительным числом!")
                continue
            return n
        except ValueError:
            print("Ошибка: Введите целое положительное число!")


def get_value_range() -> tuple:
    print("\nНастройка диапазона значений:")

    while True:
        try:
            min_val = int(input("Введите минимальное значение: ") or "0")
            max_val = int(input("Введите максимальное значение: ") or "100")

            if min_val > max_val:
                print("Минимальное значение не может быть больше максимального!")
                continue

            return min_val, max_val

        except ValueError:
            print("Ошибка: Введите целые числа!")

def main():
    print("ПРОГРАММА ОБРАБОТКИ КВАДРАТНОЙ МАТРИЦЫ")

    try:
        n = get_matrix_size()

        min_val, max_val = get_value_range()

        print(f"\nГенерация матрицы {n}x{n} со случайными числами "
              f"от {min_val} до {max_val}...")
        matrix = generate_matrix_numpy(n, min_val, max_val)

        display_matrix(matrix)

        print("\nВычисление суммы элементов выше главной диагонали...")
        sum_above_main = sum_above_main_diagonal(matrix)

        print("Вычисление произведения элементов выше побочной диагонали...")
        product_above_secondary = product_above_secondary_diagonal(matrix)

        print("РЕЗУЛЬТАТЫ ВЫЧИСЛЕНИЙ:")
        print(f"Сумма элементов ВЫШЕ ГЛАВНОЙ диагонали: {sum_above_main:.2f}")
        print(f"Произведение элементов ВЫШЕ ПОБОЧНОЙ диагонали: {product_above_secondary:.2e}")

        filename = f"matrix_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        save_results_to_file(filename, matrix, sum_above_main, product_above_secondary)

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()