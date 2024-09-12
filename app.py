import flask
from flask import render_template, request, send_file, jsonify
import pprint
import openpyxl
import json
import os
import io
import pandas as pd
import paramiko
import pathlib
import pyreadstat
import shutil
import time
import warnings
import xport
import zipfile
import xpt_to_json
from xpt_to_json import *

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

warnings.filterwarnings("ignore")
app = flask.Flask(__name__)
app.secret_key = "Hello"


# global IE_base, domain, study_name, filetype, inputFile, path
@app.route("/")
def index():
    """Renders first page of application"""
    return render_template("JSON.html")


@app.route("/Navigation/<PageName>")
def Navigation(PageName):
    """Navigates between different pages of the application"""
    global currPage
    currPage = PageName
    return render_template(PageName + ".html")


@app.route("/generate_target_file/", methods=["GET", "POST"])
def generate_target_file():
    """
    Get the required inputs from the User (StudyName, Domain, FileType, Input File)
    Generate the target file based on User Input
    """
    # global IE_base, domain, study_name, filetype, inputFile, path
    if request.method == "POST":
        global filetype, inputFile, path, target, myfile, data, dict_, meta_dict
        filetype = request.form["filetype"]
        inputFile = request.files["sourcefile"]
        path = inputFile.filename
        inputFile.save(path)
        if filetype == "JSON":
            target, dict_, meta_dict = json_(path)
            message = "JSON is Generated successfully"

        if filetype == "NDJSON":
            target, dict_, meta_dict = ndjson_(path)
            message = "NDJSON is Generated successfully"

        print(target)
        # with open(target, "r") as myfile:
        #     data = myfile.read()
        # JSON = data.to_html(classes='table table-stripped')
    return render_template("JSON.html", message=message, targetdataset=target)


@app.route("/generate_target_file/JSONfile.html")
def JSONfile():
    data_d = {key: dict_[key] for key in ["rows"]}
    # data_f = pprint.pformat(dict_)
    return render_template("JSONfile.html", title="JSON file", jsonfile=data_d)


@app.route("/generate_target_file/JSONMeta.html")
def JSONMeta():
    data_m = {
        key: dict_[key]
        for key in [
            "creationDateTime",
            "datasetJSONVersion",
            "fileOID",
            "name",
            "label",
            "originator",
            "sourceSystem",
            "sourceSystemVersion",
            "records",
            "columns",
            "metaDataRef",
            "itemGroupOID",
        ]
    }
    return render_template("JSONMeta.html", title="JSON file", jsonfile=data_m)


@app.route("/download_file/", methods=["GET", "POST"])
def download_file():
    """
    Download the Result files in XPT / JSON format
    """
    if request.method == "POST":
        # filetype = request.form.getlist('target_filetype')
        # filetype = request.form['target_filetype']
        return send_file(target, as_attachment=True)
        # elif i == 'ndjson':
        #     return send_file(filepath_json, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
