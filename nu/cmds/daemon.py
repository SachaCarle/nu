from pathlib import Path
import multiprocessing as mp
import os, shutil, subprocess, json, nu, sys

def aprint(*args, **kwargs):
    print (*args, **kwargs)
    sys.stdout.flush()


def entity_script(entity_path, *debug):
    p = subprocess.Popen(["python", '-m', "nu", "awake"], stdout=subprocess.PIPE)
    entity_path = str(entity_path)
    state = None
    #aprint ("#--\t", entity_path + ":")
    text = []
    for line in p.stdout:
        try:
            line = line.decode('ascii')
        except Exception as e:
            print ("<!>\tAn error occured decoding: '{}': {}".format(line, e))
        chks = line.split(':')
        #aprint(chks[0] + '.nu', " >>> ", line.replace('\r', '').replace('\n', ''))
        if chks[0] + '.nu' == entity_path:
            line = line.replace('\r', '').replace('\n', '')
            nl = line.replace(chks[0] + ': ', '')
            #aprint ("\t|" + line + "|\t|" + chks[0] + ': ' + '|')
            if nl == '__PRAY_END__':
                assert state == "praying"
                nl = " ~ * ~ "
                state = None
                aprint (os.getcwd(), "\t-\t", nl)
                break
            if state == 'praying':
                aprint (os.getcwd(), "\t-\t\t", nl)
                text.append(nl)
                continue
            elif nl == '__PRAY_ENTER__':
                nl = " ~ * ~ "
                state = "praying"
            aprint (os.getcwd(), "\t-\t", nl)
    def fun(dae):
        p.wait()
        if len(text) > 0:
            #aprint ("ENTITY WORKSHIPPING, process: ", debug, os.getcwd() )
            for nl in text:
                #aprint ('nu.workship({})'.format(nl))
                dae.com.send(nl)
            #aprint ("ENTITY ", entity_path, " STOP FROM PRAYING !!")
        #aprint ("ENTITY ", entity_path, " STOP !!")
        # Executed by the top layer process !!
    return (p, fun)

def globit(st, nd):
    bl = Path(st).glob(nd)
    return [str(b) for b in sorted(bl)]

def is_in(ls, s):
    for l in ls:
        if l in s:
            return True
        if s.endswith(l):
            return True
    return False

debug = ["wecandoo"]
_ignored = []
def select(s):
#    if 'recycle' in s:
#        aprint ("WTF ?", s)
    if os.path.split(s)[1].startswith('.') or is_in(["node_modules", "$Recycle.Bin", "$RECYCLE.BIN", ".git", "__pycache__", ".bin", ".cache", "vendor", "Application Data",
            "AppData", "Caches", "Settings", "Program Files (x86)", "WinSxS", "eSupport", "Program Files",
            "lib", "bin", "SYSTEM32", "Browser", "doc",
            "WindowsApps", "Microsoft", *debug], s):
        _ignored.append (s)
        return False
    return True

class Daemon:
    def __init__(self, *args, **kwargs):
        if 'entity' in kwargs:
            self.entity = kwargs['entity']
        if 'listener' in kwargs:
            self.listener = kwargs['listener']
        self.args = args
        self.kwargs = kwargs
        self.ets = []
        self.state = 'continue'
        self.com = kwargs['com']
    def _walk(self, di, d=0):
        ls = globit(di, '*')
        t = '-'
        for _ in range(d):
            t += '\t'
        for l in [ _ for _ in ls if select(_)]:
            p = Path(l)
            try:
                if p.is_dir():
                    if p.is_symlink():
                        #aprint ("PASSED SYMLINK:", p)
                        continue
                    pp = os.path.split(p)[1]
                    self.walk(p, d=d+1)
            except Exception as e: pass
                #aprint ("["+ str(p) +"]Error: ", e)
    def walk(self, di, d=0):
        if '.entity' in str(di) or '.nu' in str(di):
            self.on_entity(di)
            return;
        self._walk(di, d)


    def root(self):
        #aprint ("\n\n__fork__", self.args, self.kwargs)
        if 'win' in self.kwargs.keys():
            di = self.args[0] + ':\\'
        else:
            di = self.args[0]
        di = Path(di).resolve()
        os.chdir(str(di))
        self.walk('.', d=1)
        while True:
            if self.state == 'continue':
                #aprint ("__exit__", self.state, self.args, self.kwargs)
                exit()
            #aprint ("__loop__", self.state, self.args, self.kwargs)
            self.state = "continue"
            #aprint ("\t", self.state, "\n\t", self.ets)
            sys.stdout.flush()
            self.walk('.', d=1)

    def daemonize(self, default='root', args=[]):
        p = mp.Process(target=getattr(self, default) , args=[])
        p.start()
        return p

    def on_entity(self, entity):
        if not entity in self.ets:
            self.ets.append(entity)
            self.state = "nu"
            Daemon(entity=entity, com=self.com).daemonize('entity_daemon')
        sys.stdout.flush()

    def entity_daemon(self):
        #aprint ("\tentity: " + str(self.entity), ' STARTED', os.getcwd())
        di = Path(os.getcwd(), self.entity).resolve()
        os.chdir(str(di))
        (proc, endentity) = entity_script(self.entity, self)
        #aprint ("\tentity: " + str(self.entity), ' EXECUTING\n\t\t', proc)
        proc.wait()
        #aprint ("\tentity: " + str(self.entity), ' EXITED', os.getcwd())
        proc.terminate()
        #aprint(self.entity, " killed ?")
        endentity(self)
        #aprint(self.entity, " pray reach top ?")
        exit()

    def nugod_listener(self):
        #aprint ("HEY I'm the listener !!", self)
        while True:
            r = self.listener.recv()
            #aprint ('listener ==> ', r)
            nu.workship(r)
            #aprint ("workshipped !!")


def cmd(_, args, **kwargs):
    mp.set_start_method('spawn')
    ds = []
    parent_conn, child_conn = mp.Pipe(False)
    dae = Daemon(listener=parent_conn, com=child_conn).daemonize('nugod_listener')
    for l in nu.drives:
        dae = Daemon(l, win=True, com=child_conn)
        ds.append(dae.daemonize())
    exit()