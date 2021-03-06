#!/usr/bin/env python
__author__ = "hloverflow"
__credits__ = ["stephenbradshaw"]

from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto import Random
from flask import Flask, request 
from lxml import etree
import cgi
import html
import traceback
import sys

app = Flask(__name__)

# Config stuff
KEY = Random.new().read(32)  # 256 bit key for extra security!!!
BLOCKSIZE = AES.block_size
ADMIN_SECRET = Random.new().read(32)  # need to keep this secret
APP_NAME = 'Flask XXE demo - Python etree parser'
APP_VERSION = '0.1 pre pre pre alpha'

CONFIG = {
    'encrypto_key': b64encode(KEY),
    'secret_admin_value': b64encode(ADMIN_SECRET),
    'app_name': APP_NAME,
}


@app.route('/')
def index():
    return """
    <html>
    <head><title>Vulnerable Flask App: """ + CONFIG['app_name'] + """</title></head>
    <body>
        <p><h3>Functions</h3></p>
        <a href="/xml">Parse XML</a><br>
    </body>
    </html>
    """

# credits to stephenbradshaw/breakableflask for the base. I merely modified his code. 
# xml external entities and DTD
@app.route('/xml', methods=['POST', 'GET'])
def xml():
    parsed_xml = None
    errormsg = ''
    
    htmlData = """
    <html>
      <body>
    """
    
    if request.method == 'POST':
        xml = request.form['xml']
        parser = etree.XMLParser(no_network=False) # to enable network entity. see xmlparser-info.txt
        try:
            doc = etree.fromstring(str(xml), parser)
            parsed_xml = etree.tostring(doc)
            print (parsed_xml)
        except:
            print ("Cannot parse the xml")
            htmlData += "Error:\n<br>\n" + traceback.format_exc()
    if (parsed_xml):
        htmlData += "Result:\n<br>\n" + html.escape(parsed_xml.decode("utf-8"))
    else:
        htmlData += """
                  <form action = "/xml" method = "POST">
                     <p><h3>Enter xml to parse</h3></p>
                     <textarea class="input" name="xml" cols="40" rows="5"></textarea>
                     <p><input type = 'submit' value = 'Parse'/></p>
                  </form>
                """
    htmlData += """
            </body>
        </html>
        """
    return htmlData


# credits to stephenbradshaw/breakableflask for the base. I merely modified his code. 
# xml external entities and DTD ( without returning error message )
@app.route('/blindxml', methods=['POST', 'GET'])
def blindxml():
    parsed_xml = None
    errormsg = ''
    
    htmlData = """
    <html>
      <body>
    """
    
    if request.method == 'POST':
        xml = request.form['xml']
        parser = etree.XMLParser(no_network=False) # to enable network entity. see xmlparser-info.txt
        try:
            doc = etree.fromstring(str(xml), parser)
            parsed_xml = etree.tostring(doc)
            print (repr(parsed_xml))
        except:
            print ("Cannot parse the xml")
            # htmlData += "Error:\n<br>\n" + traceback.format_exc()
    if (parsed_xml):
        htmlData += "Result:\n<br>\n" + parsed_xml.decode("utf-8") 
    else:
        htmlData += """
          <form action = "/blindxml" method = "POST">
             <p><h3>Enter xml to parse</h3></p>
             <textarea class="input" name="xml" cols="40" rows="5"></textarea>
             <p><input type = 'submit' value = 'Parse'/></p>
          </form>
        """
    htmlData += """
      </body>
    </html>
    """
    return htmlData

if __name__ == '__main__':
    lport=9999
    try:
        lport=sys.argv[1]
    except:
        lport=9999
    app.run(host='0.0.0.0', port=lport)
