from flask import Flask, redirect, send_file

app = Flask(__name__)

@app.route('/')
def home():  # Changed function name to be more descriptive
    return send_file("index.html")

if __name__ == "__main__":  # Ensures script runs only when executed directly
    app.run(debug=True)
