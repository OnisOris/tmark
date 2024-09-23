import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Table:
    def __init__(self, label):
        self.label = label
        self.starts_times = np.array([])
        self.end_times = np.array([])
        self.latencies = np.array([])
        self.timestamps = np.array([])

    def matrix(self):
        return np.vstack([self.starts_times, self.end_times, self.latencies, self.timestamps])


class LatencyTracker:
    def __init__(self, accuracy: int = 5):
        self.labels = np.array([])
        self.data = np.array([])
        self.accuracy = accuracy
        self.t0 = np.round(time.time(), self.accuracy)



    def start(self, label: str) -> None:
        """
        Records the start time of the code section with the specified tag.
        """
        index = np.where(label == self.labels)[0]
        if not index.shape == (0,):
            self.data[index[0]].starts_times = np.hstack([self.data[index[0]].starts_times,
                                                          np.round(time.time(), self.accuracy) - self.t0])
        else:
            self.labels = np.hstack([self.labels, label])
            self.data = np.hstack([self.data, Table(label)])
            self.data[-1].starts_times = np.hstack([self.data[-1].starts_times,
                                                    np.round(time.time(), self.accuracy) - self.t0])

    def stop(self, label: str) -> None:
        """
        Records the time of completion of the code section with the specified tag and calculates the delay
        """
        end_time = np.round(time.time(), self.accuracy) - self.t0
        index = np.where(label == self.labels)[0]
        if not index.shape == (0,):
            item = index[0]
        else:
            item = -1
        self.data[item].end_times = np.hstack([self.data[item].end_times, end_time])
        # Calculate the delay and save it
        latency = end_time - self.data[item].starts_times[-1]
        self.data[item].latencies = np.hstack([self.data[item].latencies, latency])

        # Save current time for X axis
        self.data[item].timestamps = np.hstack([self.data[item].timestamps, end_time])

    def plot(self, statistic: bool = False, accuracy: int = 4) -> None:
        """
        Builds delay schedules for each tag
        """
        plt.figure()
        str_stat = ''
        for index_table, table in enumerate(self.data):
            if statistic:
                r = accuracy
                mean = np.round(table.latencies.mean(), r)
                median = np.round(np.median(table.latencies), r)
                maximum = np.round(table.latencies.max(), r)
                minimum = np.round(table.latencies.min(), r)
                str_stat += f'\n{table.label}: mean = {mean}, median = {median}, max = {maximum}, min = {minimum}'
            m = table.matrix()
            plt.plot(m[3], m[2], marker='o', label=f"{table.label}")
        plt.xlabel('Time [s]')
        plt.ylabel('Latency [с]')
        plt.title('Latencies')
        plt.legend()
        plt.grid(True)
        plt.show()
        print('Stat:' + str_stat)

    def plot_from_csv(self, path: str = './csv/', statistic: bool = False, accuracy: int = 4):
        """
        Plot all files inside the csv folder, combining them
        """
        import os
        files = os.listdir(path)
        print(f"File read: {files}")
        plt.figure()
        str_stat = 'Stat:'
        for file in files:
            lf = len(file)
            if file[lf-4:lf] != ".csv":
                continue
            df = pd.read_csv(f'{path}{file}', index_col=0)
            plt.plot(df['t'], df['latencies'], label=f'{file}', marker='o')
            if statistic:
                r = accuracy
                mean = np.round(df['latencies'].mean(), r)
                median = np.round(df['latencies'].median(), r)
                maximum = np.round(df['latencies'].max(), r)
                minimum = np.round(df['latencies'].min(), r)
                str_stat += f'\n{file}: mean = {mean}, median = {median}, max = {maximum}, min = {minimum}'
        plt.xlabel('Time [s]')
        plt.ylabel('Latency [s]')
        plt.title('Latencies')
        plt.legend()
        plt.grid(True)
        plt.show()
        print(str_stat)

    def save_to_numpy(self, path: str = './numpy/') -> None:
        """
        Save the whole array to npy
        """
        from os.path import isdir
        if not isdir(path):
            from os import makedirs
            makedirs(path, exist_ok=True)
        array = self.vstack_data()
        np.save(f'{path}data.npy', array[1:])

    def vstack_data(self) -> np.ndarray:
        """
        Function compiles all information into matrix
        """
        array = np.zeros(self.data[0].starts_times.shape)
        for table in self.data:
            array = np.vstack([array, table.matrix()])
        return array[1:]

    def save_to_csv(self, path: str = './csv/') -> None:
        """
        Save as csv file
        """
        from os.path import isdir
        if not isdir(path):
            from os import makedirs
            makedirs(path, exist_ok=True)
        for table in self.data:
            df = pd.DataFrame(table.matrix().T, columns=[f'starts_times',
                                                         f'end_times',
                                                         f'latencies',
                                                         f't'])
            df.to_csv(f'{path}data_{table.label}.csv')

    def get_labels(self) -> np.ndarray:
        """
        Returns labels
        """
        labels = np.array([])
        for table in self.data:
            labels = np.hstack([labels, table.label])
        return labels
