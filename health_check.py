#!/usr/bin/env python3
"""
Health check simple para verificar que la aplicación está funcionando
"""

from app import app

def test_app():
    """Prueba básica de la aplicación"""
    with app.test_client() as client:
        response = client.get('/')
        return response.status_code == 200 or response.status_code == 302

if __name__ == '__main__':
    if test_app():
        print("✅ Aplicación funcionando correctamente")
    else:
        print("❌ Error en la aplicación")
