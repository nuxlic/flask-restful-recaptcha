from flask.app import Flask
from flask_restful import Api
from controllers.captchacontroller import CaptchaController, ValidateSubController

app = Flask(__name__)
api = Api(app)

api.add_resource(CaptchaController, '/captcha/')
api.add_resource(ValidateSubController, '/captcha/validate')

app.run(debug=True)