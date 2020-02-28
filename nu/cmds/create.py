from pathlib import Path


def cmd(_, args):
    name = args.o
    folder_path = Path(name + '.nu').resolve()
    try:
        folder_path.mkdir(0o777, True)
        _.logger('created at ', folder_path)
    except Exception as e:
        folder_path.rmdir()
        _.logger('cleaned ', folder_path)
        cmd(_, args)
