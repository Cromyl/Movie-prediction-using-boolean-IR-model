#!/bin/bash


LOGFILE="script_log.txt"
exec &> >(tee -a "$LOGFILE")  


pip install transformers pandas nltk textblob flask pyngrok regex tf-keras flask_cors

python server.py

npm install

npm start



echo "Script finished. Check $LOGFILE for any errors."