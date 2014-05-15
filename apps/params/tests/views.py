# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     params

Descripcion: Testing de las views de la app params
"""
from django.test import TestCase
from apps.params.models import Locality
import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class ParamsViewsTestCase(TestCase):
    fixtures = ['testdata.json'] #lee segun indica FIXTURE_DIRS del setting.py
    
    def setUp(self):
        #response = self.client.get('/params/locality/index/')
        #account = authenticate(username='admin', password='12345')
        #login(response, account)
        user = User.objects.create_superuser(username="admin", email="a@gmail.com", password="12345")
        #user.save()
            
        #self.poll_1 = Locality.objects.get(id=1)
        #self.poll_2 = Locality.objects.get(pk=2)
        now = datetime.datetime.now()
        self.poll = Locality.objects.create(
            name= "Juliaca3",
            location= "loca ju",
            utm= "ut ju",
            msnm= 3800,
            is_active= True,
            registered_at= now, 
            modified_in= now
        )
        #self.assertEqual(poll.name, "Juliaca3")
        #from django.db import connections
        #from django.conf import settings
       # connections.databases = settings.DATABASES = {}
        #connections._connections['default'].close()
        #del connections._connections['default']
    
        
    def test_locality_index(self):
        """
        Tests that carga la página /home/
        """
        locals= Locality.objects.all()
        print locals
        self.client.login(username="admin", password="12345")
        response = self.client.get('/params/locality/index/')
                
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_module' in response.context)
        self.assertTrue('page_title' in response.context)
        self.assertEqual(response.context['page_title'], "Lista de localidades.")
        self.assertTrue('locality_page' in response.context)
        d_1 = response.context['locality_page'][0]
        #d_1 = self.poll
        self.assertEqual(d_1.name, 'Juliaca3')
        #self.assertEqual([d.pk for d in response.context['locality_page']], [1])
        self.assertTrue(Locality.objects.count()>0)
        
        
        
        