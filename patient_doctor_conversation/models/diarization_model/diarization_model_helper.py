import os
import contextlib
import wave
from pyannote.core import Segment
from pyannote.audio import Inference
from sklearn.cluster import AgglomerativeClustering

'''def getAllFiles():
    audioFilesDict = {}
    directory = 'audio_files'
    for root, _, files in os.walk(directory):
          for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            audioFilesDict[file_path] = file

    return audioFilesDict'''

def get_segment_framerate(filesDict, model):
    segments = []
    audioFrameRateDict = {}
    for filePath in filesDict.keys():
      print(filesDict[filePath])
      result = model.transcribe(filePath)
      result["segments"] = list(map(lambda d:{**d, filePath: filesDict[filePath]},result["segments"]))
      segments.append(result["segments"])
      with contextlib.closing(wave.open(filePath,'r')) as f:
        audioFrameRateDict[filePath] = {'frames':f.getnframes(), 'rate':f.getframerate(), 'duration':f.getnframes() / float(f.getframerate())}
    return segments, audioFrameRateDict

def segment_embedding(segment,duration,path,embedding_model,audio):
  start = segment["start"]
  # Whisper overshoots the end timestamp in the last segment
  end = min(duration, segment["end"])
  clip = Segment(start, end)
  waveform, sample_rate = audio.crop(path, clip)
  inference = Inference(embedding_model, window="whole")
  excerpt = Segment(start, end)
  return inference.crop(path, excerpt)

def assign_sepaker(embeddingsDict, pathSegmentListDict):
   for path in embeddingsDict.keys():
    print("*"*20)
    print(len(embeddingsDict[path]))
    if len(embeddingsDict[path]) == 1:
      for i in range(len(pathSegmentListDict[path])):
        print(path)
        last_underscore_index = pathSegmentListDict[path][i][path].rfind("_")
        dot_index = pathSegmentListDict[path][i][path].rfind(".")
        pathSegmentListDict[path][i]["speaker"] = 'SPEAKER 1'
        pathSegmentListDict[path][i]["dateTime"] = pathSegmentListDict[path][i][path][last_underscore_index + 1:dot_index]
    else:
      clustering = AgglomerativeClustering(2).fit(embeddingsDict[path])
      labels = clustering.labels_
      print(labels)
      for i in range(len(pathSegmentListDict[path])):
        last_underscore_index = pathSegmentListDict[path][i][path].rfind("_")
        dot_index = pathSegmentListDict[path][i][path].rfind(".")
        pathSegmentListDict[path][i]["speaker"] = 'SPEAKER ' + str(labels[i])
        pathSegmentListDict[path][i]["dateTime"] = pathSegmentListDict[path][i][path][last_underscore_index + 1:dot_index]
   return pathSegmentListDict