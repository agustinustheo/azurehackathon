## Dependencies
ffmpeg  
youtube-dl  
deepspeech  

### Command to run deepspeech
deepspeech --model models/output_graph.pbmm --alphabet models/alphabet.txt --lm models/lm.binary --trie models/trie --audio my_audio_file.wav
