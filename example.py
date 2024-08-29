import tmark as tm
import time
# Пример использования
tracker = tm.LatencyTracker()

# Имитация выполнения цикла с несколькими метками в одной итерации
for i in range(12):
    tracker.start("operation_1")
    time.sleep(0.1 + i * 0.02)  # Симуляция первой операции
    tracker.stop("operation_1")

    tracker.start("operation_2")
    time.sleep(0.2 + i * 0.03)  # Симуляция второй операции
    tracker.stop("operation_2")

    tracker.start("operation_3")
    time.sleep(0.15 + i * 0.01)  # Симуляция третьей операции
    tracker.stop("operation_3")

# Построение графика
tracker.plot()
