#!/bin/bash
# ----- AUDIO EXTRACTOR -------
# Dependencies for youtube-dl download video from youtube and extract audio
sudo apt-get install ffmpeg

# ------ DEEPSPEECH -------------
# Git LFS needed for deepspeech development
# sudo add-apt-repository ppa:git-core/ppa
# curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
# sudo apt-get install git-lfs
# git lfs install
# Get Dependencies
sudo apt install libsox3 libstdc++6 libgomp1 libpthread-stubs0-dev sox
# get deepspeech pretrained model
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.4.1/deepspeech-0.4.1-models.tar.gz 
tar xvfz deepspeech-0.4.1-models.tar.gz