activate_this = '/vagrant/item_catalog_app/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/vagrant/item_catalog_app')

from app import app as application
