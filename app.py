from flask import Flask

app = Flask(__name__)
app.config.update(
    SECRET_KEY=b"asfsdft76rtdjghfy4uiut?/dl][fhfvnu6rgh",
)

import views

if __name__ == '__main__':
    app.run(debug=True)