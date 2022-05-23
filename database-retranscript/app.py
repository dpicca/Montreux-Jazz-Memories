from flask import *
import os
from werkzeug.utils import secure_filename
import mysql.connector
from google.cloud import speech_v1
from google.cloud import storage
import asyncio
import datetime
from pathlib import Path
import json


AUDIO_EXTENSIONS = {'wav'}
JSON_EXTENSION = {'json'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DataBasic$'
app.config['UPLOAD_FOLDER'] = './uploads'


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
async def speech_to_text_google(file, language, filename):
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
        audio_channel_count=1,
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

    # TODO: return transcription as text
    return transcription


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in AUDIO_EXTENSIONS


def insert_interview(text, transcription, audio):
    print("Inserting Audio file and its transcription to interview table")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port='8889',
                                             user='root',
                                             password='root',
                                             database='mydb')

        cursor = connection.cursor()
        sql_insert_interview = """ INSERT INTO interview (text, transcription, audio) VALUES (%s, %s, %s)"""
        insert_interview_data = (text, transcription, audio)
        result_interview = cursor.execute(sql_insert_interview, insert_interview_data)

        connection.commit()
        print("Transcription and audio file successfully uploaded to database", result_interview)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_metadata(fname_interviewee,lname_interviewee, gender_interviewee, fname_interviewer,lname_interviewer,
                    gender_interviewer, location, date, context, file_name, audio_length, file_format, language,
                    mediainfo):
    print("Inserting Meta Data")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port='8889',
                                             user='root',
                                             password='root',
                                             database='mydb')

        cursor = connection.cursor()

        sql_insert_descriptive = """ INSERT INTO descriptive_metadata (id, first_name_interviewee,
         last_name_interviewee, gender_interviewee, first_name_interviewer, last_name_interviewer, gender_interviewer,
         location, date, context) VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        insert_descriptive_data = (fname_interviewee, lname_interviewee, gender_interviewee, fname_interviewer,
                                   lname_interviewer, gender_interviewer, location, date, context)
        result_descriptive = cursor.execute(sql_insert_descriptive, insert_descriptive_data)

        sql_insert_technical = """INSERT INTO technical_metadata (id, file_name, file_length, format, language,
         media_info) VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s)"""
        insert_technical_data = (file_name, audio_length, file_format, language, mediainfo)
        result_technical = cursor.execute(sql_insert_technical, insert_technical_data)

        connection.commit()
        print("Transcription and audio file successfully uploaded to database",result_descriptive, result_technical)

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
        if 'audio' not in request.files:
            print('missing audio file')
            flash('No file part')
            return redirect(request.url)

        if 'json' not in request.files:
            print('missing json file')
            flash('No file part')
            return redirect(request.url)

        file = request.files['audio']
        minfo = request.files['json']
        language = request.form['language']
        fname_interviewee = request.form['fn_interviewee']
        lname_interviewee = request.form['ln_interviewee']
        gender_interviewee = request.form['gender_interviewee']
        fname_interviewer = request.form['fn_interviewer']
        lname_interviewer = request.form['ln_interviewer']
        gender_interviewer = request.form['gender_interviewer']
        location = request.form['location']
        form_date = request.form.get('Idate')
        date = datetime.datetime.strptime(form_date, '%Y-%m-%d')
        context = request.form['context']
        file_format = file.filename.split('.')[1]
        # get audio file duration from json file
        duration = 2.9

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('Missing file')
            return redirect(request.url)
        # "en_US" is supposed to be replaced by a language selection on the web page
        filename = secure_filename(file.filename)
        results = asyncio.run(speech_to_text_google(file, language, filename))
        if file and allowed_file(file.filename):
            minfo_name = secure_filename(minfo.filename)
            Path('./uploads/' + filename.split('.')[0]).mkdir(parents=True, exist_ok=True)
            app.config['FOLDER_PATH'] = Path('./uploads/' + filename.split('.')[0]).as_posix()
            file.stream.seek(0)
            file.save(os.path.join(app.config['FOLDER_PATH'], filename))
            minfo.stream.seek(0)
            minfo.save(os.path.join(app.config['FOLDER_PATH'], minfo_name))
            filepath = app.config['FOLDER_PATH'] + '/' + filename
            jsonpath = app.config['FOLDER_PATH'] + '/' + minfo_name

            insert_interview(results, results, filepath)
            insert_metadata(fname_interviewee, lname_interviewee, gender_interviewee, fname_interviewer,
                            lname_interviewer, gender_interviewer, location, date, context, filename, duration,
                            file_format, language, jsonpath)

    return render_template('upload_revamp.html')


@app.route('/transcriptions/<date>/<name>', methods=['GET', 'POST'])
def update_text(interview_id):
    def select_interview():
        print("Retrieving interview ID")
        interview_name = request.form('interview_search')
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 port='8889',
                                                 user='root',
                                                 password='root',
                                                 database='mydb')

            cursor = connection.cursor()
            sql_select_interview = """SELECT MAX(id) FROM interview"""
            selected_interview = cursor.execute(sql_select_interview)

            connection.commit()
            return selected_interview

        except mysql.connector.Error as error:
            print("Failed inserting BLOB data into MySQL table {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    interview_id = request.args.get('id')
    return render_template('transcription.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port='8889',
                                             user='root',
                                             password='root',
                                             database='mydb')

        cursor = connection.cursor(buffered=True)
        if request.method == "POST":
            research = request.form['name']
            # search name of file
            # TODO : récupérer infos dans plusieurs tables (transcription, nom etc...)
            cursor.execute("SELECT first_name_interviewee, last_name_interviewee, first_name_interviewer, last_name_interviewer, date, location, context, audio, transcription from descriptive_metadata, interview where interview.id = descriptive_metadata.id group by descriptive_metadata.id")
            # boucle for pour récupérer les valeurs et les afficher
            connection.commit()
            data = cursor.fetchall()
            # all in the search box will return all the tuples
            if len(data) == 0 and research == 'all':
                cursor.execute("SELECT first_name_interviewee, last_name_interviewee, first_name_interviewer, last_name_interviewer, date, location, context, audio, transcription from descriptive_metadata, interview where interview.id = descriptive_metadata.id group by descriptive_metadata.id")
                connection.commit()
                data = cursor.fetchall()
            return render_template('search.html', data=data)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template('search.html')


if __name__ == '__main__':
    app.run()
