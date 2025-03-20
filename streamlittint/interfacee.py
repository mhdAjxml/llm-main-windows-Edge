import streamlit as st
import bcrypt
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from sentiment import analyze_overall_sentiment
# Initialize the model and prompt template
template = """
Answer the qn below

History : {context}

Question : {question}

Answer :
"""
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


# Initialize session state variables if they don't exist
if 'context' not in st.session_state:
    st.session_state.context = ""
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'conversation_start_time' not in st.session_state:
    st.session_state.conversation_start_time = None
if 'conversation_end_time' not in st.session_state:
    st.session_state.conversation_end_time = None

def load_data():
    try:
        with open("database.txt", "r") as db:
            data = {}
            for line in db:
                if ',' in line:
                    a, b = line.split(",")
                    data[a.strip()] = b.strip()
        return data
    except FileNotFoundError:
        return {}

def save_data(username, hashed_password):
    with open("database.txt", "a") as db:
        db.write(f"{username}, {hashed_password}\n")

def log_conversation_start(username):
    if not st.session_state.conversation_start_time:
        st.session_state.conversation_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = f"{username}_conversation_log.txt"
        with open(log_file, "w") as log:
            log.write(f"Conversation Start Time: {st.session_state.conversation_start_time}\n")

def log_conversation(username, user_input, bot_response):
    log_file = f"{username}_conversation_log.txt"
    with open(log_file, "a") as log:
        log.write(f"{username}: {user_input}\n")
        log.write(f"Bot: {bot_response}\n")

def log_conversation_end(username):
    st.session_state.conversation_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"{username}_conversation_log.txt"
    with open(log_file, "a") as log:
        log.write(f'{username}:'"exit\n")
        log.write(f"Conversation End Time: {st.session_state.conversation_end_time}\n\n")
    analyze_overall_sentiment(f"{username}_conversation_log.txt")



def handle_convo(user_input):
    log_conversation_start(st.session_state.username)  # Log conversation start if not already logged
    response = chain.invoke({"context": st.session_state.context, "question": user_input})
    st.session_state.context += f"\n{user_input}\n{response}"
    log_conversation(st.session_state.username, user_input, response)  # Log the conversation
    return response

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if username and password:
            data = load_data()
            if username in data:
                hashed = data[username].strip('b').replace("'", "").encode('utf-8')
                if bcrypt.checkpw(password.encode(), hashed):
                    st.success("Login success!")
                    st.session_state.username = username
                    st.session_state.logged_in = True
                else:
                    st.error("Wrong password")
            else:
                st.error("Username doesn't exist")
        else:
            st.warning("Please enter both username and password")

def register():
    st.title("Sign Up")
    username = st.text_input("Enter a username")
    password1 = st.text_input("Create password", type='password')
    password2 = st.text_input("Confirm password", type='password')

    if st.button("Register"):
        if len(password1) > 8:
            if username:
                data = load_data()
                if username in data:
                    st.error("Username exists")
                else:
                    if password1 == password2:
                        hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
                        save_data(username, hashed_password)
                        st.success("User created successfully! Please login to proceed:")
                    else:
                        st.error("Passwords do not match")
            else:
                st.warning("Please provide a username")
        else:
            st.error("Password too short")

def chatbot_interface():
    st.title("Chatbot Interface")

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    user_input = st.text_area("Ask your question:", value=st.session_state.user_input)

    if st.button("Submit"):
        if user_input:
            if user_input.lower() == "exit":
                st.write("**Bot:** Have a good day!")
                log_conversation_end(st.session_state.username)  # Log conversation end
                st.session_state.logged_in = False
                st.session_state.context = ""
                st.session_state.username = ""
                st.session_state.user_input = ""
                st.balloons()
                st.write("You can now close this tab or window.")
            else:
                response = handle_convo(user_input)
                st.write("**Bot:**")
                st.write(response)
                st.session_state.user_input = ""
        else:
            st.warning("Please enter a query")

def main():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        chatbot_interface()
    else:
        st.sidebar.title("Navigation")
        option = st.sidebar.radio("Choose an option", ["Login", "Sign Up"])

        if option == "Login":
            login()
        elif option == "Sign Up":
            register()

if __name__ == "__main__":
    main()