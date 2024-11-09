from flask import Flask, render_template, request, redirect, url_for
from app.analyzer import preprocess_chat, analyze_messages

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = f"app/uploads/{file.filename}"
        file.save(file_path)
        messages = preprocess_chat(file_path)
        analyze_messages(messages)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
