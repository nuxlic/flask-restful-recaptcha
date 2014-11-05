import sys,os


num = { 'ZERO':'0', 
        'ONE':'1', 
        'TWO':'2', 
        'THREE':'3', 
        'FOUR':'4',
        'FIVE':'5',
        'SIX':'6',
        'SEVEN':'7',
        'EIGHT':'8',
        'NINE':'9'}



def decodeSpeech(hmmd,lmdir,dictp,wavfile):
    """
    Decodes a speech file
    """
    try:
        import pocketsphinx as ps
    except:
        import pocketsphinx as ps

    try:
        import sphinxba__se
    except:
        print """Pocket sphinx and sphixbase is not installed
                in your system. Please install it with package manager.
              """


    speechRec = ps.Decoder(hmm = hmmd, lm = lmdir, dict = dictp)
    wavFile = file(wavfile,'rb')
    wavFile.seek(44)
    speechRec.decode_raw(wavFile)
    result = speechRec.get_hyp()
    return result[0]



#if __name__ == "__main__":
def SphinxRecognizer(wavfile): 
    hmdir = "/usr/share/pocketsphinx/model/hmm/en/tidigits/"
    lmd = "/usr/share/pocketsphinx/model/lm/en/tidigits.DMP"
    dictd = "/usr/share/pocketsphinx/model/lm/en/tidigits.dic"
    recognised = decodeSpeech(hmdir,lmd,dictd,wavfile).strip()

    out = ''
    for word in recognised.split(' '):
        out += num[word]

    return out

if __name__ == "__main__":
    wavfile = sys.argv[1]
    print SphinxRecognizer(wavfile)
