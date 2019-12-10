#!/usr/bin/env python3
#
# Executes a basic skillet from the ENV variable 'SKILLET_CONTENT' useful for testing
#
import os
import sys
import oyaml

from skilletlib.exceptions import LoginException
from skilletlib.exceptions import SkilletLoaderException
from skilletlib.panoply import Panoply
from skilletlib.skillet.panos import PanosSkillet

# each variable will be present in the environ dict on the 'os' module
username = os.environ.get('TARGET_USERNAME', 'admin')
password = os.environ.get('TARGET_PASSWORD', 'admin')
ip = os.environ.get('TARGET_IP', '')
skillet_content = os.environ.get('SKILLET_CONTENT', '')

try:
    panoply = Panoply(hostname=ip, api_username=username, api_password=password, debug=False)

    # every skillet needs a 'config' item in the context
    config = panoply.get_configuration()
    context = dict()
    context['config'] = config

    # create the skillet definition from the 'skillet_content' dict we got from the environ
    skillet_dict = oyaml.safe_load(skillet_content)

    # create the skillet object from the skillet dict
    skillet = PanosSkillet(skillet_dict, panoply)

    # execute the skillet and return the results to us
    results = skillet.execute(context)

    # in this case, just print them out for the user
    print(results)
    sys.exit(0)

except SkilletLoaderException as se:
    print('Error Executing Skillet')
    print(se)
    sys.exit(1)
except LoginException as le:
    print('Error Logging into device')
    print(le)
    sys.exit(1)
