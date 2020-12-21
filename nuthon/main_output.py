from pathlib import Path

def get_comments_blocks(nuthon_root, nuthon_file):
    from . import parse_lines
    code_ = Path(nuthon_root, nuthon_file).read_text()
    return parse_lines(code_).res

def write_interpreter(filename):
    nuthon_root = str(Path(__file__).resolve()).replace(Path(__file__).stem + Path(__file__).suffix, '')
    filename = Path(filename).resolve()
    code_main = get_comments_blocks(nuthon_root, "__main__.py")
    code_scope = get_comments_blocks(nuthon_root, "class_Scope.py")
    tx = ""
    tx += "\n".join(code_scope['CLASS_SCOPE']) + '\n'
    tx += "\n".join(code_main['ARGPARSE_0']) + '\n'
    tx += "\n".join(code_main['ARGPARSE_1']) + '\n'
    tx += "\n".join(code_main['MAIN_0']) + '\n'
    tx += "\n".join(code_main['INTERPRETER']) + '\n'
    tx += "\n".join(code_main['CONSOLE']) + '\n'
    tx += "\n".join(code_main['OUTPUT'])
    filename.write_text(tx)