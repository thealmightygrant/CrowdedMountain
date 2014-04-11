"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from .views import home

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        self.assertTrue(response.content.startswith('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">'))
        self.assertIn('<title>Mountain Crowd Estimates</title>', response.content)
        self.assertIn('</html>', response.content)
