from django.test import TestCase
from django.http import HttpRequest
from main_Side.views import main_page
from django.core.urlresolvers import resolve

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/main_Side/Welcome_to_Salamat/')
        self.assertEqual(found.func, main_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  #1
        response = main_page(request)  #2
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))  #3
        self.assertIn(b'<a href="#" class="btn btn-lg btn-dark">', response.content)  #4
        self.assertTrue(response.content.endswith(b'</html>\n'))  #5