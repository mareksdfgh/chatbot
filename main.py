# Installiere die benötigten Pakete:
# pip install eel markdown

import eel
import markdown
import ollama
import os

eel.init('web')

messages = []
chat_file = 'chat_history.txt'

def save_chat_history():
    with open(chat_file, 'w', encoding='utf-8') as file:
        for message in messages:
            file.write(f"{message['role']}: {message['content']}\n")

@eel.expose
def send(chat):
    global messages
    messages.append({'role': 'user', 'content': chat})

    response = ''
    stream = ollama.chat(model='llama3', messages=messages, stream=True)
    for chunk in stream:
        part = chunk['message']['content']
        response += part

    messages.append({'role': 'assistant', 'content': response})
    save_chat_history()  # Speichere den Chatverlauf nach jeder Nachricht
    return response

@eel.expose
def format_output(text):
    # Convert Markdown to HTML and preserve line breaks
    html_output = markdown.markdown(text)
    return html_output.replace('\n', '<br>')

# Starte die Eel-Anwendung
eel.start('index.html', size=(600, 400))
