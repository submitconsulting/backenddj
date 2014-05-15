# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     BackendDJ

Descripcion: Testing del sistema
"""
from django.test import TestCase

# Create your tests here.
class SimpleTest(TestCase):
#    def setUp(self):
        
    def test_home_page(self):
        """
        Tests that carga la página de inicio
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)