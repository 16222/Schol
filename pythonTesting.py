import sqlite3, sys, subprocess

p = subprocess.Popen((["powershell.exe",
                        "./ADTesting.ps1"]),
                         stdout = sys.stdout) #i can execute the powershell script from python

