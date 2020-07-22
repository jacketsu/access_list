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
    folders = []
    for pid in os.listdir(directory):
        if "." in pid:
            continue
        path = "/".join([directory, pid])
        pid_f = os.listdir(path)
        path = "/".join([path, pid_f[0]])
        for subf in os.listdir(path):
            fname = "/".join([pid, subf])
            count = len(os.listdir("/".join([path, subf])))
            # mtime = time.ctime(os.path.getmtime("/".join([directory, pid])))
            mtime = os.path.getmtime("/".join([directory, pid]))
            folders.append([fname, mtime, count])
    sorted(folders, key=lambda f:f[1], reversed=True)

    with open(filename, "w") as file:
        for r in folders:
            file.write(str(r[0]) + " " * 30 + str(time.ctime(r[1])) + " " * 30 + str(r[2]) + "\n")

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
