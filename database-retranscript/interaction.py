import mysql.connector

AUDIO_EXTENSIONS = {'wav'}


def allowed_file(filename):
    """Sets the only accepted extension as .wav"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in AUDIO_EXTENSIONS


def edit_interview(text, id):
    """Edits the text saved in the database"""
    print("Inserting new transcription to database")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port='8889',
                                             user='root',
                                             password='root',
                                             database='mydb')

        cursor = connection.cursor()
        sql_edit_interview = """UPDATE interview SET text = %s WHERE id = %s"""
        insert_edited_data = (text, id)
        result_edit = cursor.execute(sql_edit_interview, insert_edited_data)

        connection.commit()
        print("Edit successfully uploaded to database", result_edit)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_interview(text, transcription, audio):
    """Insert a new interview in the database"""
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


def insert_metadata(fname_interviewee, lname_interviewee, gender_interviewee, fname_interviewer,lname_interviewer,
                    gender_interviewer, location, date, context, file_name, audio_length, file_format, language,
                    mediainfo):
    """Inserts metadata linked to the interview"""
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
