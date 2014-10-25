from flask.app import Flask
from flask_restful import Api
from controllers.captchacontroller import CaptchaController

app = Flask(__name__)
api = Api(app)

api.add_resource(CaptchaController, '/captcha/')

app.run(debug=True)