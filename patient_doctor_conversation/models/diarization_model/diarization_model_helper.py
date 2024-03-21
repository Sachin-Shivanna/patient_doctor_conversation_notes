import os
def getAllFiles():
    audioFilesDict = {}
    directory = '/root/patient_doctor_conversation_notes/audio_files'
    for root, _, files in os.walk(directory):
          for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            audioFilesDict[file_path] = file
    print(audioFilesDict)
    return audioFilesDict