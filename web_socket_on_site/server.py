from flask import Flask

app = Flask(__name__)


@app.route('/url-client', methods=('GET',))
def f():
    return 200

if __name__ == "__main__":
    app.run(
        host='localhost',
        port=5000,
    )