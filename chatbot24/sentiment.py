import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re
from datetime import datetime
from graph import plot_sentiment_pie_chart

# Initialize the LLM model for sentiment analysis
model = OllamaLLM(model="llama3")

# Define a template for overall sentiment analysis
template = """
Analyze the overall sentiment of the following conversation.

Conversation:
{conversation}

Overall Sentiment:
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def extract_details_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

        # Extract conversation start time
        start_time_match = re.search(r'Conversation Start Time: (.+)', ''.join(lines))
        start_time_str = start_time_match.group(1) if start_time_match else "Unknown"

        # Extract conversation end time
        end_time_match = re.search(r'Conversation End Time: (.+)', ''.join(lines))
        end_time_str = end_time_match.group(1) if end_time_match else "Unknown"

        # Extract username from the first non-empty line
        username = lines[1].split(':')[0].strip() if len(lines) > 1 else "Unknown"

        # Convert start and end times to datetime objects
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S") if start_time_str != "Unknown" else None
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S") if end_time_str != "Unknown" else None

        return username, start_time, end_time

def calculate_total_time(start_time, end_time):
    if start_time and end_time:
        duration = end_time - start_time
        return duration
    return None

def analyze_overall_sentiment(file_path):
    # Extract username, start time, and end time from the conversation log file
    username, start_time, end_time = extract_details_from_file(file_path)

    if not username:
        print("Username could not be extracted from the file.")
        return

    with open(file_path, "r") as file:
        conversation = file.read()

    result = chain.invoke({"conversation": conversation})
    sentiment, explanation = extract_sentiment_and_explanation(result)

    print(f"Sentiment Analysis Result: {result}")

    total_time = calculate_total_time(start_time, end_time)
    total_time_str = total_time.total_seconds() // 60 if total_time else "Unknown"

    append_to_excel(username, sentiment, explanation, start_time.strftime("%Y-%m-%d %H:%M:%S") if start_time else "Unknown",
                     end_time.strftime("%Y-%m-%d %H:%M:%S") if end_time else "Unknown",
                     total_time_str)

def extract_sentiment_and_explanation(result):
    # Extract sentiment from the detailed explanation
    sentiment = "Neutral"  # Default value in case extraction fails
    explanation = result.strip()  # Entire result as explanation for now

    # Check for specific sentiment phrases in the explanation
    if "NEGATIVE" in explanation or "Negative" in explanation:
        sentiment = "Negative"
    elif "Sadness" in explanation or "SADNESS" in explanation:
        sentiment = "Negative"
    elif "POSITIVE" in explanation or "Positive" in explanation:
        sentiment = "Positive"
    elif "NEUTRAL" in explanation or "Neutral" in explanation:
        sentiment = "Neutral"
    elif "Mixed" in explanation or "MIXED" in explanation:
        sentiment = "Mixed"

    else:
        sentiment = "Unknown"
    return sentiment, explanation

def append_to_excel(username, sentiment, explanation, start_time, end_time, total_time):
    excel_file = "sentiment_analysis_logg.xlsx"

    data = {
        "Username": [username],
        "Overall Sentiment": [sentiment],
        "Explanation": [explanation],
        "Conversation Start Time": [start_time],
        "Conversation End Time": [end_time],
        "Total Conversation Time (minutes)": [total_time]  # New column for total time
    }
    df = pd.DataFrame(data)

    try:
        existing_df = pd.read_excel(excel_file)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        updated_df = df

    updated_df.to_excel(excel_file, index=False)
    plot_sentiment_pie_chart(excel_file)
