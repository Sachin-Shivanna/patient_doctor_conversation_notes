from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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")
import torch
pipeline.to(torch.device("cuda"))

import whisper #pip install openai-whisper
from pyannote.audio import Audio #pip install pyannote.audio
from pyannote.audio import Model
import numpy as np

from diarization_model_helper import getAllFiles
from diarization_model_helper import get_segment_framerate
from diarization_model_helper import segment_embedding
from diarization_model_helper import assign_sepaker

pipeline

class audio_diarization:
    
    segments = []
    audioFrameRateDict = {}
    embeddingsDict = {}
    pathSegmentListDict={}

    filesDict = getAllFiles()

    model = whisper.load_model('base')

    segments,audioFrameRateDict = get_segment_framerate(filesDict,model)

    audio = Audio(sample_rate=16000, mono="downmix")

    embedding_model = Model.from_pretrained("pyannote/wespeaker-voxceleb-resnet34-LM")

    for segmentList in segments:
      segmentPath = ""
      embeddings = np.zeros(shape=(len(segmentList), 256))
      for i, segment in enumerate(segmentList):
        path,fileName = list(segment.items())[-1]
        duration = audioFrameRateDict[path]["duration"]
        segmentPath = path
        #print(embeddings)
        embeddings[i] = segment_embedding(segment,duration,path,embedding_model,audio)
      embeddings = np.nan_to_num(embeddings)
      embeddingsDict[segmentPath] = embeddings

    for segmentList in segments:
      for i, segment in enumerate(segmentList):
        pathSegmentListDict[list(segment)[-1]] = segmentList
    
    #print('length >>> ',len(embeddingsDict.keys()))
    pathSegmentListDict = assign_sepaker(embeddingsDict, pathSegmentListDict)

    print(pathSegmentListDict)