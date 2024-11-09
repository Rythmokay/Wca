import re
import pandas as pd
import matplotlib.pyplot as plt

def preprocess_chat(file_path):
    timestamp_12hr = r"\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [APM]{2} -"
    timestamp_24hr = r"\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} -"

    with open(file_path, 'r', encoding='utf-8') as file:
        chat_data = file.readlines()

    messages = []
    for line in chat_data:
        if re.match(timestamp_12hr, line) or re.match(timestamp_24hr, line):
            messages.append(line.strip())
        else:
            messages[-1] += ' ' + line.strip()
    
    return messages

def analyze_messages(messages):
    df = pd.DataFrame(messages, columns=["raw_message"])
    df["timestamp"] = df["raw_message"].apply(lambda x: re.findall(r"\d{1,2}/\d{1,2}/\d{2}", x)[0])

    daily_message_counts = df['timestamp'].value_counts()
    plt.figure(figsize=(10, 6))
    daily_message_counts.plot(kind="bar")
    plt.title("Daily Message Counts")
    plt.xlabel("Date")
    plt.ylabel("Messages")
    plt.savefig("app/static/charts/daily_message_counts.png")
    return "Analysis Completed"
