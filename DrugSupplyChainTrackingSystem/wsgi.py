"""
WSGI config for DrugSupplyChainTrackingSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import sys
import os

path = '/home/DrugSupplyChainTrackingSystem/DrugSupplyChainTrackingSystem'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'DrugSupplyChainTrackingSystem.settings'

# Activate virtualenv
activate_this = '/home/DrugSupplyChainTrackingSystem/myenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
