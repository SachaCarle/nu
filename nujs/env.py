import sys, os, subprocess, nu, json
from pathlib import Path

class ExecuteJs:
    def __init__(self, code=None, fd=None, stdin=None, stdout=False):
        assert code != None or fd != None
        assert code == None or fd == None
        self.state = None

        e_code = """console.log('hello there', __dirname)
        process.stdin.setEncoding('utf8');
        function listener(fun) {
            fun()
        }
        fun = require('./execute_nujs')
        var stat = false
        process.stdin.on('readable', () => {
            if (stat == false) {
                console.log("__START__")
                stat = true
            } else {
                console.log("__NEXT__")
            }

            var chunk = process.stdin.read()
            var res = fun(chunk)
        })
        process.stdin.on("end", () => {
            console.log("__END__")

        })

        """

        #sub = nu.nupath
        sub = Path('.').resolve()

        ecma5 = Path(os.path.join(sub, '__execute__.js'))
        if not ecma5.exists():
            with ecma5.open('w') as js:
                js.write(e_code)


        exe = Path(os.path.join(sub, 'execute_nujs.js'))

        if exe.exists():
                os.remove(exe)
        if fd:
            with exe.open('w') as js:
                js.write(Path(fd).resolve().read_text())
        elif code:
            if exe.exists():
                os.remove(exe)
            with exe.open('w') as js:
                js.write(code)
        else:
            raise Exception('No param for ExecuteJs')


        #print ("!!\t\t", str(ecma5.resolve()), exe)
        if not stdout:
            self.state = subprocess.Popen(["node", str(ecma5.resolve())], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            self.state = subprocess.Popen(["node", str(ecma5.resolve())], stdin=subprocess.PIPE)
        if stdin:
            self.res = self.state.communicate(input=stdin)
        else:
            self.res = self.state.communicate()
        self.body = self.res[0]

        try:
            if stdout:
                result = '{}'
            result = self.res[0].split(b'__START__')[1].split(b'__END__')[0]
            result = result.split(b'__NEXT__')
            self.body = result
            self.result = [json.loads(it) for it in result if it not in [
                b'\n'
            ]]
        except Exception as e:
            self.result = e

        os.remove(exe)
        os.remove(ecma5)