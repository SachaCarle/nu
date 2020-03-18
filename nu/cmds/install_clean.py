from pathlib import Path
import os, shutil
def cmd(_, args, nupath=None, **kwargs):
    assert nupath
    xx = os.path.join('X', 'nu').replace('X', '')
    rmd = ''.join(nupath.rsplit(xx, 1))
    if 'nuloader' in nupath:
        for mn in ['nu', 'nujs', 'nuthon']:
            p = Path(rmd, mn).resolve()
            print ("DELETING\t", p)
            shutil.rmtree(p)
    elif 'nusys' in nupath:
        for mn in ['nuloader']:
            p = Path(rmd, mn).resolve()
            print ("DELETING\t", p)
            shutil.rmtree(p)
    else:
        print (xx, nupath, "Heyy", rmd)
