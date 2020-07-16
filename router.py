from flask import Flask, request
from requests import post, delete
import json
import os
import logging
from flask import send_file, send_from_directory

app = Flask(__name__)

@app.route("/accession_list", methods=['GET','POST'])
def accession_list():
    app.logger.info('Request received')
    directory = "/Users/xjw/Documents/tuixiang/jefferson_accession_list/router/"
    filename = "accession_list.txt"
    cmd = "rm -f " + directory + filename
    os.system(cmd)
    cmd = "ls " + directory + " -lt > " + filename
    os.system(cmd)
    # f=open(filename,'a')
    # for d in os.listdir(directory):
    #     app.logger.info(d)
    #     f.write(str(d))
    #     f.write('\n')
    return send_from_directory(directory, filename, as_attachment=False)
    

if __name__ == "__main__":
    app.debug = True
    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.logger.info("Initiated....")

    app.run(host="0.0.0.0", port=5002)
    # new_upload()