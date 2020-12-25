from pathlib import Path

def get_comments_blocks(nuthon_root, nuthon_file):
    from . import parse_lines
    code_ = Path(nuthon_root, nuthon_file).read_text()
    return parse_lines(code_).res

def join_code(code_dict, key):
    r = "\n# OPEN " + key + '\n'
    r += "\n".join(code_dict[key]) + '\n'
    r += "# CLOSE " + key + '\n'
    return r

def write_interpreter(filename):
    nuthon_root = str(Path(__file__).resolve()).replace(Path(__file__).stem + Path(__file__).suffix, '')
    filename = Path(filename).resolve()
    code_main = get_comments_blocks(nuthon_root, "__main__.py")
    code_scope = get_comments_blocks(nuthon_root, "class_Scope.py")
    tx = ""
    tx += join_code(code_scope, 'CLASS_SCOPE')
    tx += join_code(code_main, 'ARGPARSE_0')
    tx += join_code(code_main, 'ARGPARSE_1')
    tx += join_code(code_main, 'MAIN_0')
    tx += join_code(code_main, 'INTERPRETER')
    tx += join_code(code_main, 'CONSOLE')
    tx += join_code(code_main, 'OUTPUT')
    filename.write_text(tx)