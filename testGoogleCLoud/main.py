# Imports the Google Cloud client library
from google.cloud import speech_v1
import io
import asyncio

# Imports the Google Cloud client library
from google.cloud import storage


def upload_audio(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    # Instantiates a client
    storage_client = storage.Client.from_service_account_file('key.json')
    bucket = storage_client.bucket(bucket_name)
    audio = bucket.blob(destination_blob_name)

    audio.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

#async useful or not?

async def speech_to_text_google(uri, language):
    # uri is a string
    # Instantiates a client
    client = speech_v1.SpeechAsyncClient.from_service_account_file('key.json')

    # The name of the audio file to transcribe
    # file_name = "/Users/johancuda/PycharmProjects/pythonProject/testGoogleCLoud/MJ_test.wav"

    # with io.open(file_name, 'rb') as f:
    # audio_file=f.read()

    # audio = speech.RecognitionAudio(content=audio_file)
    audio = speech_v1.RecognitionAudio(uri=uri)

    config = speech_v1.RecognitionConfig(
        language_code=language,
        audio_channel_count=1,
        enable_automatic_punctuation=True,
    )
    operation = await client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")

    response = await operation.result()


    # status update every 3 minutes for

    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    # Detects speech in the audio file
    # response = client.recognize(config=config, audio=audio)

    # for result in response.results:
    # print("Transcript: {}".format(result.alternatives[0].transcript))

    # return print(response)




if __name__ == "__main__":
    asyncio.run(speech_to_text_google("gs://montreux_test/machine-learning_speech-recognition_7601-291468-0006.wav", "en_US"))
