from flask import Response, request
from flask_restful import Resource, reqparse

from recaptcha.client import captcha

class CaptchaController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('recaptcha_challenge_field', type=str)
        self.parser.add_argument('recaptcha_response_field', type=str)

    def get(self):
        captcha_html = captcha.displayhtml("6LdaFvsSAAAAAHJrA4ETTAcWRaXpcKKMWx_ErwU- ")

        html = """
        <form action="/captcha/" method="post">
        %s
        <input type=submit value="Submit Captcha Text" \>
        </form>
        """%captcha_html

        return Response(html)

    def post(self):
        args = self.parser.parse_args()
        response = captcha.submit(args['recaptcha_challenge_field'],
                                  args['recaptcha_response_field'],'6LdaFvsSAAAAAPhdPEuKa5KBOYNGNPNCkhxIo8mG',
                                  request.headers.get('REMOTE_ADDR'))
        if response.is_valid:
            return "NICE"

        return "CHUPIT"