# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     home

Descripcion: Testing de las views de la app home
"""
from django.test import TestCase



class HomeViewsTestCase(TestCase):
    
    def test_index(self):
        """
        Tests that carga la página /home/
        """
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_module' in response.context)
        self.assertTrue('page_title' in response.context)
        self.assertEqual(response.context['page_title'], "DjangoBackend Home Page.")