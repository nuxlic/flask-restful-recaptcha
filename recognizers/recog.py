import os
import httplib
import sys


def log(msg):
	print msg

class CaptchaSolver:
	pass

class GoogleSpeech(CaptchaSolver):

	def mp3ToFlac( pName ):
		"""
			This function conver a mp3 file format to Flac
			@return => None
		"""
		fname = os.path.splitext( pName )[0] + ".flac" 
		cmd = 'env lame %s %s.flac' % pName, fname
		os.sysem(cmd)

	def crack(self, fname):
		"""
			This function make the magick
		"""
		log('[+] Sending clean file to Google voice API')

		f = open(fname)
		data = f.read()
		f.close()

		google_speech = httplib.HTTPConnection('www.google.com')
		print 1
		google_speech.request('POST','/speech-api/v2/recognize?xjerr=1&client=chromium&lang=en-US',data,{'Content-type': 'audio/x-flac; rate=16000'})
		print 2
		text = google_speech.getresponse().read()
		print 3

		google_speech.close()
		print 4
		return text

c = GoogleSpeech()
print c.crack('./captchas/100.mp3')
