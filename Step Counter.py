import math

import matplotlib.pyplot as plt


def get_accel_net_data(name):
    path = "C:\\Users\\darre\\step-sensor-data\\"
    with open(path + name) as reader:
        lines = reader.readlines()
    acc_x = [float(line.split(",")[0]) for line in lines[1:]]
    acc_y = [float(line.split(",")[1]) for line in lines[1:]]
    acc_z = [float(line.split(",")[2]) for line in lines[1:]]
    return [math.sqrt(acc_x[i] ** 2 + acc_y[i] ** 2 + acc_z[i] ** 2) for i in range(len(acc_x))]


def get_mean(data):
    sum = 0
    for val in data:
        sum += val
    return sum / (len(data))


def get_standard_deviation(data, mean):
    squared_sum = 0
    for val in data:
        squared_sum += (val - mean) * (val - mean)
    return math.sqrt(squared_sum / (len(data) - 1))


def get_maxs(data):
    peaks_x = []
    for i in range(1, len(data) - 1):
        if (data[i] > data[i - 1] and data[i] > data[i + 1]):
            peaks_x.append(i)
    peaks_y = [data[index] for index in peaks_x]
    return peaks_x, peaks_y


def get_mins(data):
    mins_x = []
    for i in range(1, len(data) - 1):
        if (data[i] < data[i - 1] and data[i] < data[i + 1]):
            mins_x.append(i)
    mins_y = [data[index] for index in mins_x]
    return mins_x, mins_y


def get_step_peaks(data):
    range_for_calculating_SD = 10
    maxs_x, maxs_y = get_maxs(data)
    mins_x, mins_y = get_mins(data)
    maxs_mean = get_mean(maxs_y)
    mins_mean = get_mean(mins_y)
    z_score_differences = 1.2
    z_score_all_data = 1.2
    steps_x = []
    steps_y = []
    averageDifference = maxs_mean - mins_mean
    mean = get_mean(data)
    standard_deviation = get_standard_deviation(data, mean)
    mins_x, mins_y = get_mins(data)
    i = range_for_calculating_SD * 2
    while (i < len(maxs_x) - range_for_calculating_SD and i < len(mins_x) - range_for_calculating_SD):
        maxs_standard_deviation = get_standard_deviation(
            maxs_y[i - range_for_calculating_SD:i + range_for_calculating_SD], maxs_mean)
        mins_standard_deviation = get_standard_deviation(
            mins_y[i - range_for_calculating_SD:i + range_for_calculating_SD], mins_mean)
        differences_standard_deviation = math.sqrt(maxs_standard_deviation ** 2 + mins_standard_deviation ** 2)
        maxToBeCompared = maxs_y[i]
        indexOfMaxToBeCompared = i
        minToBeCompared = mins_y[i]
        while (
                maxToBeCompared - minToBeCompared < averageDifference + z_score_differences * differences_standard_deviation and
                i < len(maxs_x) and i < len(mins_x)):
            if (maxs_y[i] > maxToBeCompared):
                maxToBeCompared = maxs_y[i]
                indexOfMaxToBeCompared = i
                minToBeCompared = mins_y[i]
            i += 1
        if (maxToBeCompared > mean + z_score_all_data * standard_deviation):
            steps_x.append(maxs_x[indexOfMaxToBeCompared])
            steps_y.append(maxToBeCompared)
        i += 1
    return steps_x, steps_y


def plot(name, plotRows, plotCols, n):
    acc_net = get_accel_net_data(name)
    steps_x, steps_y = get_step_peaks(acc_net)
    title = name[:name.find(".")]
    num_steps = int(title.split("-")[1])
    plt.subplot(plotRows, plotCols, n)
    plt.title(title)
    plt.plot(acc_net, "b-")
    plt.plot(steps_x, steps_y, "ro")
    plt.text(2, 2, str(len(steps_x) * 2) + " counted steps\nPercent error: " + str(
        ((len(steps_x) * 2 - num_steps) / num_steps) * 100) + "%", color='white', fontsize=12,
             bbox=dict(facecolor='black', alpha=0.5))


filenames = ["1-200-step-regular.csv", "2-200-step-variable.csv", "3-200-step-jacket.csv", "4-100-step-running.csv",
             "5-200-step-rear-pocket.csv", "6-200-step-toddler-pace.csv", "7-200-step-jacket-variable.csv",
             "8-200-step-toddler.csv", "9-200-step-toddler.csv", "10-500-step-regular.csv", "11-400-step-regular.csv"]
f = ["1-200-step-regular.csv", "4-100-step-running.csv", "10-500-step-regular.csv", "11-400-step-regular.csv"]

for i in range(0, len(filenames)):
    plot(filenames[i], 4, 3, i + 1)

plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.6)
plt.show()
