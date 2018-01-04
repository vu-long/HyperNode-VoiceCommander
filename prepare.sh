export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt update
sudo apt install -y python3 git openssl vim gcc libasound-dev python3-pyaudio swig3.0 python-pyaudio python3-pyaudio sox libatlas-base-dev swig alsa-utils mpg321 lame python3-pip vlc-nox google-cloud-sdk google-cloud-sdk-app-engine-python

sudo pip3 install --upgrade gTTS apiai pipenv google-api-python-client pyaudio google-api-python-client google google.cloud pika json-encoder paho-mqtt pyaudio youtube-dl pafy

git clone --recursive git@gitlab.com:hyperbrain/firmware/HyperNode-VoiceCommander.git
git submodule update --init --recursive
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config --global user.email "pi@raspberry"
git config --global user.name "vulong"

Change your ~/.asoundrc file to:

pcm.!default {
  type asym
   playback.pcm {
     type plug
     slave.pcm "hw:0,0"
   }
   capture.pcm {
     type plug
     slave.pcm "hw:1,0"
   }
}

sox -t wav YOUR_ORIGINAL.wav -t wav -r 16000 -b 16 -e signed-integer -c 1 YOUR_PROCESSED.wav