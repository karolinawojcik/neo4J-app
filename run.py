# coding=UTF-8
from sources import app
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app.secret_key = os.urandom(24)
app.run(debug=True)