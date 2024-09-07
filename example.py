import tmark as tm
import time

tracker = tm.LatencyTracker()

# Simulation of a cycle with multiple tags in one iteration
for i in range(12):
    tracker.start("operation_1")
    time.sleep(0.1 + i * 0.02)  # Simulation of first operation
    tracker.stop("operation_1")

    tracker.start("operation_2")
    time.sleep(0.2 + i * 0.03)  # Simulation of the second operation
    tracker.stop("operation_2")

    tracker.start("operation_3")
    time.sleep(0.15 + i * 0.01)  # Simulation of the third operation
    tracker.stop("operation_3")

# Graph from object data
tracker.plot(statistic=True)

# Save to csv file
tracker.save_to_csv()

# Reading from csv file and plotting
tracker.plot_from_csv()
