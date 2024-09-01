import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import pytz

# Define a regular expression pattern to extract the necessary components
pattern1 = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\]: \(Team #\d\) (.+?) sent (.+?) to (.+?)'
pattern2 = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\]: Notice \(all\): (.+?) \(Team #\d\) has completed their goal.'

# Function to process each line
def process_line(line):
    match1 = re.match(pattern1, line)
    match2 = re.match(pattern2, line)

    if match1:
        # Extracted values from the first pattern
        date_time = match1.group(1)
        category = match1.group(2)
        
        return date_time, category

    elif match2:
        # Extracted values from the second pattern
        date_time = match2.group(1)
        
        return date_time, "completed goal"

    return None

# File path
file_path = 'f144HvXqQKmRVuWoEHFrvA.txt'

# Initialize counters and storage for time series data
checks = 0
goals = 0
time_series_data = []  # List to store time, checks, and goals

# print(non_cleared)

# Reading the file and processing each line
with open(file_path, 'r') as file:
    for line in file:
        result = process_line(line.strip())
        if result:
            date_time_str, category = result
            # Convert date_time_str to a datetime object for easier processing
            date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S,%f')
            
            if category == "completed goal":
                goals += 1
            else:
                checks += 1
            
            # Store the time, checks, and goals count at this point in time
            time_series_data.append({
                'time': date_time_str,
                'checks': checks,
                'goals': goals
            })

# Dark mode style settings with dark gray background
def dark_mode():
    plt.style.use('dark_background')
    plt.rcParams.update({
        'axes.facecolor': '#2e2e2e',
        'figure.facecolor': '#2e2e2e',
        'axes.edgecolor': '#ffffff',
        'text.color': '#ffffff',
        'axes.labelcolor': '#ffffff',
        'xtick.color': '#ffffff',
        'ytick.color': '#ffffff',
        'grid.color': '#444444'
    })

# Plot and save time series graph
def plot_time_series(data, filename):
    dark_mode()  # Assuming this sets a dark theme for the plot
    df = pd.DataFrame(data)
    
    if len(data) > 0:
        plt.figure(figsize=(12, 6))
        
        # Plot the 'checks' on the primary y-axis
        ax1 = plt.gca()  # Get the current axis for the primary y-axis
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S,%f')
        ax1.plot(df['time'], df['checks'], label='Checks', color=(0/255, 255/255, 255/255, 1))
        
        
        # Create a twin y-axis to plot 'goals' on a secondary axis
        ax2 = ax1.twinx()
        ax2.plot(df['time'], df['goals'], label='Goals', color=(255/255, 0/255, 0/255, 1))
        
        # Customize axis labels
        ax1.set_xlabel('Time', color='white')
        ax1.set_ylabel('Checks', color=(0/255, 255/255, 255/255, 1))
        ax2.set_ylabel('Goals', color=(255/255, 0/255, 0/255, 1))
        
        # Title and grid
        plt.title('Evolution of Checks and Goals Over Time', color='white')
        ax1.grid(True, color='gray')
        
        # Customize tick colors for both y-axes
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='cyan')
        ax2.tick_params(axis='y', colors='red')
        
        # Manually combine legends from both axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # Adjust layout and save the figure
        plt.tight_layout()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

plot_time_series(time_series_data, 'time_series_plot_simple.png')

# Define the timezone you want to use
timezone = pytz.timezone('Europe/Amsterdam')  # Replace 'Your/Timezone' with the desired timezone

# Get the current time in the specified timezone
now = datetime.now(timezone)

# Format the time with the timezone information
timenow = now.strftime('%Y-%m-%d %H:%M:%S %Z%z')  # %Z is the timezone name, %z is the UTC offset

print("Image saved.")