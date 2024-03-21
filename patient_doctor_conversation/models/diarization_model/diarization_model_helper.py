import os
import contextlib
import wave

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

def get_audio_frame_rate(audio_file_dict,model):
  audioFrameRateDict = {}
  segments = []
  for filePath in audio_file_dict.keys():
    print(audio_file_dict[filePath])
    result = model.transcribe(filePath)
    result["segments"] = list(map(lambda d:{**d, filePath: audio_file_dict[filePath]},result["segments"]))
    segments.append(result["segments"])
    with contextlib.closing(wave.open(filePath,'r')) as f:
      audioFrameRateDict[filePath] = {'frames':f.getnframes(), 'rate':f.getframerate(), 'duration':f.getnframes() / float(f.getframerate())}
  return {'segments' : segments, 'audioFrameRateDict' : audioFrameRateDict}