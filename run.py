import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "security_flaws"))

import security_flaws.db as db

db.create_schema()
db.insert_fixtures()
print(db.find_user_by_username('charles'))

from security_flaws.app import app

app.run()
