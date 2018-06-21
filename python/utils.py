

from glob import iglob
from multiprocessing import Pool
from functools import partial
from os.path import join, isfile

def search_wav(data_path):
    file_list = []
    for filename in iglob('{}/**/*.WAV'.format(data_path), recursive=True):
        file_list.append(str(filename))
    for filename in iglob('{}/**/*.wav'.format(data_path), recursive=True):
        file_list.append(str(filename))
    return file_list

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def search_dir(data_path):
    file_list = []
    for filename in iglob('{}/*'.format(data_path), recursive=True):
        file_list.append(str(filename))
    return file_list

def search_files(file_dir):
    uid_dic = []
    pqc_list = []
    uid = file_dir.split('/')[-1]
    passage_file = join(file_dir, '{}_p.wav'.format(uid))
    question_file = join(file_dir, '{}_q.wav'.format(uid))
    choice_dir = join(file_dir, '{}_c'.format(uid))
    choice_list = sorted(search_wav(choice_dir))
    pqc_list.append(passage_file)
    pqc_list.append(question_file)
    pqc_list.extend(choice_list)


    return uid, pqc_list

import speech_recognition as asr

def Google_ASR(file_dir=None):
    r = asr.Recognizer()
    uid, pqc_list = search_files(file_dir)
    result = []
    result.append(uid)
    for test_file in pqc_list:
        if isfile(test_file):
            FLAG = True
            while FLAG:
                try:
                    with asr.AudioFile (test_file) as source:
                        audio = r.record(source)
                        G_result = r.recognize_google(audio, language='zh-TW')
                    FLAG = False
                    result.append(G_result)
                except:
                    print('Google error', test_file)
        else:
            result.append([])
    return result


from aip import AipSpeech
def Baidu_ASR(file_dir=None):

    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    uid, pqc_list = search_files(file_dir)
    result = []
    result.append(uid)
    for test_file in pqc_list:
        if isfile(test_file):
            FLAG = True
            # while FLAG:
            try:
                B_result = client.asr(get_file_content(test_file), 'wav', 
        16000, {'lan': 'zh',})['result'][0]
                result.append(B_result)
                FLAG = False
            except:
                print('Baidu error', test_file)
                tmp = client.asr(get_file_content(test_file), 'wav', 16000, {'lan': 'zh',})
                if tmp['err_msg'] == 'speech quality error.':
                    result.append([])
                    FLAG = False
        else:
            result.append([])
    return result


import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
def GCP_ASR(file_dir=None):

    client = speech.SpeechClient()
    FLAG = True
    config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='cmn-Hant-TW')

    uid, pqc_list = search_files(file_dir)
    result = []
    result.append(uid)
    for test_file in pqc_list:
        if isfile(test_file):
            FLAG = True
            while FLAG:
                try:
                    audio = types.RecognitionAudio(content=get_file_content(test_file))
                    config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000,
                    language_code='cmn-Hant-TW')
                    G_C_tmp = client.recognize(config, audio)
                    for result_tmp in G_C_tmp.results:
                        G_C_result = result_tmp.alternatives[0].transcript
                    result.append(G_C_result)
                    FLAG = False

                except:
                    print('GCP error', test_file)
        else:
            result.append([])
    return result
    

