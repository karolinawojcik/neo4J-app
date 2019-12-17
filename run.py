# coding=UTF-8
from sources import app
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app.secret_key = os.urandom(24)
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)