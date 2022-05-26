from google.cloud import speech_v1
from google.cloud import storage


def get_file_uri(file_name, bucket_name):
    """Returns the file's URI"""
    gcs_uri = 'gs://' + bucket_name + '/' + file_name
    return gcs_uri


async def delete_blob(bucket_name, blob_name):
    """Deletes an audio file from the bucket."""
    storage_client = storage.Client.from_service_account_json('key.json')
    bucket = storage_client.get_bucket(bucket_name)
    audio_file = bucket.blob(blob_name)

    audio_file.delete()

    print("File deleted")


async def upload_audio(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    # Instantiates a client
    storage_client = storage.Client.from_service_account_json('key.json')
    bucket = storage_client.bucket(bucket_name)
    audio = bucket.blob(destination_blob_name)

    audio.upload_from_file(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    return destination_blob_name


async def speech_to_text_google(file, language, filename, minfo_channels):
    # uri is a string
    # Instantiates a client
    client = speech_v1.SpeechAsyncClient.from_service_account_file('key.json')

    # Uploads the audio

    print("Waiting for upload...")

    file_name = await upload_audio("montreux_test", file, filename)
    # Gets uri
    uri = get_file_uri(file_name, "montreux_test")
    audio = speech_v1.RecognitionAudio(uri=uri)

    config = speech_v1.RecognitionConfig(
        language_code=language,
        audio_channel_count=int(minfo_channels),
        enable_automatic_punctuation=True,
    )
    operation = await client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")

    response = await operation.result()
    # Creating output
    transcription = ""

    # status update every 3 minutes for
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        transcription += result.alternatives[0].transcript
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    await delete_blob("montreux_test", file_name)

    return transcription
