import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "security_flaws"))

from security_flaws.app import app
import security_flaws.db as db

with app.app_context():
    db.create_schema(db.get_db())
    db.insert_fixtures(db.get_db())

app.run()
