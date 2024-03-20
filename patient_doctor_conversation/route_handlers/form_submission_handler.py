from flask import request,redirect, url_for
import os
from datetime import date
from datetime import datetime
from pydub import AudioSegment 


"""
A function that handles form submission, processes audio files, and redirects to the main index page.
"""
def handle_form_submission():
    input_file = "hello.mp3"

    if 'conversation_audio' in request.files:
        input_file = request.files['conversation_audio']
        

    patient_id = request.form['patient_id']
    account_id = request.form['account_id']
    file_dir = 'audio_files' + "/" + account_id + "/" + patient_id + "/" + date.today().strftime("%Y-%m-%d")
    file_name = datetime.now().strftime("%H:%M:%S") + ".wav"
    output_path = os.path.join(file_dir, file_name)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

   
    sound = AudioSegment.from_mp3(input_file) 
    sound.export(output_path, format="wav")

    
    return redirect(url_for('main.index'))