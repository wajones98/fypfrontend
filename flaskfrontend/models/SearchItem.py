from flask import session, send_file, make_response
import requests
import shutil
import os
import boto3
import json

BASE_URL = 'http://192.168.0.22:8080'
LANDING = '..\\flaskfrontend\\temp'

class SearchItem:
    
    def __init__(self):
        self.item_id = None
        self.search_result = {'Files': []}
        SearchItem.clear_temp_folder(session['session_id'])
        return

    def set_data_set_name(self, data_set_name):
        self.search_result['DatasetName'] = data_set_name
        return self

    def get_data_set_name(self):
        return self.search_result['DatasetName']

    def set_project_name(self, project_name):
        self.search_result['ProjectName'] = project_name
        return self
    
    def get_project_name(self):
        return self.search_result['ProjectName']

    def set_signal_type(self, signal_type):
        self.search_result['SignalType'] = signal_type
        return self
    
    def get_signal_type(self):
        return self.search_result['SignalType']

    def set_species(self, species):
        self.search_result['Species'] = species 
        return self
    
    def get_species(self):
        return self.search_result['Species']

    def set_gender(self, gender):
        self.search_result['Gender'] = gender
        return self
    
    def get_gender(self):
        return self.search_result['Gender']
    
    def set_age(self, age):
        self.search_result['Age'] = age
        return self
    
    def get_age(self):
        return self.search_result['Age']

    def set_target(self, target):
        self.search_result['Target'] = target
        return self
    
    def get_target(self):
        return self.search_result['Target']

    def set_action(self, action):
        self.search_result['Action'] = action
        return self
    
    def get_action(self):
        return self.search_result['Action']

    def set_channel_count(self, channel_count):
        self.search_result['ChannelCount'] = channel_count
        return self
    
    def get_channel_count(self):
        return self.search_result['ChannelCount']

    def set_device(self, device):
        self.search_result['Device'] = device
        return self
    
    def get_device(self):
        return self.search_result['Device']

    def set_tags(self, tags):
        self.search_result['Tags'] = tags
        return self
    
    def get_tags(self):
        return self.search_result['Tags']

    def set_files(self, files):
        self.search_result['Files'] = files
        return self
    
    def get_files(self):
        return self.search_result['Files']
    
    def set_data_set_id(self, data_set_id):
        self.search_result['DatasetId'] = data_set_id
        return self
    
    def get_data_set_id(self):
        return self.search_result['DatasetId']

    @staticmethod
    def get_search_items(body):
        r = requests.post(
            f'{BASE_URL}/search',
            json=body,
            headers={'SessionId': session['session_id']}
        )
        response = r.json()

        search_items = []
        datasets = set()
        for item in response['Results']:       
            if item['DatasetId'] not in datasets:
                search_item = SearchItem()
                search_item.set_data_set_name(item['DatasetName'])
                search_item.set_project_name(item['ProjectName'])
                search_item.set_signal_type(item['SignalType'])
                search_item.set_species(item['Species'])
                search_item.set_gender(item['Gender'])
                search_item.set_age(item['Age'])
                search_item.set_target(item['Target'])
                search_item.set_action(item['Action'])
                search_item.set_channel_count(item['ChannelCount'])
                search_item.set_device(item['Device'])
                search_item.set_data_set_id(item['DatasetId'])
                search_item.set_tags(item['Tags'])
                file_info = {
                    'Filename': item['Filename'],
                    'Filepath': item['Filepath'],
                    'Change': item['Change']
                }
                search_item.get_files().append(file_info)
                search_items.append(search_item)
            else:
                for data_set in search_items:
                    if item['DatasetId'] == data_set.get_data_set_id():
                        file_info = {
                            'Filename': item['Filename'],
                            'Filepath': item['Filepath'],
                            'Change': item['Change']
                        }
                        data_set.get_files().append(file_info)
                        session[item['DatasetId']] = data_set.get_files()
            datasets.add(item['DatasetId'])
        return search_items

    @staticmethod
    def download_file(file_info):
        bucket = 'fyp-data-repo'
        s3_client = boto3.client('s3')
        local_directory = os.path.join(LANDING, session['session_id'])
        if not os.path.exists(local_directory):
            os.mkdir(local_directory)
        full_local_path = os.path.join(local_directory, file_info['fileName'])
        s3_client.download_file(bucket, file_info['filePath'], full_local_path)
        return send_file(full_local_path, as_attachment=True)
    
    @staticmethod
    def download_dataset(dataset_info):
        bucket = 'fyp-data-repo'
        s3_client = boto3.client('s3')
        
        local_directory = os.path.join(LANDING, session['session_id'])
        if not os.path.exists(local_directory):
            os.mkdir(local_directory)
        
        dataset_directory = os.path.join(local_directory, dataset_info['dataset'])
        if not os.path.exists(dataset_directory):
            os.mkdir(dataset_directory)
        
        file_info = dataset_info['fileInfo']
        for file in file_info:
            full_local_path = os.path.join(dataset_directory, file['Filename'])
            s3_client.download_file(bucket, file['Filepath'], full_local_path)

        zipped_file = shutil.make_archive(dataset_directory, 'zip', dataset_directory)
        
        return send_file(zipped_file, as_attachment=True)
    
    @staticmethod
    def clear_temp_folder(session_id):
        directory = os.path.join(LANDING, session['session_id'])
        if os.path.exists(directory):
            shutil.rmtree(directory)