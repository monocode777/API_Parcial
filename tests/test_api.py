import unittest
import json
import os
from app import create_app
from extensions import db

class APITestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_01_register_user(self):
        """Test registro de usuario"""
        response = self.client.post('/api/auth/register', 
                                   data=json.dumps({
                                       'email': 'test@example.com',
                                       'password': 'test123'
                                   }),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
    
    def test_02_login_valid_credentials(self):
        """Test login con credenciales válidas"""
        # Primero registrar usuario
        self.client.post('/api/auth/register', 
                        data=json.dumps({
                            'email': 'test@example.com',
                            'password': 'test123'
                        }),
                        content_type='application/json')
        
        # Luego hacer login
        response = self.client.post('/api/auth/login', 
                                   data=json.dumps({
                                       'email': 'test@example.com',
                                       'password': 'test123'
                                   }),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)
    
    def test_03_login_invalid_credentials(self):
        """Test login con credenciales inválidas"""
        response = self.client.post('/api/auth/login', 
                                   data=json.dumps({
                                       'email': 'nonexistent@example.com',
                                       'password': 'wrongpassword'
                                   }),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', data)
    
    def test_04_protected_route_without_token(self):
        """Test acceso a ruta protegida sin token"""
        response = self.client.get('/api/auth/profile')
        self.assertEqual(response.status_code, 401)
    
    def test_05_protected_route_with_token(self):
        """Test acceso a ruta protegida con token válido"""
        # Registrar y hacer login
        self.client.post('/api/auth/register', 
                        data=json.dumps({
                            'email': 'test@example.com',
                            'password': 'test123'
                        }),
                        content_type='application/json')
        
        login_response = self.client.post('/api/auth/login', 
                                        data=json.dumps({
                                            'email': 'test@example.com',
                                            'password': 'test123'
                                        }),
                                        content_type='application/json')
        login_data = json.loads(login_response.data)
        token = login_data['access_token']
        
        # Acceder a ruta protegida con token
        response = self.client.get('/api/auth/profile', 
                                 headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()