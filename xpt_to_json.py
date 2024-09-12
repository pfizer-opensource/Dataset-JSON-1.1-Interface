"""
File: adam_xpt_json.py
Authors: Aishwarya L R, Deepika S, Natarajan Vijaikumar, Sai Pooja V R
Date: 2024-01-29
Description: A Python script to convert XPT format to JSON format and JSON back to XPT.
"""
# add versions

import pandas as pd  #
import json  #
import ndjson
import pyreadstat as prs  #
import datetime  #
from datetime import datetime, timedelta
import os
import yaml


def read_meta(xpt_meta):
    # read the attributes from the meta data of xpt
    attributes = dict(xpt_meta.__dict__)
    # print(xpt_meta.__dict__)
    attributes["column_names"] = xpt_meta.__dict__["column_names"]
    attributes["column_labels"] = xpt_meta.__dict__["column_labels"]
    attributes["table_name"] = xpt_meta.__dict__["table_name"]
    attributes["file_label"] = xpt_meta.__dict__["file_label"]
    attributes["Types"] = xpt_meta.__dict__["readstat_variable_types"]
    attributes["length"] = xpt_meta.__dict__["variable_storage_width"]
    attributes["format"] = xpt_meta.__dict__["original_variable_types"]
    # print(attributes)
    return attributes


def replace_missing_with_null(data):
    null = None
    # Iterate over each row in the data
    for row in data:
        # Iterate over each element in the row
        for i in range(len(row)):
            # Replace empty strings and 'nan' with None
            if row[i] == "" or row[i] == "nan" or row[i] == "NaT" or row[i] == "None":
                row[i] = null
    return data


def xpt_to_json(attributes, path, filename, df_xpt):
    meta_dict, decimal_col = [], []
    final_dict = {
        "creationDateTime": str(datetime.now()),
        "datasetJSONVersion": "1.1.0",
        "fileOID": "www.cdisc.org/StudyMSGv2/1/Define-XML_2.1.0/",
        "name": attributes["table_name"],
        "label": attributes["file_label"],
        # "asOfDateTime": "<need to check>",
        "originator": "<need to check>",
        "sourceSystem": "<need to check>",
        "sourceSystemVersion": "<need to check>",
        "records": attributes["number_rows"],
    }  # df_xpt.shape[0]}
    # metadata creation for json
    # temp={'table_name':xpt_meta.__dict__['table_name'],'file_label':xpt_meta.__dict__['file_label']} #8888888888888888888
    temp = {
        "itemOID": "ITEMGROUPDATASEQ",
        "name": "ITEMGROUPDATASEQ",
        "label": "Record Identifier",
        "dataType": "integer",
    }
    meta_dict.append(temp)
    datetime_columns = df_xpt.select_dtypes("datetime64[ns]").columns.tolist()

    for column in df_xpt.columns:
        if df_xpt[column].dtype == "float64":
            if any(round(df_xpt[column]) != df_xpt[column]) == True:
                df_xpt[column] = df_xpt[column].astype(str)
                decimal_col.append(column)

    for i in datetime_columns:
        df_xpt[i] = df_xpt[i].astype(str)
    df_xpt = df_xpt.fillna("")
    records_list = df_xpt.values.tolist()
    for i in attributes["column_names_to_labels"]:
        temp = {}
        temp["itemOID"] = "IT." + attributes["table_name"] + "." + i
        temp["name"] = i
        temp["label"] = attributes["column_names_to_labels"][i]
        temp["dataType"] = attributes["readstat_variable_types"][i]

        if i in datetime_columns:
            temp["dataType"] = "datetime"
            temp["targetDataType"] = "integer"
        if i in decimal_col:
            length_ = int(df_xpt[i].str.len().max())
            temp["dataType"] = "string"
            temp["targetDataType"] = "decimal"
            temp["length"] = length_
        else:
            temp["length"] = attributes["variable_storage_width"][i]
        if attributes["format"][i] != "NULL":
            temp["format"] = attributes["format"][i]
        meta_dict.append(temp)

    # final dictionary with data and metadata
    final_dict["columns"] = meta_dict
    final_dict["rows"] = replace_missing_with_null(records_list)
    final_dict[
        "metaDataRef"
    ] = "https://metadata.location.org/TDF_ADaM_ADaMIG11/define.xml"
    final_dict["itemGroupOID"] = "IG." + attributes["table_name"]

    # truncate white spaces
    final_json = json.dumps(final_dict, separators=(",", ":"),indent = 4)

    # final json creation
    with open("{}".format(filename) + ".json", "w", encoding="iso-8859-1") as f:
        f.write(final_json)

    return final_dict, meta_dict


def json_(path):
    df_xpt, xpt_meta = prs.read_xport(
        r"{}".format(path), dates_as_pandas_datetime=True, encoding="iso-8859-1"
    )
    filename = os.path.basename(r"{}".format(path)).split(".")[0]
    print(filename)
    path_to_store = os.path.dirname(r"{}".format(path))
    print(path_to_store)
    attributes = read_meta(xpt_meta)
    final_dict, meta_dict = xpt_to_json(
        attributes, path_to_store, filename, df_xpt
    )
    return "{}".format(filename) + ".json", final_dict, meta_dict


def ndjson_(path):
    # ndjson file creation from dictionary
    df_xpt, xpt_meta = prs.read_xport(
        r"{}".format(path), dates_as_pandas_datetime=True, encoding="iso-8859-1"
    )
    filename = os.path.basename(r"{}".format(path)).split(".")[0]
    print(filename)
    path_to_store = os.path.dirname(r"{}".format(path))
    print(path_to_store)
    attributes = read_meta(xpt_meta)
    final_dict, meta_dict = xpt_to_json(
        attributes, path_to_store, filename, df_xpt
    )
    with open("{}".format(filename) + ".ndjson", "w", encoding="iso-8859-1") as nf:
        # Write columns metadata as a single record
        # nf.write(json.dumps({'columns': final_dict['columns']}) + '\n')
        combined_metadata = {
            "creationDateTime": str(datetime.now()),
            "datasetJSONVersion": "1.1.0",
            "fileOID": "www.cdisc.org/StudyMSGv2/1/Define-XML_2.1.0/",
            "name": attributes["table_name"],
            "label": attributes["file_label"],
            # "asOfDateTime": "<need to check>",
            "originator": "<need to check>",
            "sourceSystem": "<need to check>",
            "sourceSystemVersion": "<need to check>",
            "records": attributes["number_rows"],
            "itemGroupOID": final_dict["itemGroupOID"],
            "columns": final_dict["columns"],
        }
        nf.write(json.dumps(combined_metadata) + "\n")

        # Write each row as a separate record
        for record in final_dict["rows"]:
            nf.write(json.dumps(record) + "\n")

        # Add metaDataRef to final_dict after writing all rows
        mt = {
            "metaDataRef" : "https://metadata.location.org/TDF_ADaM_ADaMIG11/define.xml"
        }

        # Write metaDataRef to the ndjson file
        nf.write(json.dumps(mt) + '\n')


    return "{}".format(filename) + ".ndjson", final_dict, meta_dict
