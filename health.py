from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return f'Hello, World! This is practice'
@app.route('/health')
def health():
    return f'Health check OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)