import matplotlib.pyplot as plt
import json

with open('config.json') as config_file:
    config = json.load(config_file)


def generate_graph(timestamps: list, humidities: list, temperatures: list):
    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(8, 8))

    # Plot humidity
    ax1.set_xlabel('Timestamps')
    ax1.set_ylabel('Humidity (%)', color='blue')
    ax1.plot(timestamps, humidities, color='blue', label='Humidity')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_ylim(0, 100)  # Set y-axis limits for humidity

    n_x_on_graph = 5
    print(f"n_x_on_graph: {n_x_on_graph}")
    take_each = round(len(timestamps) / n_x_on_graph)
    print(f"take_each: {take_each}")
    x_invis = []
    for i in range(len(timestamps)):
        if i % take_each != 0:
            x_invis.append(i)
    print(timestamps)
    print(x_invis)
    # Hide every second label
    if x_invis != []:
        for i in reversed(x_invis):
            plt.gca().get_xticklabels()[i].set_visible(False)


    # Create a second y-axis for temperature
    ax2 = ax1.twinx()
    ax2.set_ylabel('Temperature (°C)', color='red')
    ax2.plot(timestamps, temperatures, color='red', label='Temperature')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, 100)  # Set y-axis limits for temperature

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