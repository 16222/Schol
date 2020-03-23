import sqlite3, sys, subprocess

p = subprocess.Popen((["powershell.exe",
                        "./powershellTesting.ps1"]),
                         stdout = sys.stdout)