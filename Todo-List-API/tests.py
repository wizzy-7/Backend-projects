import requests

def test():
    register_url = 'http://127.0.0.1:5000/register'
    register_data = {
        'name': 'testname',
        'email': 'test@email.com',
        'password': 'password'
    }
    register_response = requests.post(register_url, json=register_data)
    print(f'Register response: {register_response.json()}')
    
    login_url = 'http://127.0.0.1:5000/login'
    login_data ={
        'email': 'test@email.com',
        'password': 'password'
    }
    login_response = requests.post(login_url, json=login_data)
    login_r = login_response.json()
    print(f'Login response: {login_r}')
    
    token = login_r.get('token')
    if not token:
        print('Failed to obtain token.')
    else:
        headers={'Authorization': token}
        todos_response = requests.get('http://127.0.0.1:5000/todos', headers=headers)
        print('Todos response:', todos_response.json())
        
    
if __name__ == '__main__':
    test()