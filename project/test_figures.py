
import matplotlib.pyplot as plt

# Data for six pie charts
sizes_list = [(6, 94), (29, 71), (19, 81), (48, 52), (18, 82), (45, 55)]
titles_graph = ["Case B11", "Case B12", "Case B21",
                "Case B22", "Case B31", "Case B32", ]

labels_list = ['A', 'B', 'C', 'D', 'E', 'F']
colors_list = ['#FFFF00', '#90EE90']  # Yellow and Light Green colors

# Create a figure with 6 subplots arranged in a 3x2 grid
fig, axs = plt.subplots(3, 2)

# Flatten the axs array for easy iteration
axs = axs.flatten()

legend_handles = []  # Store legend handles for each chart

# Iterate over each pie chart
for i, (sizes, labels) in enumerate(zip(sizes_list, labels_list)):
    ax = axs[i]
    patches = ax.pie(sizes, labels=['', ''], autopct='%1.0f%%', startangle=90, colors=colors_list)
    ax.set_title(titles_graph[i])

    # Store the first patch (representing Value 1) as a handle for the legend
    legend_handles.append(patches[0])

# Adjust layout
plt.tight_layout()

# Add legend for the entire figure
fig.legend(patches[0], ["PV generation", "Energy consumed from the network"], loc='lower right')


# Save the figure as 'six_pie_charts_with_single_legend.png'
plt.savefig('six_pie_charts_with_single_legend.png')

# Show the plot
plt.show()
