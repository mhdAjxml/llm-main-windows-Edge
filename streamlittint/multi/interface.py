import streamlit as st
import argostranslate.package
import argostranslate.translate
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os


# Function to perform the translation
def translate_text(input_text, from_code, to_code):
    return argostranslate.translate.translate(input_text, from_code, to_code)


# Function to process the user input using Llama
def process_with_llama(context, question):
    template = """
    Answer the qn below

    History : {context}

    Question : {question}

    Answer :
    """
    model = OllamaLLM(model="llama3")  # Use the local Llama model
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model  # Combine prompt and model
    result = chain.invoke({"context": context, "question": question})  # Use invoke() to process input
    return result


# Streamlit UI
st.title("Chatbot Interface")
st.write("Enter the text you want to translate:")

# User input text box
input_text = st.text_area("Input Text")

# Language codes for translation
from_code = "hi"
to_code = "en"

# Button to trigger translation
if st.button("Process"):
    if input_text:
        # Step 1: Translate Hindi input to English
        translated_text = translate_text(input_text, from_code, to_code)
        st.write(f"Translated to English: {translated_text}")

        # Step 2: Use the translated English text for Llama processing
        context = "Previous conversation history or relevant context."
        response = process_with_llama(context, translated_text)
        st.write(f"Bot: {response}")

        # Step 3: Translate the Llama's response back to Hindi
        final_response = translate_text(response, "en", "hi")
        st.success(f"Final Translated Response: {final_response}")
    else:
        st.warning("Please enter some text to process.")
