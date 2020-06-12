import csv
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

with open('mag.csv') as csvfile:
     reader = csv.reader(csvfile)
     data = [r for r in reader]

x_data = [float(row[0]) for row in data]
y_data = [float(row[1]) for row in data]
z_data = [float(row[2]) for row in data]

x_avg = sum(x_data) / len(x_data)
y_avg = sum(y_data) / len(y_data)
z_avg = sum(z_data) / len(z_data)

x_data = [d - x_avg for d in x_data]
y_data = [d - y_avg for d in y_data]
z_data = [d - z_avg for d in z_data]
print(x_avg)
print(y_avg)
print(z_avg)
filtered_x = []
filtered_y = []
filtered_z = []

for i in range(len(x_data)):
    if -1000 < x_data[i] < 1000:
        if -1000 < y_data[i] < 1000:
            if -1000 < z_data[i] < 1000:
                filtered_x.append(x_data[i])
                filtered_y.append(y_data[i])
                filtered_z.append(z_data[i])
plt.scatter(filtered_x, filtered_y);
plt.scatter(filtered_x, filtered_z);
plt.scatter(filtered_y, filtered_z);
plt.show()
