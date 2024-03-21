import json
import numpy as np
import whisper #pip install git+https://github.com/openai/whisper.git 
import datetime
import subprocess
import torch
import wave

import pyannote.audio #pip install pyannote.audio==2.1.1 | pip install speechbrain | pip install git+https://github.com/speechbrain/speechbrain.git@develop
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
embedding_model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cuda"))
from pyannote.audio import Audio
from pyannote.core import Segment

from sklearn.cluster import AgglomerativeClustering

from diarization_model_helper import getAllFiles
from diarization_model_helper import get_audio_frame_rate

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

segments_frame_rate_dict = get_audio_frame_rate(filesDict)

audioFrameRateDict = segments_frame_rate_dict['audioFrameRateDict']

segments = segments_frame_rate_dict['segments']

print(audioFrameRateDict)
print(segments)