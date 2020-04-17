from flask import session
import json
import requests

BASE_URL = 'http://192.168.0.22:8080'

class Project:
   
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
    def get_users_projects():
        r = requests.get(
            f'{BASE_URL}/project/get',
            headers={'SessionId': session['session_id']}
        )
        response = r.json()
        projects = []
        for item in response['Projects']:
            project = Project()
            project.set_name(item['Name'])
            project.set_desc(item['Desc'])
            project.set_creator(item['Creator'])
            project.set_start(item['StartDate'])
            project.set_end(item['EndDate'])
            project.set_public(item['Public'])
            project.set_members(item['Members'])
            projects.append(project)
        return projects
        
    def __init__(self):
        self.project_id = None
        self.project = {}

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