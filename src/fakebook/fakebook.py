'''
Created on 19-03-2013

@author: karol
'''
import requests

import json

class FakebookException(Exception):
    
    def __init__(self, raw_text):
        self.facebook_response = raw_text 

class FakebookUser(object):
    
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.access_token = kwargs['access_token']
        self.login_url = kwargs['login_url']
        self.email = kwargs.get('email', None)
        self.password = kwargs.get('password', None)

class FakebookContextManager(object):
    
    def __init__(self, count, permissions, fb_app):
        self.count = count
        self.permissions = permissions
        self.users = []
        self.fb_app = fb_app
    
    def __enter__(self):
        for _ in range(0, self.count):
            self.users.append(self.fb_app.create_test_user(permissions=self.permissions))
        return self.users
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # just make requests to delete users no matter what
        for user in self.users:
            self.fb_app.delete_user(user.id, user.access_token)
        return False

class Fakebook(object):
    
    def __init__(self, app_id, access_token):
        self.app_id = app_id
        self.access_token = access_token
    
    @staticmethod
    def get_app_access_token(app_id, app_secret):
        path = 'https://graph.facebook.com/oauth/access_token'
        query_params = {
            'client_id': app_id,
            'client_secret': app_secret,
            'grant_type': "client_credentials"
        }
        response = requests.get(path, params=query_params)
        try:
            token = response.text.split('=')[1]
        except Exception:
            raise FakebookException(response.text)
        return token
    
    def create_test_user(self, installed=True, name='Fakebook User', locale='en_US', permissions=None):
        path = 'https://graph.facebook.com/{app_id}/accounts/test-users'
        query_params = {
            'installed': installed,
            'name': name,
            'locale': locale,
            'permissions': permissions,
            'method': "post",
            'access_token': self.access_token
        }
        response = requests.get(path.format(app_id=self.app_id), params=query_params)
        try:
            user = FakebookUser(**json.loads(response.text))
        except Exception:
            raise FakebookException(response.text)
        return user
    
    def add_user_to_app(self, uid, other_app_id, other_app_token, installed=True, permissions=''):
        path = 'https://graph.facebook.com/{app_id}/accounts/test-users'
        query_params = {
            'uid': uid,
            'owner_access_token': self.access_token,
            'installed': installed,
            'permissions': permissions,
            'method': "post",
            'access_token': other_app_token
        }
        response = requests.get(path.format(app_id=other_app_id), params=query_params)
        try:
            user = FakebookUser(**json.loads(response.text))
        except Exception:
            raise FakebookException(response.text)
        return user
    
    def send_friend_request(self, sender_id, access_token, recipient_id):
        path = 'https://graph.facebook.com/{uid1}/friends/{uid2}'
        query_params = {
            'method': "post",
            'access_token': access_token
        }
        response = requests.get(path.format(uid1=sender_id, uid2=recipient_id), params=query_params)
        if response.text != "true":
            raise FakebookException(response.text)
    
    def accept_friend_request(self, recipient_id, access_token, sender_id):
        path = 'https://graph.facebook.com/{uid1}/friends/{uid2}'
        query_params = {
            'method': "post",
            'access_token': access_token
        }
        response = requests.get(path.format(uid1=recipient_id, uid2=sender_id), params=query_params)
        if response.text != "true":
            raise FakebookException(response.text)
    
    def get_users(self):
        path = 'https://graph.facebook.com/{app_id}/accounts/test-users'
        query_params = {'access_token': self.access_token}
        response = requests.get(path.format(app_id=self.app_id), params=query_params)
        try:
            l = json.loads(response.text)['data']
            users = [FakebookUser(**obj) for obj in l]
        except Exception:
            raise FakebookException(response.text)
        return users
    
    def delete_user_from_app(self, user_id):
        """
        https://graph.facebook.com/TEST_USER_ID?
          method=delete
          &access_token=TEST_USER_ACCESS_TOKEN (OR) APP_ACCESS_TOKEN
        """
        path = 'https://graph.facebook.com/{user_id}'
        query_params = {'access_token': self.access_token, 'method': "delete"}
        response = requests.get(path.format(user_id=user_id), params=query_params)
        if response.text != "true":
            raise FakebookException(response.text)
    
    def delete_user(self, user_id, user_token):
        """
        https://graph.facebook.com/TEST_USER_ID?
          method=delete
          &access_token=TEST_USER_ACCESS_TOKEN (OR) APP_ACCESS_TOKEN
        """
        path = 'https://graph.facebook.com/{user_id}'
        query_params = {'access_token': user_token, 'method': "delete"}
        response = requests.get(path.format(user_id=user_id), params=query_params)
        if response.text != "true":
            raise FakebookException(response.text)
    
    def managed_users(self, count, permissions):
        return FakebookContextManager(count, permissions, self)