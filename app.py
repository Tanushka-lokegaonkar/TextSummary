import torch
from flask import Flask, render_template_string, request

# Use a pipeline as a high-level helper
from transformers import pipeline

text_summary = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", torch_dtype=torch.bfloat16)

def summary(para) :
    output = text_summary(para)
    return output[0]['summary_text']

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return render_template_string('''
    <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GenSummary</title>
            <style>
                body {
                    font-family: Arial, Helvetica, sans-serif;
                    background-color: #f4f4f4;
                    padding: 30px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                .container {
                    background-color: white;
                    padding: 30px;
                    max-width: 60vh;
                    margin: auto;
                    border-radius: 10px;
                    box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
                }

                h1 {
                    color: #007bff;
                    margin-bottom: 20px;
                }

                label {
                    font-weight: bold;
                    display: block;
                    margin-bottom: 5px;
                }

                input {
                    width: 100%;
                    padding: 10px;
                    font-size: 16px;
                    margin-bottom: 15px;
                    border: 1px solid #ccc;
                }

                button {
                    background-color: #343a40;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 10px;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #23272b;
                }

                .loading {
                    font-style: italic;
                    color: #777;
                    margin-top: 10px;
                }

                .output-box {
                    margin-top: 20px;
                    border: 1px solid gray;
                    padding: 0;
                    border-radius: 5px;
                }

                .output-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    font-weight: bold;
                    margin-bottom: 10px;
                    background-color: #007bff;
                    color: white;
                    padding: 10px;
                    border-top-left-radius: 5px;
                    position: relative;
                }
                .output-text{
                    padding: 5px;
                    background-color: white;
                    color: black;
                }
                .copy-btn {
                    background-color: #707274;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    cursor: pointer;
                }

                p {
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }

                .privacy-box {
                    margin-top: 20px;
                    background-color: #d1f0f9;
                    padding: 15px;
                    border: 2px solid #25cde7aa;
                    border-radius: 5px;
                    color: #0c5460;
                    font-size: 14px;
                }
            </style>
        </head>

        <body>
            <div class="container">
                <form id="tutorial-form" onsubmit="event.preventDefault(); generateContent()">
                    <h1>GenSummary: AI Summary Generator</h1>

                    <label for="courseTitle">Text :</label>
                    <textarea id="course" placeholder="Enter the text" rows="10" cols="50"></textarea>
                    <button type="submit">Generate Summary</button>
                </form>

                <p id="loadingMsg" class="loading" style="display: none;">Generating summary, please wait...</p>
                <div class="output-box" id="outputBox">
                    <div class="output-header">
                        <span>Output: </span>
                        <button onclick="copyOutput()" class="copy-btn">Copy</button>
                    </div>
                    <div class="output-text">
                        <p id="outputText"></p>
                    </div>

                </div>

                <div class="privacy-box">
                    <strong>Data Privacy Notice:</strong> Your input data is used only to generate educational content and is
                    not stored or logged.
                </div>
            </div>

            <script>
                async function generateContent() {
                    const course = document.getElementById('course').value;
                    const outputBox = document.getElementById('outputBox');
                    const outputText = document.getElementById('outputText');
                    const loadingMsg = document.getElementById('loadingMsg');

                    outputBox.style.display = 'none';
                    loadingMsg.style.display = 'block';

                    const formData = new FormData();
                    formData.append('course', course);

                    const response = await fetch('/generate', {
                        method: 'POST',
                        body: formData
                    });

                    const outtext = await response.text();
                    outputText.innerText = outtext;
                    outputBox.style.display = 'block';
                    loadingMsg.style.display = 'none';
                }

                function copyOutput() {
                    const outputText = document.getElementById('outputText').innerText;
                    navigator.clipboard.writeText(outputText)
                        .then(() => alert("Output copied to clipboard!"))
                        .catch(() => alert("Failed to copy."));
                }
            </script>
        </body>

        </html>''')

@app.route('/generate',methods=['POST'])
def generate():
    course = request.form['course']
    return summary(course)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
