from flask import *
import mysql.connector
from google.cloud import speech_v1
from google.cloud import storage
import asyncio


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'DataBasic$'


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


# async useful or not?
async def speech_to_text_google(file, language):
    # uri is a string
    # Instantiates a client
    client = speech_v1.SpeechAsyncClient.from_service_account_file('key.json')

    # Uploads the audio

    print("Waiting for upload...")

    file_name = await upload_audio("montreux_test", file, "test2.wav")
    # Gets uri
    uri = get_file_uri(file_name, "montreux_test")
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

    await delete_blob("montreux_test", file_name)

    # return response.results
    return 'youpi youpos'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data


def insertBLOB(name, empAudio):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port='8889',
                                             user='root',
                                             password='root',
                                             database='mydb')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO interview (Text, Audio) VALUES (%s, %s)"""

        # Convert data into tuple format
        insert_blob_tuple = (name, empAudio)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Retranscription and audio file successfully uploaded to database", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            binary_audio = file.read()
            results = asyncio.run(speech_to_text_google(file, "en_US"))
            insertBLOB(results, binary_audio)


    return render_template('upload_revamp.html')


if __name__ == '__main__':
    app.run()
