python3 << endpy
# this plugin is janky, but good enough!
import os
import vim
import typing as t
import io
import builtins
import string
class Logger:
    def __init__(self, o):
        if o:
            self.out = open(os.path.expanduser(o), 'w')
            self('Log opened!')
        else:
            self.out = None
    def __call__(self, *args, **kwargs):
        if self.out is not None:
            print(*args, **kwargs, file=self.out)
            self.out.flush()
logger = Logger(None)

class Writer:
    def __init__(self) -> None:
        self.buf = io.StringIO()
        self.wrote = False
    def __call__(self, s:str) -> None:
        if self.wrote:
            self.buf.write('.')
        self.buf.write(s)
        self.wrote = True
    def get(self) -> str:
        return self.buf.getvalue()

class Imported(t.NamedTuple):
    path: str
    name: str

def _parse(s:str, result:t.Dict[str, Imported]) -> None:
    if 'import' not in s:
        return
    s = s.replace(',', '')
    toks = s.strip().split()
    w = Writer()
    if not toks:
        return
    if toks[0] == 'from':
        logger(toks)
        tok_iter = iter(toks)
        next(tok_iter)
        main_mod = next(tok_iter)
        w(main_mod)
        should_be_import = next(tok_iter, None)
        if should_be_import is None:
            return
        if should_be_import != 'import':
            return
        target = next(tok_iter)
        while True:
            might_be_as = next(tok_iter, None)
            if might_be_as is None:
                w(target)
                result[target] = Imported(w.get(), target)
                return
            elif might_be_as == 'as':
                w(target)
                break
            else:
                result[might_be_as] = Imported(w.get()+'.'+might_be_as, might_be_as)
        # post-as
        name = next(tok_iter)
        return Imported(w.get(), name)
    elif toks[0] == 'import':
        tok_iter = iter(toks)
        next(tok_iter)
        main_mod = next(tok_iter)
        might_be_as = next(tok_iter, None)
        if might_be_as is None:
            result[main_mod] =  Imported(main_mod, main_mod)
        elif might_be_as == 'as':
            pass
        else:
            return
        name = next(tok_iter)
        result[name] = Imported(main_mod, name)
    else:
        return

def parse(s:str, result:dict) -> None:
    try:
        _parse(s, result)
    except:
        return

def cursor_position():
    out = vim.eval('getcurpos()')
    return out

def parse_imports() -> t.Dict[str, Imported]:
    cb = vim.current.buffer
    logger(cb.name)
    # just look at the first 50 lines
    first50 = cb[:50]
    result = {}
    for line in first50:
        parse(line, result)
    return result

def get_token(line:str, col:int) -> str:
    identchars = {*string.ascii_letters, *string.digits, *'_.'}
    ident = ''
    for char in line[col:]:
        if char in identchars:
            ident += char
        else:
            break
    for char in line[col-1::-1]:
        if char in identchars:
            ident = char + ident
        else:
            break
    return ident

def get_py_help():
    imports = parse_imports()
    _, lnum_s, col_s, _, _ = cursor_position()
    lnum = int(lnum_s)-1
    col = int(col_s)
    cb = vim.current.buffer
    line = cb[lnum]
    tok = get_token(line, col)
    cmd = None
    if tok in imports:
        im = imports[tok]
        cmd = 'vert term ++close pydoc3 {}'.format(im.path)
    else:
        if '.' in tok:
            first, *last = tok.split('.')
            last = '.'.join(last)
            if first in imports:
                fullpath = imports[first].path + '.' + last
                cmd = 'vert term ++close pydoc3 {}'.format(fullpath)
            elif first in dir(builtins):
                cmd = 'vert term ++close pydoc3 {}'.format(tok)
        elif tok in dir(builtins):
            cmd = 'vert term ++close pydoc3 {}'.format(tok)
        else:
            # try in local file?
            relfilename = os.path.relpath(cb.name)
            if not '..' in relfilename:
                filename = relfilename[:-3]
                logger(filename)
                tokpath = '{}.{}'.format(filename.replace('/', '.'), tok).replace(' ', r'\ ')
                logger(tokpath)
                cmd = 'vert term ++close pydoc3 {}'.format(tokpath)
                logger(cmd)

    if cmd is None:
        logger("Couldn't figure out:", tok)
        print("Couldn't get help for:", tok)
    else:
        vim.command(cmd)

endpy
