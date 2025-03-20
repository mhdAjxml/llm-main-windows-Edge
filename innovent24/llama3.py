import requests
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from sentiment import analyze_overall_sentiment


subscription_key = "DWbvznT76Z0bRUpbxxyCHF1umhYNcWwnsjxDJ7IykjT6WmlSfvtaJQQJ99ALACGhslBXJ3w3AAAbACOGLM7G"
endpoint = "https://api.cognitive.microsofttranslator.com"
region = "centralindia"



def translate_text(text, to_lang, from_lang=None):
    path = '/translate?api-version=3.0'
    url = endpoint + path
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-Type': 'application/json',
    }
    body = [{'text': text}]
    params = {'to': to_lang}
    if from_lang:
        params['from'] = from_lang

    response = requests.post(url, headers=headers, json=body, params=params)
    response_data = response.json()
    translated_text = response_data[0]['translations'][0]['text']
    return translated_text



def handle_convo(username):

    # Allow user to select a language
    print("Select your language:")
    print("1. Tamil")
    print("2. English")
    print("3. German")
    print("4. Hindi")
    print("5. Telugu")


    language_map = {'1': 'ta', '2': 'en', '3': 'de', '4': 'hi','5':'te'}
    choice = input("Enter your choice (1/2/3/4/5): ")
    if choice not in language_map:
        print("Invalid choice! Defaulting to English.")
        user_lang = 'en'
    else:
        user_lang = language_map[choice]

    context = f"{username}: "
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Welcome, {username}! Your TroubleShooter is here to help.")

    # Template for LLM model
    template = """
    Answer the qn below

    History : {context}

    Question : {question}

    Answer :
    """

    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    # Open conversation log file
    with open("conversation_log.txt", "w") as file:
        file.write(f"Conversation Start Time: {start_time}\n")

        while True:
            user_input = input(f"{username}: ")

            if user_input.lower() == "exit":
                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Have a good day!!")

                file.write(f"{username}: exit\nBot: Have a good day!!\n")
                file.write(f"\nConversation End Time: {end_time}\n")
                break

            # Translate input to English
            translated_input = translate_text(user_input, to_lang='en', from_lang=user_lang)
            print(f"Translated Input (English): {translated_input}")
           # st.write(f"Translated Input (English): {translated_input}")
            # Get response from LLM
            result = chain.invoke({"context": context, "question": translated_input})
            print(f"Bot (English): {result}")
           # st.write(f"Bot(English): {result}")

            # Translate the LLM response back to the user's language
            translated_output = translate_text(result, to_lang=user_lang)
            print(f"Bot ({user_lang}): {translated_output}")
            #st.write(f"Bot ({user_lang}): {translated_output}")
            # Log the conversation (only English inputs and outputs)
            file.write(f"{username}: {translated_input}\nBot: {result}\n")

            # Update context for LLM
            context += f"\n{username}: {translated_input}\nBot: {result}"

    analyze_overall_sentiment("conversation_log.txt")