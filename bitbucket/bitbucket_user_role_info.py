from configparser import ConfigParser
import requests
import sys

def get_config_details(i_filepath):
    config = ConfigParser()
    config.read(i_filepath)
    return config

# This session will be used for REST calls for applications
def get_REST_session(userid, password):
    rest_session = requests.Session()
    rest_session.auth = (userid, password)
    return rest_session

# Permission Types: PROJECT_ADMIN, PROJECT_WRITE, PROJECT_READ
def get_bitbucket_project_users(rest_session, bitbucket_base_url, project_key, permission_type):
    try:
        get_response = rest_session.get(bitbucket_base_url + "/rest/api/1.0/projects/{project_key}/permissions/users".format(project_key=project_key))
        json_result = get_response.json()
        total_users = json_result['size']
        project_admins = []
        if total_users > 0:
            project_admins = [ user_permission['user']['name'] for user_permission in json_result['values'] if user_permission['permission'] == permission_type]
        return project_admins
    except requests.exceptions.HTTPError as err:
        print (err)
        sys.exit(1)        

def get_all_bitbucket_projects_admin(rest_session, bitbucket_base_url):
    are_more_projects_available = True
    start = 0
    limit = 50
    all_project_dict = {}
    try:
        while are_more_projects_available:
            get_response = rest_session.get(bitbucket_base_url + f"/rest/api/1.0/projects?start={start}&limit={limit}")
            get_result = get_response.json()
            project_list = get_result["size"]
            if(project_list > 0):
                for project in get_result["values"]:
                    all_project_dict[project['key']] = project['name']
            start += (limit + 1)
            are_more_projects_available = not bool(get_result["isLastPage"])           
    except requests.exceptions.HTTPError as err:
        print(err)
    
    for project_key in all_project_dict:
        print(f"|{all_project_dict[project_key]}|{project_key}|{', '.join(get_bitbucket_project_users(rest_session, bitbucket_base_url, project_key, 'PROJECT_ADMIN'))}|")

# Read Application Info
cred_config = get_config_details(".application_info")
userid = cred_config.get("bitbucket_server", "userid")
password = cred_config.get("bitbucket_server", "password")
bitbucket_base_url = cred_config.get("bitbucket_server", "base_url")

project_role = input('Provide one role (PROJECT_ADMIN | PROJECT_WRITE | PROJECT_READ) for which you want user list: ')
project_key = input('Provide Project Key: ')
rest_session = get_REST_session(userid, password)

print(get_bitbucket_project_users(rest_session, bitbucket_base_url, project_key, project_role))

#get_all_bitbucket_projects_admin(rest_session, bitbucket_base_url)