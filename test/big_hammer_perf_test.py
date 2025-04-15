from locust import HttpUser, SequentialTaskSet,task, between
import random
import string
from locust import tag


class BigHammerUser(SequentialTaskSet):
    wait_time = between(1, 3)
    project_name  =""
    project_id = ""

    @tag('create_project')
    @task
    def create_project(self):        
        #STEP 1: Create a new project
        # Generate a random string of length 10
        self.project_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "bh_project_cld_id": "string",
            "bh_project_name": self.project_name,
            "bh_project_desc": "string",
            "cloud_provider_cd": "string",
            "cloud_region_cd": 0,
            "access_type_cd": 0,
            "access_details": {},
            "validation_status": False,
            "business_url": "string",
            "lake_name": "string",
            "lake_desc": "string",
            "env_cd": 0,
            "tags": {},
            "status_cd": 0
        }
        self.client.request_name = 'Create Project' 
        response = self.client.post('/bh_project', headers=headers, json=data)
        assert response.status_code == 200
        self.project_id = response.json()['bh_project_id']

    @tag('get_project')
    @task
    def get_project(self):
        #STEP 2: Get the project details     
        project_id = getattr(self, 'project_id', None)  
        self.client.request_name = 'Get Project' 
        response = self.client.get(f'/bh_project/{project_id}')
        assert response.status_code == 200
        
    @tag('search_project')
    @task
    def search_project(self):
        #STEP 3: Search for the project
        project_name = getattr(self, 'project_name', None)   
        self.client.request_name = 'Search Project' 
        response = self.client.get(f'/bh_project/search/?params={project_name}')
        assert response.status_code == 200
        #assert response content contains bh_project_name as project_name
        assert any(project['bh_project_name'] == project_name for project in response.json())

    @tag('delete_project')
    @task
    def delete_project(self):
        #STEP 4: Delete the project
        project_id = getattr(self, 'project_id', None)  
        self.client.request_name = 'Delete Project' 
        response = self.client.delete(f'/bh_project/{project_id}')
        assert response.status_code == 200
        assert response.json()['message'] == 'The record has been deleted!'

        #STEP 5: Get the deelted project details
        # response = self.client.get(f'/bh_project/{project_id}')
        # assert response.status_code == 404
        # assert response.json()['detail'] == 'Record is not found!'   

class WebsiteUser(HttpUser):
    tasks = [BigHammerUser]
    min_wait = 5000
    max_wait = 9000