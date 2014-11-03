import json
from BeautifulSoup import BeautifulSOAP
from flask import Response, request
from flask_restful import Resource, reqparse, abort

from recaptcha.client import captcha
import urllib
import re

class CaptchaController(Resource):
    PUBLIC_KEY = '6LdaFvsSAAAAAHJrA4ETTAcWRaXpcKKMWx_ErwU-'
    GOOGLE_URL_API = "http://www.google.com/recaptcha/api/"
    HTTP_FORBIDDEN = 403

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('recaptcha_challenge_field', type=str)
        self.parser.add_argument('recaptcha_response_field', type=str)

    def get(self):
        r = urllib.urlopen("%snoscript?k=%s&is_audio=true" % (self.GOOGLE_URL_API, self.PUBLIC_KEY) )
        inner_html = r.read()
        soup = BeautifulSOAP(inner_html)
        audio_link = re.findall("(image\?c=.*?)\">", inner_html)

        if audio_link is []:
            raise Exception("Audio link not Found")

        #find the challenge_field_value
        recaptcha_challenge_field = soup.find('input', {'id':'recaptcha_challenge_field'})['value']

        #build the url te return

        response = {
            'recaptcha_challenge_field': recaptcha_challenge_field,
            'audio_link'               : self.GOOGLE_URL_API + audio_link[0]
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