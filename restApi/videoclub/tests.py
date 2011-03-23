"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from models import Category


class CategoryTest(TestCase):

    fixtures = ['initial_data.json']

    def test_01_categories_fixtures(self):
        categories = Category.objects.all()
        self.assertEqual(len(categories), 2)
        
