# Imports the Google Cloud client library
from google.cloud import speech
import io


def main():

    # Instantiates a client
    client = speech.SpeechClient.from_service_account_file('key.json')

    # The name of the audio file to transcribe
    file_name = "/Users/johancuda/PycharmProjects/pythonProject/testGoogleCLoud/MJ_test.wav"

    with io.open(file_name, 'rb') as f:
        audio_file=f.read()

    #audio = speech.RecognitionAudio(content=audio_file)
    audio = speech.RecognitionAudio(uri="gs://montreux_test/355009.wav")

    config = speech.RecognitionConfig(
        language_code="fr-FR",
        audio_channel_count=1,
        enable_automatic_punctuation=True,
    )
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result()

    #status update every 3 minutes for

    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    # Detects speech in the audio file
    #response = client.recognize(config=config, audio=audio)

    #for result in response.results:
       # print("Transcript: {}".format(result.alternatives[0].transcript))

    #return print(response)


"""le fichier est trop grand --> faut passer par google storage"""

if __name__ == "__main__":

    main()