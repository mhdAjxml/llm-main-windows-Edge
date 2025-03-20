import streamlit as st
import bcrypt
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

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
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

def load_data():
    with open("database.txt", "r") as db:
        data = {}
        for line in db:
            if ',' in line:
                a, b = line.split(",")
                data[a.strip()] = b.strip()
    return data

def save_data(username, hashed_password):
    with open("database.txt", "a") as db:
        db.write(f"{username}, {hashed_password}\n")

def handle_convo(user_input):
    response = chain.invoke({"context": st.session_state.context, "question": user_input})
    st.session_state.context += f"\n{user_input}\n{response}"
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

    # Initialize the text input field with session state
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Text input field for user query
    user_input = st.text_input("Ask your question:", value=st.session_state.user_input)

    if st.button("Submit"):
        if user_input:
            if user_input.lower() == "exit":
                st.write("**Bot:** Have a good day!")
                st.session_state.logged_in = False
                st.session_state.context = ""
                st.session_state.username = ""
                st.session_state.user_input = ""
                st.balloons()  # Optional: to give a visual cue that the session is ending
                st.write("You can now close this tab or window.")
            else:
                response = handle_convo(user_input)
                st.write("**Bot:**")
                st.write(response)
                # Clear the input field by resetting the session state
                st.session_state.user_input = ""
        else:
            st.warning("Please enter a query")

def main():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # User is logged in, show the chatbot interface
        chatbot_interface()
    else:
        # User is not logged in, show login or sign-up options
        st.sidebar.title("Navigation")
        option = st.sidebar.radio("Choose an option", ["Login", "Sign Up"])

        if option == "Login":
            login()
        elif option == "Sign Up":
            register()

if __name__ == "__main__":
    main()
