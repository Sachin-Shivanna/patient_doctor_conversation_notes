import os
import contextlib
import wave
import torch
from pyannote.core import Segment
from pyannote.audio import Audio
from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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")
pipeline.to(torch.device("cuda"))
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
embedding_model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cuda"))

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

def segment_embedding(segment,duration,path):
  audio = Audio(sample_rate=16000, mono="downmix")
  start = segment["start"]
  # Whisper overshoots the end timestamp in the last segment
  end = min(duration, segment["end"])
  clip = Segment(start, end)
  waveform, sample_rate = audio.crop(path, clip)
  print('waveform>>>>>>')
  print(waveform)
  print(waveform[None])
  #return embedding_model(waveform[None])