import sys
import shlex
import subprocess
import wave
from timeit import default_timer as timer
import numpy as np
from deepspeech import Model

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_ALPHA = 0.75

# The beta hyperparameter of the CTC decoder. Word insertion bonus.
LM_BETA = 1.85


# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9

MODEL = 'speech_analyzer/judgeyou_nlp/models/output_graph.pbmm'
ALPHABET = 'speech_analyzer/judgeyou_nlp/models/alphabet.txt'
LM = 'speech_analyzer/judgeyou_nlp/models/lm.binary'
TRIE = 'speech_analyzer/judgeyou_nlp/models/trie'

def convert_samplerate(audio_path):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path))
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

    return 16000, np.frombuffer(output, np.int16)

def write_text_to_file(text):
    file_obj = open(r'speech_analyzer/judgeyou_nlp/speech_to_text_result/text_result.txt', 'w+')
    file_obj.write(text)
    file_obj.close()


def extract_text(AUDIO):
    ds = Model(MODEL, N_FEATURES, N_CONTEXT, ALPHABET, BEAM_WIDTH)
    ds.enableDecoderWithLM(ALPHABET, LM, TRIE, LM_ALPHA, LM_BETA)

    fin = wave.open(AUDIO, 'rb')
    fs = fin.getframerate()
    if fs != 16000:
        print('Warning: original sample rate ({}) is different than 16kHz. Resampling might produce erratic speech recognition.'.format(fs), file=sys.stderr)
        fs, audio = convert_samplerate(AUDIO)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/16000)
    fin.close()

    print('Running inference.', file=sys.stderr)
    inference_start = timer()
    INFERENCE_RESULT= ds.stt(audio, fs)
    print(INFERENCE_RESULT)
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
    # write_text_to_file(INFERENCE_RESULT)
    return INFERENCE_RESULT