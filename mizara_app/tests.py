import requests
import json

BASE_URL = 'http://localhost:8000/'

def print_results(response):
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.text}')

def create_user(username,first_name,last_name,email,password):
    url = BASE_URL + 'users/'
    data = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print_results(response)

def get_user(pk):
    url = BASE_URL + f'users/{pk}/'
    response = requests.get(url)
    print_results(response)


def update_user(pk):
    url = BASE_URL + f'users/{pk}/'
    data = {
        'username': 'janedoe',
        'email': 'janedoe@example.com',
        'password': 'newpassword123'
    }
    headers = {'Content-type': 'application/json'}
    response = requests.put(url, data=json.dumps(data), headers=headers)
    print_results(response)

def delete_user(pk):
    url = BASE_URL + f'users/{pk}/'
    response = requests.delete(url)
    print_results(response)
def authenticate(username, password):
    url = BASE_URL + 'token/'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data=data)
    print_results(response)
# create_user('lucazh','luca','zh','luca@zh.com','password123')
# get_user(1)
# create_user('john', 'luca','zh','luca@zh.com','password123')
authenticate('lucazh','password123')


import os,magic
import requests

url = 'http://localhost:8000/fichiers/'

file_path = '/home/rimuru/Documents/5243-prog_dynamique.pdf'

file_name = '5243-prog_dynamique.pdf'
mime = magic.Magic(mime=True)
data = {
    'nom': file_name,
    'taille': os.path.getsize(file_path),
    'type_fichier': mime.from_file(file_path),
}

headers = {
    'Authorization': '56ab8d15eb6e0d619357fbc0d662d7c36342b393',
}

with open(file_path, 'rb') as f:
    response = requests.post(url, data=data, files={'fichier': f}, headers=headers)

print(response.json())

url = 'http://localhost:8000/directory/'

params = {'directory': '/home/'}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print('Directories:', data['directories'])
    print('Files:', data['files'])
else:
    print('Error:', response.status_code)