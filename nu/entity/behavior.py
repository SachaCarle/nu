from pathlib import Path
import sys, os, nu, json

def function(e):
    def _function():
        return f"""def _{e.name}_function_()"""
    return _function