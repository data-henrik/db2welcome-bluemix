import os
from flask import Flask,redirect,render_template
import urllib
import datetime
import json
import ibm_db

app = Flask(__name__)

# get service information if on Bluemix
if 'VCAP_SERVICES' in os.environ:
   db2info = json.loads(os.environ['VCAP_SERVICES'])['sqldb'][0]
   db2cred = db2info["credentials"]


# connect to DB2
db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")

# main page to dump some environment information
@app.route('/')
def index():
   page = '<title>Welcome DB2!</title>'
   page += '<h1>Welcome DB2!</h1>'
   page += 'Want to retrieve <a href="dbinfo">system information</a>?'
   return page

@app.route('/dbinfo')
def dbinfo():
   if db2conn:
     # we have a DB2 connection, so obtain system information via ENV_SYS_INFO:
     stmt = ibm_db.exec_immediate(db2conn,"select * from sysibmadm.env_sys_info")
     # fetch the result
     result = ibm_db.fetch_assoc(stmt)
   return render_template('dbinfo.html', db2info=result)


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
