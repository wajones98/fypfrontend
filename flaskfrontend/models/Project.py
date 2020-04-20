from flask import session
import json
import requests
from models.SearchItem import SearchItem

BASE_URL = 'http://127.0.0.1:8080'

class Project:

    @staticmethod
    def make_public(json_body):
        r = requests.post(
            f'{BASE_URL}/project/mode',
            json=json_body,
            headers={'SessionId': session['session_id']}
        )
        response = r.json()
        return response

    @staticmethod
    def leave_project(json_body):
        r = requests.post(
            f'{BASE_URL}/project/leave',
            json=json_body,
            headers={'SessionId': session['session_id']}
        )
        response = r.json()
        return response

    @staticmethod
    def invite_project(json_body):
        r = requests.post(
            f'{BASE_URL}/project/invite',
            json=json_body,
            headers={'SessionId': session['session_id']}
        )
        response = r.json()
        return response

    @staticmethod
    def join_project(json_body):
        r = requests.post(
            f'{BASE_URL}/project/join',
            json=json_body,
            headers={'SessionId': session['session_id']}
        )
        response = r.json()
        return response

    @staticmethod
    def create_project(json_body):
        r = requests.post(
            f'{BASE_URL}/project/create',
            json=json_body,
            headers={'SessionId': session['session_id']}
        )
        response = r.json()
        return response

    @staticmethod
    def get_users_invitations():
        r = requests.get(
            f'{BASE_URL}/project/get/invitations',
            headers={'SessionId': session['session_id']}
        )
        response = r.json()
        projects = []
        for item in response['Projects']:
            project = Project()
            project.set_project_id(item['ProjectId'])
            project.set_name(item['Name'])
            project.set_creator(item['Creator'])
            projects.append(project)
        return projects

    @staticmethod
    def get_users_projects():
        r = requests.get(
            f'{BASE_URL}/project/get',
            headers={'SessionId': session['session_id']}
        )
        response = r.json()
        projects = []
        for item in response['Projects']:
            project = Project()
            project.set_project_id(item['ProjectId'])
            project.set_name(item['Name'])
            project.set_desc(item['Desc'])
            project.set_creator(item['Creator'])
            project.set_start(item['StartDate'])
            project.set_end(item['EndDate'])
            project.set_public(item['Public'])
            project.set_members(item['Members'])
            project.set_datasets(SearchItem.get_search_items({'Parameters': {"ProjectId": project.get_project_id()}}, private=False))
            projects.append(project)
        return projects
        
    def __init__(self):
        self.project_id = None
        self.project = {}

    def set_project_id(self, id):
        self.project_id = id
        return self

    def get_project_id(self):
        return self.project_id

    def set_name(self, name):
        self.project['name'] = name
        return self
    
    def get_name(self):
        return self.project['name']

    def set_desc(self,desc):
        self.project['desc'] = desc 
        return self
    
    def get_desc(self):
        return self.project['desc']

    def set_start(self,start):
        self.project['start'] = start
        return self
    
    def get_start(self):
        return self.project['start']    
    
    def set_end(self,end):
        self.project['end'] = end 
        return self
    
    def get_end(self):
        return self.project['end']

    def set_public(self,public):
        self.project['public'] = public
        return self
    
    def get_public(self):
        return self.project['public']

    def set_creator(self, creator):
        self.project['creator'] = creator
        return self
    
    def get_creator(self):
        return self.project['creator']

    def set_members(self, members):
        self.project['members'] = members
        return self
    
    def get_members(self):
        return self.project['members']

    def set_datasets(self, datasets):
        self.project['datasets'] = datasets
        ids = []
        for dataset in self.project['datasets']:
            ids.append(dataset.get_data_set_id())
        self.project['dataset_ids'] = ids
        return self

    def get_datasets(self):
        return self.project['datasets']

    def get_dataset_ids(self):
        return self.project['dataset_ids']