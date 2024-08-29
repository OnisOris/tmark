import time
import matplotlib.pyplot as plt
from collections import defaultdict


class LatencyTracker:
    def __init__(self):
        self.data = defaultdict(lambda: {"start_times": [], "end_times": [], "latencies": [], "timestamps": []})

    def start(self, label: str) -> None:
        """
        Фиксирует время начала выполнения участка кода с указанной меткой.
        """
        self.data[label]["start_times"].append(time.time())

    def stop(self, label: str) -> None:
        """
        Фиксирует время окончания выполнения участка кода с указанной меткой и вычисляет задержку.
        """
        end_time = time.time()
        self.data[label]["end_times"].append(end_time)

        # Вычисляем задержку и сохраняем её
        latency = end_time - self.data[label]["start_times"][-1]
        self.data[label]["latencies"].append(latency)

        # Сохраняем текущее время для оси X
        self.data[label]["timestamps"].append(end_time)

    def plot(self) -> None:
        """
        Строит графики задержек для каждой метки.
        """
        plt.figure()

        for label, metrics in self.data.items():
            plt.plot(metrics["timestamps"], metrics["latencies"], marker='o', label=label)

        plt.xlabel('Время')
        plt.ylabel('Задержка (секунды)')
        plt.title('График задержек по времени для разных меток')
        plt.legend()
        plt.grid(True)
        plt.show()
