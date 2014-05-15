# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     account

Descripcion: Testing de las views de la app account
"""
from django.test import TestCase



class AccountViewsTestCase(TestCase):
    
    def test_index(self):
        """
        Tests that carga la página /home/
        """
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)