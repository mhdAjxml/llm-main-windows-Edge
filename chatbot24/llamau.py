import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import requests

# Initialize the model
model = OllamaLLM(model="llama3")

# Define the template
template = """Provide a detailed response to the following query. In addition, suggest a related YouTube video link for further reference. Query: {query}"""
prompt = ChatPromptTemplate.from_template(template)


# Function to get related YouTube video
def get_youtube_video(query):
    youtube_api_key = "AIzaSyBqGOIaeXwqoo6wtxEHWoJHf2tDNWzV4MI"  # Replace with your actual YouTube API key
    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={youtube_api_key}"
    response = requests.get(youtube_url)
    video_data = response.json()
    if "items" in video_data and len(video_data["items"]) > 0:
        return f"https://www.youtube.com/watch?v={video_data['items'][0]['id']['videoId']}"
    return None


# Combine the prompt and model chain
def generate_response(query):
    # First, generate the response using the model
    response = model.invoke(prompt.format(query=query))

    # Get related YouTube video
    video_link = get_youtube_video(query)

    # Return the response and YouTube video link
    return {
        "response": response,
        "video_link": video_link
    }


# Streamlit interface
st.title("Chatbot")

# Chat history to maintain conversation
if "history" not in st.session_state:
    st.session_state.history = []


# Function to display chat history
def display_chat():
    for msg in st.session_state.history:
        if msg['role'] == 'user':
            st.markdown(f"**You**: {msg['content']}")
        else:
            st.markdown(f"**Bot**: {msg['content']}")
        st.markdown("---")


# Input from user
user_input = st.text_input("Ask me anything:", "")

# Button to send the query
if st.button("Send") and user_input:
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": user_input})

    # Get response from the model and related YouTube video
    output = generate_response(user_input)

    # Add bot's response to history
    st.session_state.history.append({"role": "bot", "content": output["response"]})

    # Display the video link if available
    if output['video_link']:
        st.session_state.history.append(
            {"role": "bot", "content": f"Here is a related video: [Watch Video]({output['video_link']})"})

# Display the chat history once after adding new messages
if len(st.session_state.history) > 0:
    display_chat()
