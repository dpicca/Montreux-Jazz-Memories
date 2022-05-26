from flask import *
from pathlib import Path
from werkzeug.utils import secure_filename
import asyncio
import datetime
import json
import mysql.connector
import os
import transcription
import interaction


JSON_EXTENSION = {'json'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DataBasic$'
app.config['UPLOAD_FOLDER'] = './static/uploads'


@app.route('/transcript', methods=['GET', 'POST'])
def transcript():
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

        # Makes Flask requests to access form inputs
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
        # Opens and reads the json file to extract useful information
        # Audio duration
        read_minfo = json.loads(minfo.read())
        minfo_duration = read_minfo['media']['track'][0]['Duration']
        converted_duration = str(datetime.timedelta(seconds=float(minfo_duration)))
        duration = converted_duration
        # Number of recording channels
        minfo_channels = read_minfo['media']['track'][1]['Channels']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('Missing file')
            return redirect(request.url)
        # "en_US" is supposed to be replaced by a language selection on the web page
        filename = secure_filename(file.filename)
        results = asyncio.run(transcription.speech_to_text_google(file, language, filename, minfo_channels))
        if file and interaction.allowed_file(file.filename):
            minfo_name = secure_filename(minfo.filename)
            Path('./static/uploads/' + filename.split('.')[0]).mkdir(parents=True, exist_ok=True)
            app.config['FOLDER_PATH'] = Path('./static/uploads/' + filename.split('.')[0]).as_posix()
            file.stream.seek(0)
            file.save(os.path.join(app.config['FOLDER_PATH'], filename))
            minfo.stream.seek(0)
            minfo.save(os.path.join(app.config['FOLDER_PATH'], minfo_name))
            filepath = app.config['FOLDER_PATH'] + '/' + filename
            jsonpath = app.config['FOLDER_PATH'] + '/' + minfo_name

            interaction.insert_interview(results, results, filepath)
            interaction.insert_metadata(fname_interviewee, lname_interviewee, gender_interviewee, fname_interviewer,
                            lname_interviewer, gender_interviewer, location, date, context, filename, duration,
                            file_format, language, jsonpath)

    return render_template('transcript.html')


@app.route('/', methods=['GET', 'POST'])
def search():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port='8889',
                                             user='root',
                                             password='root',
                                             database='mydb')

        cursor = connection.cursor(buffered=True)
        if request.method == "POST":
            interview = request.form['interview']
            # Search name of file
            cursor.execute("SELECT first_name_interviewee, last_name_interviewee, first_name_interviewer,"
                           " last_name_interviewer, descriptive_metadata.date, location, id from"
                           " descriptive_metadata where descriptive_metadata.first_name_interviewee like %s or"
                           " descriptive_metadata.first_name_interviewer like %s or"
                           " descriptive_metadata.last_name_interviewer like %s or"
                           " descriptive_metadata.last_name_interviewee like %s or"
                           " descriptive_metadata.location like %s",
                           (interview, interview, interview, interview, interview))
            # For loop to get values and display them
            connection.commit()
            fetched_data = cursor.fetchall()
            results = len(fetched_data)
            data = []
            id_list = []
            i = 0
            while i < results:
                id = fetched_data[i][6]
                result_dict = {
                    'Interviewee': str(fetched_data[i][0]) + ' ' + str(fetched_data[i][1]),
                    'Interviewer': str(fetched_data[i][2]) + ' ' + str(fetched_data[i][3]),
                    'Date': fetched_data[i][4],
                    'Location': fetched_data[i][5],
                }
                id_list.append(id)
                data.append(result_dict)
                i += 1

            return render_template('search.html', data=zip(data, id_list), results=results)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template('search.html')


@app.route('/display-id=<id>')
def display(id):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port='8889',
                                             user='root',
                                             password='root',
                                             database='mydb')

        cursor = connection.cursor(buffered=True)
        # Retrieve text from database
        cursor.execute("SELECT text from interview")
        connection.commit()
        data = cursor.fetchall()
        cursor.execute("SELECT audio from interview")
        connection.commit()
        audio = cursor.fetchall()

        return render_template('display.html', data=str(data[int(id)-1])[2:-3], id=id, audio=str(audio[int(id)-1][0])[2:-1])

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template('display.html')


@app.route('/edit-id=<id>', methods=['GET', 'POST'])
def edit_page(id):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port='8889',
                                             user='root',
                                             password='root',
                                             database='mydb')

        cursor = connection.cursor(buffered=True)
        # Retrieve text from database
        cursor.execute("SELECT text from interview")
        connection.commit()
        data = cursor.fetchall()
        if request.method == 'POST':
            text = request.form['text_edit']
            interaction.edit_interview(text, id)
        return render_template('edit.html', data=str(data[int(id)-1])[2:-3])

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template('edit.html')


if __name__ == '__main__':
    app.run()
