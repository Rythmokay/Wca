import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

analyzer_bp = Blueprint('analyzer', __name__)

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@analyzer_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join("app/uploads", filename)
            file.save(filepath)
            chat_data = process_chat_file(filepath)
            user_activity = analyze_user_activity(chat_data)
            generate_visualizations(chat_data, user_activity)
            return render_template("index.html", user_activity=user_activity)
    return render_template("index.html")

def process_chat_file(filepath):
    chat_data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            if ", " in line and " - " in line:
                parts = line.split(" - ")
                date_time = parts[0]
                message_data = parts[1].split(": ")
                if len(message_data) > 1:
                    user = message_data[0]
                    message = message_data[1]
                    sentiment = TextBlob(message).sentiment.polarity
                    chat_data.append({
                        "timestamp": date_time,
                        "user": user,
                        "message": message,
                        "sentiment": "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
                    })
    return chat_data

def analyze_user_activity(chat_data):
    user_activity = Counter([entry["user"] for entry in chat_data])
    return user_activity

def generate_visualizations(chat_data, user_activity):
    user_message_counts = list(user_activity.values())
    user_names = list(user_activity.keys())

    # Pie chart for user activity
    plt.figure(figsize=(8, 6))
    plt.pie(user_message_counts, labels=user_names, autopct='%1.1f%%')
    plt.title('User Message Distribution')
    plt.savefig("app/static/images/user_activity_pie.png")
    plt.close()

    # Bar graph for user activity
    plt.figure(figsize=(10, 6))
    plt.bar(user_names, user_message_counts, color="skyblue")
    plt.xlabel("User")
    plt.ylabel("Number of Messages")
    plt.title("Messages per User")
    plt.savefig("app/static/images/user_activity_bar.png")
    plt.close()

    # Sentiment analysis pie chart
    sentiments = Counter([entry["sentiment"] for entry in chat_data])
    sentiment_counts = list(sentiments.values())
    sentiment_labels = list(sentiments.keys())

    plt.figure(figsize=(8, 6))
    plt.pie(sentiment_counts, labels=sentiment_labels, autopct='%1.1f%%', colors=['green', 'red', 'yellow'])
    plt.title('Sentiment Distribution')
    plt.savefig("app/static/images/sentiment_distribution.png")
    plt.close()

    # Time analysis for busiest days
    dates = [entry["timestamp"].split(",")[0] for entry in chat_data]
    date_counts = Counter(dates)
    date_keys = list(date_counts.keys())
    date_values = list(date_counts.values())

    plt.figure(figsize=(12, 6))
    plt.plot(date_keys, date_values, marker="o", color="purple")
    plt.xlabel("Date")
    plt.ylabel("Message Count")
    plt.xticks(rotation=45)
    plt.title("Messages by Date")
    plt.savefig("app/static/images/date_analysis.png")
    plt.close()
