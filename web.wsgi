import subprocess
subprocess.call([r'D:\xampp\htdocs\server\venv2\Scripts\activate.bat'])
import sys
sys.path.insert(0, 'D:/xampp/htdocs/server')
from scripts.__init__ import app as application