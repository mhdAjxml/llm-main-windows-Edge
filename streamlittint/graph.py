import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_sentiment_pie_chart(excel_file):
    """
    Plots a pie chart showing the distribution of sentiments and displays the total number of unique users.

    Args:
        excel_file (str): Path to the Excel file containing sentiment data.
    """
    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_file)

    # Count unique users
    unique_users = df['Username'].nunique()

    # Count occurrences of each sentiment
    sentiment_counts = df['Overall Sentiment'].value_counts()

    # Define colors for the pie chart
    colors = ['#66b3ff', '#99ff99', '#ffcc99', '#ff9999']

    # Create the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
            startangle=140, colors=colors, wedgeprops={'edgecolor': 'white'})

    # Add a title
    plt.title('Overall Sentiment Distribution', fontsize=16)

    # Add unique user count as text
    plt.text(1.2, -1.3, f'Total Unique Users: {unique_users}', fontsize=12, ha='right')

    # Display the pie chart in Streamlit
    st.pyplot(plt)


