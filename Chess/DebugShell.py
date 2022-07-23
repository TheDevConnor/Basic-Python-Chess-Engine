import re, os, sys
from click import style
from colorama import Fore, Back, Style
from colorama import init
import subprocess

global _input
global _pattern
global _running
global _os

def startShell(pattern):
    _running = True
    _os=sys.platform
    init()
    compliantSlash:str = None
    if(_os == "win32"):
        compliantSlash = "\\"
    elif(_os == "cygwin"):
        compliantSlash = "\\"
    else:
        compliantSlash = "/"
    while True:
        while _running:
            _input = input(Fore.BLACK + Back.GREEN + Style.DIM + "$ ")
            if (not re.search(pattern, _input)):
                print("Invalid syntax!")
                break
                
        if(not re.search(pattern, _input)):
            _running = True
        else:
            break

if (__name__ == "__main__"):
    _pattern = "[a-zA-Z1-9\!\@\#\$\%\^\&\*\(\)\-\_\+\=\`\~\<\>\/\?]+"
    startShell(_pattern)
