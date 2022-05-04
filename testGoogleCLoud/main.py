# Imports the Google Cloud client library
from google.cloud import speech
import io
<<<<<<< Updated upstream
=======
from pydub import AudioSegment
from pydub.silence import split_on_silence


def chunked():
    sound = AudioSegment.from_wav('MJ_test.wav')
    audio_chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=-40 )

    for i, chunk in enumerate(audio_chunks):
        output_file = "/Users/johancuda/PycharmProjects/pythonProject/testGoogleCLoud/chunks/chunk{0}.wav".format(i)
        print("Exporting file", output_file)
        chunk.export(output_file, format="wav")
>>>>>>> Stashed changes


def main():

    # Instantiates a client
    client = speech.SpeechClient.from_service_account_file('key.json')

    # The name of the audio file to transcribe
    file_name = "/Users/johancuda/PycharmProjects/pythonProject/testGoogleCLoud/MJ_test.wav"

    with io.open(file_name, 'rb') as f:
        audio_file=f.read()

<<<<<<< Updated upstream
    #audio = speech.RecognitionAudio(content=audio_file)
    audio = speech.RecognitionAudio(uri="gs://montreux_test/355009.wav")

    config = speech.RecognitionConfig(
        language_code="fr-FR",
        audio_channel_count=1,
        enable_automatic_punctuation=True,
=======
    audio = speech.RecognitionAudio(content=audio_file)

    config = speech.RecognitionConfig(
        language_code="en-US",
        audio_channel_count=1,
>>>>>>> Stashed changes
    )
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
<<<<<<< Updated upstream
    response = operation.result()

    #status update every 3 minutes for
=======
    response = operation.result(timeout=90)
>>>>>>> Stashed changes

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