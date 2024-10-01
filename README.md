# Dataset-JSON-1.1-Interface

This tool converts the uploaded xpt file to JSON or NDJSON file based on the user preference.

To use this tool follow the below steps:
1. Install python 3.8 or above and install the packages as mentioned in the requirements.txt
2. Please have any Python IDE in the system like Pycharm, Visual Studio or Intellij
3. Open the folder that has the codebase in the IDE
4. You can install the packages by either of the following commands in terminal:
   pip install <package_name>==<version>
   or pip install -r requirements.txt
5. Once all packages are installed, run the following command:
   python app.py
   This will open local host window on your browser, where you can upload the XPT file and get it   
   converted to either JSON or NDJSON.
<img width="946" alt="image" src="https://github.com/user-attachments/assets/59667c15-942e-4bcc-bc9a-d9a0609e13f9">
5.1 Click on "Select File Type" and select the desired file type to get the XPT file converted (JSON/NDJSON)
5.2 Click on "Choose File" button and upload the ".xpt" file from local
5.3 Click on "Generate Target File" button, this will open the page
   ![image](https://github.com/user-attachments/assets/723ad699-a54f-429a-ae02-a8a3543dc989)
5.4 On clicking "View Metadata", the corresponding metadata alone will be viewed and on clicking "View Data", the corresponding dataset alone will be viewed (both in JSON format)
5.5 Click on "Download" button to download the ".json" or ".ndjson" file generated.


