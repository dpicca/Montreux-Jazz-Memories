# Python Program To Use IBM Watson
# Studio's Speech To Text Below Code
# Accepts only .mp3 Format of Audio
# File
import json
import time
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# Insert API Key in place of
# 'YOUR UNIQUE API KEY'
authenticator = IAMAuthenticator('zl-n_Mb7J1NvDQPmfwaNIUeu7MWYbeyM1kMogpQs7k5F')
service = SpeechToTextV1(authenticator=authenticator)

# Insert URL in place of 'API_URL'
service.set_service_url('https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/8ca8530d-8810-4e34-aac5-c22f199ef271')
#register_status = service.register_callback(
 #   'http://localhost:8000/',
  #  user_secret='ThisIsMySecret'
#).get_result()


def main():

    with open(join(dirname(__file__), '/Users/johancuda/PycharmProjects/pythonProject/testIBM/MJ_test.wav'),
                  'rb') as audio_file:
        recognition_job = service.create_job(
            audio_file,
            content_type='audio/wav',
            #callback_url="http://localhost:8000/",
            #events=recognitions.completed_with_results,
            model='fr-FR_BroadbandModel',
            keywords=['test'],
            keywords_threshold=0.5,
            max_alternatives=1).get_result()
    print(json.dumps(recognition_job, indent=2))
    iD = recognition_job['id']
    print(iD)
    recognition_job1 = service.check_job(iD).get_result()
    while recognition_job1['status'] == "waiting" or recognition_job1 == "processing":
        time.sleep(60)
        recognition_job1 = service.check_job(iD).get_result()

    print(json.dumps(recognition_job1, indent=2))



# use asynchronous model with various elemnts (split on silence, background noise etc...) but check if you have to
# create/register jobs
# you have to register a callback then create a job

# TODO: check asynchronous python to wait for the response, check callback url to handle that


if __name__ == "__main__":

    main()
