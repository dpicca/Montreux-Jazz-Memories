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
            insertBLOB('transcript', binary_audio)

    return render_template('upload_revamp.html')


if __name__ == '__main__':
    app.run()
