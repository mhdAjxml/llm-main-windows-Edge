from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from sentiment import analyze_overall_sentiment

template = """
Answer the qn below

History : {context}

Question : {question}

Answer :
"""
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

"""
def handle_convo(username):
    context = f"{username}: "
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Welcome, {username}! Your TroubleShooter is here to help.")

    with open("conversation_log.txt", "w") as file:
        file.write(f"Conversation Start Time: {start_time}\n")
        # file.write(f"{username}: \n\n")
        while True:
            user_input = input(f"{username}: ")
            if user_input.lower() == "exit":
                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Have a good day!!")
                file.write(f"{username}: exit\nBot: Have a good day!!\n")
                file.write(f"\nConversation End Time: {end_time}\n")

                break

            result = chain.invoke({"context": context, "question": user_input})
            print("Bot:", result)

            # Save the conversation to the file
            file.write(f"{username}: {user_input}\nBot: {result}\n")

            # Update the context for the next iteration
            context += f"\n{username}: {user_input}\nBot: {result}"
    analyze_overall_sentiment("conversation_log.txt")"""

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
model = OllamaLLM(model="phi3")
#model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Global variable for storing the context
context = ""

def handle_convo(user_input):
    global context
    response = chain.invoke({"context": context, "question": user_input})
    context += f"\n{user_input}\n{response}"
    return response
