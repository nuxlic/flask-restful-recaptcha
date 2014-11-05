import recog_google
import recog_sphinx
import json
import urllib
import os
import tempfile
import urllib2
import random
import string
import subprocess


API_REST_URL='http://localhost:5000/captcha/'
WAV_EXTENSION = '.wav'
MP3_EXTENSION = '.mp3'
OUTPUT_DIRECTORY = './captcha_audios'

RECAPTCHA_CHALLENGE_FIELD = 'recaptcha_challenge_field'
RECAPTCHA_RESPONSE_FIELD = 'recaptcha_response_field'

SPHINX_RECOG = 1
WINDOWS_RECOG = 2

SR_RECOG = 2
NUM_OF_EXECUTION = 10
RESULT_OK = 200

REMOTE_IP = '192.168.9.136'
REMOTE_PORT = 8093


def log(msg):
    print msg

def get_from_api_rest():
    return json.loads(urllib.urlopen(API_REST_URL).read())
    
def send_result_using_api_rest(captcha, r_c_field):
    r = urllib2.Request(API_REST_URL, json.dumps({RECAPTCHA_CHALLENGE_FIELD:r_c_field, RECAPTCHA_RESPONSE_FIELD: captcha}))

    try:
        return urllib2.urlopen(r).getcode()
    except urllib2.HTTPError, e:
        return e.code


def get_random_filename():
    return ''.join([random.choice(string.letters) for _ in range(8)])

def save_mp3_content(json_, out_dir):
    mp3_name = get_random_filename()
    mp3_name += MP3_EXTENSION
    full_path = os.path.join(out_dir, mp3_name)
    urllib.urlretrieve(json_['audio_link'], full_path)
    return full_path

def get_audio_file(directory):
    jsonFromApiRest = get_from_api_rest()
    #print jsonFromApiRest
    mp3_file_path = save_mp3_content(jsonFromApiRest, directory)
    return (mp3_file_path, jsonFromApiRest[RECAPTCHA_CHALLENGE_FIELD])
    
def download_audiofile(dir_):
    wav_information = get_audio_file(dir_)
    return wav_information

def convert_to_wav(audio_path, o_dir):
    new_filename = os.path.join(o_dir, get_random_filename() + WAV_EXTENSION)
    subprocess.check_output(["/usr/bin/mpg123", "-w", new_filename, audio_path])
    os.unlink(audio_path)
    return new_filename



def get_result_windows_recognizer(wav_path):
    fd = open(wav_path, "rb")
    buff = fd.read()
    fd.close()

    s = socket.socket()

    s.connect((REMOTE_IP, REMOTE_PORT))
    s.settimeout(1000)
    
    s.send(NUM_OF_EXECUTION)
    send_result = s.read()

    if send_result != 'OK':
        raise Exception("Num of execution FAIL!")

    s.send(buff)
    r = s.read()

    s.close()
   
    return dict(r)
 


def get_result_using_sphinx(wav_path):
    for i in range(NUM_OF_EXECUTION):
        captcha = recog_sphinx.SphinxRecognizer(wav_path)
    
        if sphinx_results.get(captcha) is None:
            sphinx_results[captcha] = 1
        else:
            sphinx_results[captcha] +=  1
    
    return sphinx_results



if __name__ == "__main__":
    results = {}
    sphinx_results = {}
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.mkdir(OUTPUT_DIRECTORY)

    audio_path, response_field = download_audiofile(OUTPUT_DIRECTORY)
    wav_path = convert_to_wav(audio_path, OUTPUT_DIRECTORY)

    #import sys 
    #response_field = 1
    #wav_path = sys.argv[1]
   
    #windows_results = get_result_windows_recognizer(wav_path)
    sphinx_results = get_result_using_sphinx(wav_path) 



    #calculamos el resultado total
    for k in windows_results.keys():
        if k in sphinx_results.keys():
            results[k] = sphinx_results[k] + windows_results[k]


    captcha = sorted(results.items(), key=lambda x: x[1], reverse=True)[0][0]

    #Trying to identify if the recognizer match some result
    #recognized_match = True if captcha in windows_results.keys() and captcha in sphinx_results.keys() else False

    #if not recognized_match:
               


    captcha_sphinx = sorted(sphinx_results.items(), key=lambda x: x[1], reverse=True)[0][0]
    captcha_windows = sorted(windows_results.items(), key=lambda x: x[1], reverse=True)[0][0]


    r_code = send_result_using_api_rest(captcha, response_field)
    
    recognized_by = 0

    if r_code == RESULT_OK:
        if captcha == captcha_windows:
            recognized_by = WINDOWS_RECOG

        if captcha == captcha_sphinx:
            recog_google |= SPHINX_RECOG 
    
        
    

    print r_code 
    
