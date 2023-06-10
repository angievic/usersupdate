import requests
import os
import sys

GITHUB_API_BASE_URL = 'https://api.github.com'
FRESHDESK_API_BASE_URL = 'https://<FRESHDESK_SUBDOMAIN>.freshdesk.com/api/v2'  # Replace with your Freshdesk subdomain

def get_github_user(username):
    url = f'{GITHUB_API_BASE_URL}/users/{username}'
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Failed to retrieve GitHub user: {response.status_code} {response.text}')

def create_or_update_freshdesk_contact(user):
    url = f'{FRESHDESK_API_BASE_URL}/contacts'
    headers = {'Authorization': os.getenv('FRESHDESK_TOKEN'), 'Content-Type': 'application/json'}
    payload = {
        'name': user.get('name', ''),
        'email': user.get('email', ''),
        'phone': user.get('phone', ''),
        # Add additional fields as needed based on your judgment
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print('Contact created/updated successfully in Freshdesk')
    else:
        raise Exception(f'Failed to create/update contact in Freshdesk: {response.status_code} {response.text}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python usersupdate.py <GitHub username> <Freshdesk subdomain>')
        sys.exit(1)

    github_username = sys.argv[1]
    freshdesk_subdomain = sys.argv[2]

    os.environ['GITHUB_TOKEN'] = 'your_github_token'
    os.environ['FRESHDESK_TOKEN'] = 'your_freshdesk_api_key'

    user = get_github_user(github_username)
    create_or_update_freshdesk_contact(user)
