import requests
import json
import os

from flask import session
from werkzeug.utils import secure_filename


class UploadDataset():
    
    BASE_URL = 'http://192.168.0.22:8080'
    LANDING = '..\\flaskfrontend\\temp'
    def __init__(self, files, metadata):
        self.files = files
        self.metadata = metadata

    def upload(self):
        files = {}
        full_paths = []
        file_objs = []
        for file in self.files:
            file_name = secure_filename(file.filename)
            full_path = os.path.join(self.LANDING, file_name)
            full_paths.append(full_path)
            file.save(full_path)
            fin = open(full_path, 'rb')
            file_objs.append(fin)
            files[full_path] = fin
        r = requests.post(
            f'{self.BASE_URL}/upload/files',
            files=files,
            headers={'SessionId': session['session_id']}
        )
        response = r.json()
        for fin in file_objs:
            fin.close()
        for full_path in full_paths:
            os.remove(full_path)
        if response['Status'] == 201:
            files = {}
            print('here')
            self.metadata['DataSetId'] = response['DataSetId']
            for file in response['Files']:
                if file['Message'] == 'Successfully uploaded':
                    files[file['FileId']] = file['FileName'] 
            self.metadata['Files'] = files
            print(self.metadata)
            r = requests.post(
                f'{self.BASE_URL}/upload/metadata',
                json=self.metadata,
                headers={'SessionId': session['session_id']}
            )
            response = r.json()
            print(response)
        return response