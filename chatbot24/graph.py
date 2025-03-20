import pandas as pd
import matplotlib.pyplot as plt

def plot_sentiment_pie_chart(excel_file):
    # Load the Excel file
    df = pd.read_excel(excel_file)

    # Calculate unique users and sentiment counts
    unique_users = df['Username'].nunique()
    sentiment_counts = df['Overall Sentiment'].value_counts()

    # Define colors for the pie chart
    colors = ['#66b3ff','#99ff99','#ffcc99','#ff9999']  # Balanced color palette

    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
            startangle=140, colors=colors, wedgeprops={'edgecolor': 'white'})

    # Add a title
    plt.title('Overall Sentiment Distribution', fontsize=16)

    # Add total number of unique users in the bottom right corner
    plt.text(1.2, -1.3, f'Total Unique Users: {unique_users}', fontsize=12, ha='right')

    # Show the plot
    plt.show()

# Example usage:

