import IPython
import numpy
import json 
import essentia
import essentia.standard as es
from essentia.standard import *
from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt

def essentia_midi(file): 
      pool = essentia.Pool(); 

      # Compute all features, aggregate only 'mean' and 'stdev' statistics for all low-level, rhythm and tonal frame features
      features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                                rhythmStats=['mean', 'stdev'],
                                                tonalStats=['mean', 'stdev'])(file)

      # You can then access particular values in the pools:
      print("Filename:", features['metadata.tags.file_name'])
      print("-"*80)
      print("Replay gain:", features['metadata.audio_properties.replay_gain'])
      print("EBU128 integrated loudness:", features['lowlevel.loudness_ebu128.integrated'])
      print("EBU128 loudness range:", features['lowlevel.loudness_ebu128.loudness_range'])
      print("-"*80)
      print("MFCC mean:", features['lowlevel.mfcc.mean'])
      print("-"*80)
      print("BPM:", features['rhythm.bpm'])
      print("Beat positions (sec.)", features['rhythm.beats_position'])
      print("-"*80)
      print("Key/scale estimation (using a profile specifically suited for electronic music):",
            features['tonal.key_edma.key'], features['tonal.key_edma.scale'])

      # BPM Detection

      # Loading audio file
      audio = MonoLoader(filename=file)()

      # # Compute beat positions and BPM
      rhythm_extractor = RhythmExtractor2013(method="multifeature")
      bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

      beat_volume_extractor = BeatsLoudness(beats=beats)
      beats_loudness, beats_loudness_band_ratio = beat_volume_extractor(audio)

      # Danceability Detection
      danceability_extractor = Danceability()
      danceability, dfa = danceability_extractor(audio)

      # Melody Detection
      # Load audio file; it is recommended to apply equal-loudness filter for PredominantPitchMelodia
      loader = EqloudLoader(filename=file, sampleRate=44100)
      audio = loader()
      print("Duration of the audio sample [sec]:")
      print(len(audio)/44100.0)

      pitch_extractor = PredominantPitchMelodia(frameSize=2048, hopSize=1024)
      pitch_values, pitch_confidence = pitch_extractor(audio)

      midi_extractor = PitchContourSegmentation(hopSize=1024)
      onset, duration, midi_pitch = midi_extractor(pitch_values, audio)

      # Pitch is estimated on frames. Compute frame time positions
      pitch_times = numpy.linspace(0.0,len(audio)/44100.0,len(pitch_values))

      #Storing in Pool
      pool.add('MIDIonset', onset)
      pool.add('MIDIduration', duration)
      pool.add('MIDIpitch', midi_pitch)
      pool.add('pitch', pitch_values)
      pool.add('danceability', danceability)
      pool.add('beat-loudness', beats_loudness)
      pool.add('beats', beats)
      pool.add('bpm', bpm)
      
      output = YamlOutput(filename = './analyzer/output.json',format='json',indent=4,writeVersion=False) # use "format = 'json'" for JSON output
      output(pool)