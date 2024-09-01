import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import pytz
import csv

plot_old = False

# Define a regular expression pattern to extract the necessary components
pattern1 = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\]: \(Team #\d\) (Player\d+) sent (.+?) to (Player\d+) \((\d+)\ score\)'
pattern2 = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\]: Notice \(all\): (Player\d+) \(Team #\d\) has completed their goal.'
pattern3 = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\]: Notice \(all\): (Player\d+) \(Team #\d\) playing Yacht Dice has joined. Client(0.4.2), \[\].'


# Function to process each line
def process_line(line):
    match1 = re.match(pattern1, line)
    match2 = re.match(pattern2, line)
    match3 = re.match(pattern3, line)

    if match1:
        # Extracted values from the first pattern
        date_time = match1.group(1)
        player1 = match1.group(2)
        category = match1.group(3)
        player2 = match1.group(4)
        score = match1.group(5)
        
        return date_time, player1, category, player2, score

    elif match2:
        # Extracted values from the second pattern
        date_time = match2.group(1)
        player = match2.group(2)
        
        return date_time, player, "completed goal", None, None
    
    elif match3:
        # Extracted values from the second pattern
        date_time = match2.group(1)
        player = match2.group(2)
        
        return date_time, player, "logged in", None, None
        

    return None

# File path
file_path = 'fHr5TfTeT621SITPZ1SGdQ.txt'

# Initialize counters and storage for time series data
checks = 0
goals = 0
logged_in = 0
max_scores = {}
last_check = {}
n_points = {}
n_multipliers = {}
n_categories = {}
n_dice = {}
n_rolls = {}
time_series_data = []  # List to store time, checks, and goals

non_cleared = [f"{i}" for i in range(1, 2049)]
# print(non_cleared)

# Reading the file and processing each line
with open(file_path, 'r') as file:
    for line in file:
        result = process_line(line.strip())
        if result:
            date_time_str, player1, category, player2, score = result
            # Convert date_time_str to a datetime object for easier processing
            date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S,%f')
            
            if category == "completed goal":
                goals += 1
                non_cleared.remove(player1.replace("Player", ""))
            elif category == "logged in":
                logged_in += 1
            else:
                checks += 1
                max_scores[player2.replace("Player", "")] = score
                last_check[player2.replace("Player", "")] = date_time
                # print(date_time)
                if player2.replace("Player", "") not in n_points:
                    n_points[player2.replace("Player", "")] = 0
                    n_categories[player2.replace("Player", "")] = 0
                    n_multipliers[player2.replace("Player", "")] = 0
                    n_dice[player2.replace("Player", "")] = 0
                    n_rolls[player2.replace("Player", "")] = 0
                if category == "1 Point" or category == "Bonus Point":
                    n_points[player2.replace("Player", "")] += 1
                if category == "10 Points":
                    n_points[player2.replace("Player", "")] += 10
                if category == "100 Points":
                    n_points[player2.replace("Player", "")] += 100
                if category == "Fixed Score Multiplier" or category == "Step Score Multiplier":
                    n_multipliers[player2.replace("Player", "")] += 1
                if category.startswith("Category"):
                    n_categories[player2.replace("Player", "")] += 1
                if category == "Roll":
                    n_rolls[player2.replace("Player", "")] += 1
                if category == "Dice":
                    n_dice[player2.replace("Player", "")] += 1
                if category == "Roll Fragment":
                    n_rolls[player2.replace("Player", "")] += 1/4
                if category == "Dice Fragment":
                    n_dice[player2.replace("Player", "")] += 1/4
                
                    
                    
            
            # Store the time, checks, and goals count at this point in time
            time_series_data.append({
                'time': date_time_str,
                'checks': checks,
                'goals': goals,
                'logged_in': logged_in
            })
print(logged_in)
N = 300
# Convert dictionary values to integers and sort by value
sorted_keys1 = sorted(last_check, key=lambda k: last_check[k])[:N]
sorted_keys2 = sorted(last_check, key=lambda k: max_scores[k])[:N]
sorted_keys3 = sorted(last_check, key=lambda k: n_points[k], reverse=True)[:N]
sorted_keys4 = sorted(last_check, key=lambda k: n_multipliers[k], reverse=True)[:N]
sorted_keys5 = sorted(last_check, key=lambda k: n_categories[k], reverse=True)[:N]
sorted_keys6 = sorted(last_check, key=lambda k: n_dice[k], reverse=True)[:N]
sorted_keys7 = sorted(last_check, key=lambda k: n_rolls[k], reverse=True)[:N]
sorted_keys8 = sorted(last_check, key=lambda k: n_points[k] / 50 + n_multipliers[k] + n_categories[k] + 3 * n_dice[k] + 2 * n_rolls[k], reverse=True)[:N]

s3 = list(set(non_cleared) & set(sorted_keys3))
s4 = list(set(non_cleared) & set(sorted_keys4))
s5 = list(set(non_cleared) & set(sorted_keys5))
s6 = list(set(non_cleared) & set(sorted_keys6))
s7 = list(set(non_cleared) & set(sorted_keys7))
s8 = list(set(non_cleared) & set(sorted_keys8))

# Save the sorted keys to a .txt file
with open('S3.txt', 'w') as txt_file:
    for key in s3:
        txt_file.write(f"{key}\n")
# Save the sorted keys to a .txt file
with open('S4.txt', 'w') as txt_file:
    for key in s4:
        txt_file.write(f"{key}\n")
# Save the sorted keys to a .txt file
with open('S5.txt', 'w') as txt_file:
    for key in s5:
        txt_file.write(f"{key}\n")
# Save the sorted keys to a .txt file
with open('S6.txt', 'w') as txt_file:
    for key in s6:
        txt_file.write(f"{key}\n")
# Save the sorted keys to a .txt file
with open('S7.txt', 'w') as txt_file:
    for key in s7:
        txt_file.write(f"{key}\n")
# Save the sorted keys to a .txt file
with open('S8.txt', 'w') as txt_file:
    for key in s8:
        txt_file.write(f"{key}\n")
        
# Save the sorted keys to a .txt file
with open('random_worlds.txt', 'w') as txt_file:
    for key in non_cleared:
        txt_file.write(f"{key}\n")
        
if plot_old:
    # File path
    file_path_old = 'logYD.txt'

    # Initialize counters and storage for time series data
    checks_old = 0
    goals_old = 0
    max_scores_old = {}
    last_check_old = {}
    time_series_data_old = []  # List to store time, checks, and goals

    # Parsing the date strings into datetime objects
    date_time_str1 = '2024-06-08 19:25:48,661'
    date_time_str2 = '2024-08-23 18:01:54,511'

    date_time1 = datetime.strptime(date_time_str1, '%Y-%m-%d %H:%M:%S,%f')
    date_time2 = datetime.strptime(date_time_str2, '%Y-%m-%d %H:%M:%S,%f')

    # Calculating the difference
    difference = date_time2 - date_time1

    # Reading the file and processing each line
    with open(file_path_old, 'r') as file:
        for line in file:
            result = process_line(line.strip())
            if result:
                date_time_str, player1, category, player2, score = result
                # Convert date_time_str to a datetime object for easier processing
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S,%f') + difference
                
                # Converting the new datetime back to a string
                date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S,%f')
                
                
                if category == "completed goal":
                    goals_old += 1
                else:
                    checks_old += 1
                    max_scores_old[player1.replace("Player", "")] = score
                    last_check_old[player1.replace("Player", "")] = date_time
                    # print(date_time)
                
                # Store the time, checks, and goals count at this point in time
                time_series_data_old.append({
                    'time': date_time_str,
                    'checks': checks_old,
                    'goals': goals_old
                })
            
print("Data has been processed.")

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

# Plot and save the gauge
def plot_gauge(value, total, title, filename):
    dark_mode()
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
    sizes = [value, total - value]
    labels = [f'{title} ({value})', 'Remaining']
    colors = ['#1f77b4', '#444444']  # Dark mode colors
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title(f"{title}: {value} / {total}", color='white')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

# Plot and save histogram of max scores
def plot_histogram(data, filename):
    dark_mode()
    plt.figure(figsize=(10, 6))
    sns.histplot(data, bins=40, kde=True, color='skyblue')
    plt.title('Histogram of Max Scores', color='white')
    plt.xlabel('Score', color='white')
    plt.ylabel('Frequency', color='white')
    plt.grid(True, color='gray')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    
    # Plot and save histogram of max scores
def plot_histogram_time(data, filename):
    dark_mode()
    plt.figure(figsize=(10, 6))
    sns.histplot(data, bins=40, kde=True, color='skyblue')
    plt.title('Histogram of the time worlds were last played', color='white')
    plt.xlabel('Time last played', color='white')
    plt.ylabel('Frequency', color='white')
    plt.grid(True, color='gray')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

# Plot and save time series graph
def plot_time_series(data, old_data, filename):
    dark_mode()  # Assuming this sets a dark theme for the plot
    df = pd.DataFrame(data)
    df_old = pd.DataFrame(old_data)
    
    if len(data) > 0:
        
        plt.figure(figsize=(12, 6))
        
        # Plot the 'checks' on the primary y-axis
        ax1 = plt.gca()  # Get the current axis for the primary y-axis
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S,%f')
        ax1.plot(df['time'], df['checks'], label='Checks', color=(0/255, 255/255, 255/255, 1))
        
        
        # Create a twin y-axis to plot 'goals' on a secondary axis
        ax2 = ax1.twinx()
        ax2.plot(df['time'], df['goals'], label='Goals', color=(255/255, 0/255, 0/255, 1))
        
        if plot_old:
            df_old['time'] = pd.to_datetime(df_old['time'], format='%Y-%m-%d %H:%M:%S,%f')        
            ax1.plot(df_old['time'], df_old['checks'], label='Checks 1024YD', color=(224/255, 255/255, 255/255, 1/3))
            ax2.plot(df_old['time'], df_old['goals'], label='Goals 1024YD', color=(255/255, 0/255, 0/255, 1/3))
            ax2.set_ylim(0, 10)
        
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


# Plot and save last update text image with minimal margin and transparent background
def plot_last_update(timenow, filename):
    dark_mode()
    fig, ax = plt.subplots(figsize=(8, 1), dpi=100)  # Adjust the figure size to fit the text more closely
    ax.text(0.5, 0.5, f"Last update: {timenow}", color='white', fontsize=16, ha='center', va='center')
    
    # Remove default margins by setting limits tightly around the text
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Hide the axis
    ax.axis('off')
    
    # Save the figure with a transparent background and minimal padding
    plt.savefig(filename, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()
    

# Generate and save plots
plot_gauge(checks, 129652, 'Checks', 'checks_gauge.png')
plot_gauge(goals, 2048, 'Goals', 'goals_gauge.png')
plot_histogram(list(map(int, max_scores.values())), 'max_scores_histogram.png')
plot_histogram_time(list(last_check.values()), 'time_histogram.png')
plot_time_series(time_series_data, None if not plot_old else time_series_data_old, 'time_series_plot.png')

# Define the timezone you want to use
timezone = pytz.timezone('Europe/Amsterdam')  # Replace 'Your/Timezone' with the desired timezone

# Get the current time in the specified timezone
now = datetime.now(timezone)

# Format the time with the timezone information
timenow = now.strftime('%Y-%m-%d %H:%M:%S %Z%z')  # %Z is the timezone name, %z is the UTC offset


# Generate and save last update image
plot_last_update(timenow, 'last_update.png')

print("Images have been saved as 'checks_gauge.png', 'goals_gauge.png', 'max_scores_histogram.png', 'time_series_plot.png', and 'last_update.png'.")