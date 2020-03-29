#!/usr/bin/env bash

source venv/bin/activate
pip3 install flask
pip3 install pyresparser
python3 -m spacy download en_core_web_sm
python3 -m nltk.downloader words
python3 download_stopwords.py
cp resume_parser.py venv/lib/python3.6/site-packages/pyresparser/