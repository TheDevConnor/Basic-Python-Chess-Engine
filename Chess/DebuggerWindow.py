from colorama import Fore, Back, Style
import subprocess
import sys
import os

#debugging tools for multiplayer (if that ever happens lol)
def createDebuggerWindow(debugMode:bool, inChessDir:bool):
    _os = None
    _shellDir = None
    _counter = 0
    _counter+=1
    print("Stage[1" + str(_counter) + "]")
    
    if type(debugMode) is bool:
        _debugMode:bool = debugMode
        _counter+=1
        print("Stage[2" + str(_counter) + "]")
    else:
        return
    p__os=sys.platform
    if(p__os == "win32"):
        p__os = "win32"
        
    elif(p__os == "cygwin"):
        p__os = "win32"
    else:
        _counter+=1
        print("Stage[3" + str(_counter) + "]")
        p__os = "*nix"
    if(p__os == "*nix"):
        compliantSlash = "/"
        _counter+=1
        print("Stage[4" + str(_counter) + "]")
    else:
        compliantSlash = "\\"
    if (inChessDir == True):
        _shellDir = ("." + compliantSlash)
    else:
        _shellDir = ("." + compliantSlash + "Chess" + compliantSlash)
    if(_debugMode == True):
        _counter+=1
        print("Stage[6" + str(_counter) + "]")
        process = subprocess.Popen([sys.executable + " " + _shellDir + "DebugShell.py"], shell=True, cwd=os.getcwd())