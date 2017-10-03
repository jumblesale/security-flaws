from security_flaws.app import app
import security_flaws.db as db

with app.app_context():
    db.create_schema(db.get_db())
