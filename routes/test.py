from app import app


@app.route('/')
def hello_world():
    return "flask app is up and running!"

