import matplotlib.pyplot as plt
import json

with open('config.json') as config_file:
    config = json.load(config_file)


def generate_graph(timestamps: list, humidities: list, temperatures: list):

    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(8, 4))

    # Plot humidity
    ax1.set_xlabel('Timestamps')
    ax1.set_ylabel('Humidity (%)', color='blue')
    ax1.plot(timestamps, humidities, color='blue', marker='o', label='Humidity')
    ax1.tick_params(axis='y', labelcolor='blue')
    # ax1.set_ylim(0, 60)  # Set y-axis limits for humidity

    # Create a second y-axis for temperature
    ax2 = ax1.twinx()
    ax2.set_ylabel('Temperature (°C)', color='red')
    ax2.plot(timestamps, temperatures, color='red', marker='s', label='Temperature')
    ax2.tick_params(axis='y', labelcolor='red')
    # ax2.set_ylim(0, 60)  # Set y-axis limits for temperature

    # Title and grid
    plt.title('Humidity and Temperature over Time')
    fig.tight_layout()
    plt.grid()

    # Save the plot as a PNG file
    plt.savefig(config["graph"])


if __name__ == '__main__':
    _timestamps = ['16:1', '16:2', '16:3', '16:4', '16:5', '16:6', '16:7', '16:8', '16:9', '16:10', '16:11', '16:12']
    _humidities = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
    _temperatures = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

    generate_graph(_timestamps, _humidities, _temperatures)