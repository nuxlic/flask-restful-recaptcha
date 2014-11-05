import speech_recognition as sr
import string
import sys

"""
num = { '0':'ZERO', 
	'1':'ONE', 
	'2':'TWO', 
	'3':'THREE', 
	'4':'FOUR',
	'5':'FIVE',
	'6':'SIX',
	'7': 'SEVEN',
	'8':'EIGHT',
	'9':'NINE'}
"""



def GoogleRecognizer(wavfile):
    out = ''
    r = sr.Recognizer()
    with sr.WavFile(sys.argv[1]) as source:              # use "test.wav" as the audio source
        audio = r.record(source)                        # extract audio data from the file

    try:
        r = r.recognize(audio)   # recognize speech using Google Speech Recognition
        out = r
	#for l in r:
	#        if l in string.digits:
        #        out += num[l] + ' '
        #    else:
        #        return -1
       
    except LookupError:                                 # speech is unintelligible
            return -1

    return out

if __name__ == '__main__':
    import sys
    print GoogleRecognizer(sys.argv[1])
