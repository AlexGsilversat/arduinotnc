#!/bin/env python3

# importing the required libraries
import os, os.path, sys, glob, time
from hashlib import md5
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename

# initialising the flask app
app = Flask("minifs")

# Creating the upload folder
upload_folder = "uploads/"
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.route('/upload', methods = ['POST'])
def upload():
   if request.method == 'POST': # check if the method is post
      f = request.files['file'] # get the file from the files object
      if f.filename == "" or secure_filename(f.filename) == "":
          return "Bad filename\n",400
      # All files are cleaned up, we retain the filename
      # All files are placed in a time-stamped folder
      sfilename = os.path.split(secure_filename(f.filename))[1]
      dtfolder = time.strftime("%Y%m%d-%H%M")
      if not os.path.exists(os.path.join("uploads/",dtfolder)):
          os.makedirs(os.path.join("uploads/",dtfolder))
      f.save(os.path.join("uploads",dtfolder,secure_filename(sfilename))) # this will secure the file
      return 'Success\n', 200 # Display thsi message after uploading
   return 'Bad method\n', 400

@app.route('/download')
def download():
    filename = os.path.join('downloads',request.args['file'])
    if os.path.exists(filename):
        return send_file(os.path.join('downloads',request.args['file']), as_attachment=True)
    return "No such file\n", 400

@app.route('/list')
def list():
    pattern = request.args.get('pattern','*')
    filelist = []
    for f in glob.glob('downloads/'+pattern):
        filename = f.split('/',1)[1]
        size = str(os.path.getsize(f))
        md5hash = md5(open(f).read()).hexdigest().lower()
        filelist.append("\t".join([filename,size,md5hash]))
    filelist.sort()
    return "\n".join(filelist)+'\n'

@app.route('/tweet')
def tweet():
    from twython import Twython
    from datetime import datetime
    print (datetime.now())

    consumer_key        = 'n6yc49v1pHc8w9bW0kKv4wNUd'
    consumer_secret     = 'd3L4lVQep8MApUptGb59PGNPpHBBpK70I3Cr39C0jDjztASJlW'
    access_token        = '1313567351762280451-nIfagojWjM6LzWGGCOOIVu8EN3FZkK'
    access_token_secret = 'jGwWAICERyJsowpe6F5NgoOxHFl1jvwDS9iM7HeenrLfS'
    twitter = Twython(
        consumer_key,        
        consumer_secret,     
        access_token,        
        access_token_secret 
    )


    message = [datetime.now()]
    if f.filename == "" or secure_filename(f.filename) == "":
          return "Bad filename\n",400
    f = request.files['file']
    photo = open(f, 'rb')

    response = twitter.upload_media(media=photo)
    twitter.update_status(status=message, media_ids=[response['media_id']])
    print("Tweeted: %s with image %s" % (message, myimage))
    return "Successfull tweet\n",200

if __name__ == '__main__':
   # app.run(host='127.0.0.1',port=5001) # running the flask app
   app.run(host='192.168.100.101',port=5001) # running the flask app

 
