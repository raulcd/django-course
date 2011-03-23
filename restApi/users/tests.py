from django.utils import simplejson
from django.contrib.auth.models import User
from django.test import TestCase
from json import JSONDecoder

class ViewsTest(TestCase):

    fixtures = ['initial_data.json']

    def test_01_categories_fixtures(self):
        users = User.objects.all()
        self.assertEqual(len(users), 2)

    def test_02_read_user_forbidden(self):
        self.client.login(username='userfail', password='passwdfail')
        response = self.client.get('/user/')
        self.assertContains(response, 'Forbidden', count=1, status_code=401)

    def test_03_read_user_admin(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/user/')
        #There are two users in the fixtures and if the user is admin will return 2
        self.assertContains(response, 'is_staff', count=2, status_code=200)
        decoder = JSONDecoder()
        user = decoder.decode(response.content)
        self.assertEqual(len(user), 2)
        self.assertEqual(user[0]['username'], 'admin')
        self.assertEqual(user[1]['username'], 'pepe')

    def test_04_read_user_id(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/user/2')
        self.assertContains(response, 'is_staff', count=1, status_code=200)
        decoder = JSONDecoder()
        user = decoder.decode(response.content)
        self.assertEqual(user['username'], 'pepe')

    def test_05_create_user(self):
        self.client.login(username='admin', password='admin')
        json = simplejson.dumps({"username": "otro_user", "first_name": "", "last_name": "", "is_active": True, "is_superuser": False, "is_staff": False, "last_login": "2011-03-23 06:02:28", "groups": [], "user_permissions": [], "password": "sha1$38fad$5242e7230a41585712e74b1c00a66ce98fba01d3", "email": "", "date_joined": "2011-03-23 06:02:28"})
        response = self.client.post('/user/', data=json, content_type='application/json')
        self.assertContains(response, 'username', count=1, status_code=200)
        decoder = JSONDecoder()
        user = decoder.decode(response.content)
        self.assertEqual(user['username'], 'otro_user')

    def test_06_create_user_without_permission(self):
        self.client.login(username='auserwithoutPerm', password='admin')
        json = simplejson.dumps({"username": "otro_user", "first_name": "", "last_name": "", "is_active": True, "is_superuser": False, "is_staff": False, "last_login": "2011-03-23 06:02:28", "groups": [], "user_permissions": [], "password": "sha1$38fad$5242e7230a41585712e74b1c00a66ce98fba01d3", "email": "", "date_joined": "2011-03-23 06:02:28"})
        response = self.client.post('/user/', data=json, content_type='application/json')
        self.assertContains(response, 'Forbidden', count=1, status_code=401)
