import sqlite3, sys, subprocess

p = subprocess.Popen((["powershell.exe",
                        "./Project/query.ps1"]),
                         stdout = sys.stdout) #i can execute the powershell script from python
