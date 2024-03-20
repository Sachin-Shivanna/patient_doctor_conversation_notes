import os
import json
import numpy as np
import whisper
import datetime
import subprocess
import torch
import wave
import contextlib

import pyannote.audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
embedding_model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cuda"))
from pyannote.audio import Audio
from pyannote.core import Segment

from sklearn.cluster import AgglomerativeClustering