import json
import numpy as np
import whisper #pip install git+https://github.com/openai/whisper.git 
import datetime
import subprocess

import pyannote.audio #pip install pyannote.audio==2.1.1 | pip install speechbrain | pip install git+https://github.com/speechbrain/speechbrain.git@develop



from sklearn.cluster import AgglomerativeClustering

from diarization_model_helper import getAllFiles
from diarization_model_helper import get_audio_frame_rate
from diarization_model_helper import segment_embedding

segments = []
audioFrameRateDict = {}
num_speakers = 2 #@param {type:"integer"}
language = 'English' #@param ['any', 'English']
model_size = 'large' #@param ['tiny', 'base', 'small', 'medium', 'large']
model_name = model_size
if language == 'English' and model_size != 'large':
  model_name += '.en'

filesDict = getAllFiles()

model = whisper.load_model(model_size)

segments_frame_rate_dict = get_audio_frame_rate(filesDict, model)

audioFrameRateDict = segments_frame_rate_dict['audioFrameRateDict']

segments = segments_frame_rate_dict['segments']

embeddingsDict = {}
for segmentList in segments:
  segmentPath = ""
  embeddings = np.zeros(shape=(len(segmentList), 192))
  for i, segment in enumerate(segmentList):
    path,fileName = list(segment.items())[-1]
    duration = audioFrameRateDict[path]["duration"]
    segmentPath = path
    print(path)
    print(embeddings)
    embeddings[i] = segment_embedding(segment,duration,path)
  embeddings = np.nan_to_num(embeddings)
  embeddingsDict[segmentPath] = embeddings

print(audioFrameRateDict)
print(segments)