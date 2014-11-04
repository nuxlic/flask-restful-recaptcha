import json
from BeautifulSoup import BeautifulSOAP
from flask import Response, request
from flask_restful import Resource, reqparse, abort

from recaptcha.client import captcha
import urllib
import re
from robot import CaptchaPage


class CaptchaController(Resource):
    PUBLIC_KEY = '6LdaFvsSAAAAAHJrA4ETTAcWRaXpcKKMWx_ErwU-'
    GOOGLE_URL_API = "http://www.google.com/recaptcha/api/"
    HTTP_FORBIDDEN = 403

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('recaptcha_challenge_field', type=str)
        self.parser.add_argument('recaptcha_response_field', type=str)

    def get(self):
        captcha_page = CaptchaPage()
        audio_link = captcha_page.get_url_sound()
        recaptcha_challenge_field = captcha_page.get_recaptcha_challenge_field()
        captcha_page.close()
        response = {
            'recaptcha_challenge_field': recaptcha_challenge_field,
            'audio_link'               : audio_link
        }
        return Response(json.dumps(response))

    def post(self):
        args = self.parser.parse_args()
        response = captcha.submit(args['recaptcha_challenge_field'],
                                  args['recaptcha_response_field'],'6LdaFvsSAAAAAPhdPEuKa5KBOYNGNPNCkhxIo8mG',
                                  request.headers.get('REMOTE_ADDR'))
        if response.is_valid:
            return Response("NICE")

        return abort(self.HTTP_FORBIDDEN)