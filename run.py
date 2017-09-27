import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "security_flaws"))

from security_flaws.app import app

app.run()
