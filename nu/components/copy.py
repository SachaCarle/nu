import sys, os, subprocess
from pathlib import Path

module_path = Path(os.path.split(__file__)[0])
components_path = Path(module_path, 'builded')

def copy(cp_name, entity):
    cp_file_js = Path(module_path, 'nu-' + cp_name + '.js')
    cp_file = Path(components_path, cp_name)
    if not cp_file_js.exists():
        unbuild_path = str(Path(module_path, 'vue_components', 'src', 'components', cp_name))
        cmd = ["ls"]
        print ("!! \tBUILDING " + cp_name + "\n\t\t" + str(cmd))
        subprocess.Popen(cmd, shell=True, stdout=True).wait()

        cmd = ['vue', "build", "--target", "wc", "--dest", str(module_path), "--name", "nu-" + cp_name, unbuild_path + ".vue"]
        build_dir = str(Path(module_path, 'vue_components'))
        print ("!! \tBUILDING " + cp_name + " at " + build_dir + "\n\t\t" + str(cmd))
        subprocess.Popen(cmd, shell=True, cwd=build_dir).wait()
    print (cp_file_js, cp_file)