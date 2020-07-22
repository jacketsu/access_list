from flask import Flask, request
from requests import post, delete
import json
import os
import time
import logging
from flask import send_file, send_from_directory

app = Flask(__name__)

@app.route("/accession_list", methods=['GET','POST'])
def accession_list():
    app.logger.info('Request received')
    directory = "/media/tx-deepocean/Data/TMP/"
    filename = "accession_list.txt"
    cmd = "rm -f " + directory + filename
    os.system(cmd)
    cmd = "ls " + directory + " -lt > " + filename
    download_directory = "/media/tx-deepocean/Data/accession_list_server/access_list"
    os.system(cmd)
    app.logger.info('created a file')
    # f=open(filename,'a')
    # for d in os.listdir(directory):
    #     app.logger.info(d)
    #     f.write(str(d))
    #     f.write('\n')
    return send_from_directory(download_directory, filename, as_attachment=False)

@app.route("/accession_list_v2", methods=['GET','POST'])
def accession_list_v2():
    app.logger.info('v2 Request received')
    directory = "/media/tx-deepocean/Data/TMP"
    filename = "accession_list_v2.txt"
    with open(filename, "w") as file:
        for pid in os.listdir(directory):
            if "." in pid:
                continue
            pid_f = os.listdir("/".join([directory, pid]))
            path = "/".join([directory, pid]) 
            while len(pid_f) > 0 and os.path.isdir("/".join([path, pid_f[0]])):
                path = "/".join([path, pid_f[0]])
                pid_f = os.listdir(path)
            count = len(pid_f)
            mtime = time.ctime(os.path.getmtime("/".join([directory, pid])))
            file.write(str(pid) + "       " + str(mtime) + "     " + str(count))

    download_directory = "/media/tx-deepocean/Data/accession_list_server/access_list"
    app.logger.info('created a v2 file')
    # f=open(filename,'a')
    # for d in os.listdir(directory):
    #     app.logger.info(d)
    #     f.write(str(d))
    #     f.write('\n')
    return send_from_directory(download_directory, filename, as_attachment=False)
    

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
