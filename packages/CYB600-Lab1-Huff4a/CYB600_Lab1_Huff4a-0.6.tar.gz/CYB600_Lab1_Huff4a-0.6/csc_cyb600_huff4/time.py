from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time: {current_time}"

def main():
    app.run(host='localhost', port=8000)

if __name__ == '__main__':
    main()

