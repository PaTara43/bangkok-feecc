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
    _timestamps = ['16:10', '16:30', '16:50', '17:10', '17:30', '17:50', '18:10', '18:30', '18:50', '19:10', '19:30', '19:50']
    _humidities = [70.1, 70.1, 70.5, 71, 71, 71.1, 71.4, 71.2, 71.6, 71.7, 72, 72]
    _temperatures = [30.4, 30.5, 30.2, 30.0, 29.7, 29.7, 29.3, 29.0, 29.1, 28.7, 28.5, 28.5]

    generate_graph(_timestamps, _humidities, _temperatures)