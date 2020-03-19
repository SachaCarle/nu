import os, sys, subprocess, nu, shutil
from pathlib import Path

def globit(st, nd):
    bl = Path(st).glob(nd)
    return [str(b) for b in sorted(bl)]

cp_list = globit('.', '*.vue')



for fl in [_ for _ in cp_list if _ not in ["App.vue"]]:
    print ("BUILDING", fl)
    cp_dir = Path(nu.nupath, 'components')
    cmd = ['vue', 'build', '--target', 'wc', '--dest', 'tmp',
           '--name', fl.replace('.vue', ''), fl]
    print (' '.join(cmd))
    subprocess.Popen(cmd, shell=True).wait()
    shutil.move(str(Path('tmp', fl.replace('.vue', '.js'))), cp_dir)
    shutil.move(str(Path('tmp', fl.replace('.vue', '.js.map'))), cp_dir)
