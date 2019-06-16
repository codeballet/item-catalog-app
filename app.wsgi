activate_this = '/vagrant/item-catalog-app/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/vagrant/item-catalog')

from item-catalog import app as application
