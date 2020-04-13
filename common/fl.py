from pathlib import Path
import shutil

def remkdir(name):
    p = Path(name)
    if p.exists():
        try:
            print ('deleted: ', p)
            shutil.rmtree(p)
        except Exception as e:
            raise e
    p.mkdir()
    #print ('created: ', p)

def touchdir(name):
    p = Path(name)
    if p.exists():
        pass
    else:
        p.mkdir()
        #print ('created: ', p)