from flask import Response, request
from flask_restful import Resource, reqparse

from recaptcha.client import captcha

class CaptchaController(Resource):
    def get(self):
        captcha_html = captcha.displayhtml("6LdaFvsSAAAAAHJrA4ETTAcWRaXpcKKMWx_ErwU- ")

        html = """
        <form action="validate" method="post">
        %s
        <input type=submit value="Submit Captcha Text" \>
        </form>
        """%captcha_html

        return Response(html)


class ValidateSubController(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('recaptcha_challenge_field', type=str)
    parser.add_argument('recaptcha_response_field', type=str)

    def post(self):
        args = ValidateSubController.parser.parse_args()
        response = captcha.submit(args['recaptcha_challenge_field'], args['recaptcha_response_field'],'6LdaFvsSAAAAAPhdPEuKa5KBOYNGNPNCkhxIo8mG', request.headers.get('REMOTE_ADDR'))
        if response.is_valid:
            return "NICE"
        else:
            return "CHUPIT"