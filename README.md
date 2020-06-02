# video quality extractor

This repo contains the automations for the following workflow:
1. Video added to the input folder.
2. FFprobe analyze the video and create csv file.
3. Python script triggered and summerizes the csv file.
4. The script sends the data as a log to elasticsearch.

## Prerequisites

- **FFprobe** - The program which does all the magic. Since some metrics added only in recent versions of ffmpeg, we recommend to use version >= 4.2.1. to install it with static complied binary on linux run the following command:
```sh
wget -q https://www.johnvansickle.com/ffmpeg/old-releases/ffmpeg-4.2.1-amd64-static.tar.xz \
  && tar xJf /tmp/ffmpeg-4.2.1-amd64-static.tar.xz -C /tmp \
  && mv /tmp/ffmpeg-4.2.1-amd64-static/ffprobe /usr/local/bin/ \
  && rm -rf /tmp/ffmpeg*
```

- **python** - tested on python 3.7, installtion via anaconda is recommended. (requirements.txt file will be added)

## files
- **main.py** - Contains the logic to warp ffprobe and triggers reporting. Responsible for exception handling and for shipping the reports/alerts. This script intended to be stable and generic enought to handle varity of configurations.

- **config.ini** - Contains parameters that may change from **one host to another**.
- **alerts.py** - Contains constants and logic to handle different configurations for ffprobe. It also contains the definition of the alerts. This script may change from version to version in the early stages of the deployment.
