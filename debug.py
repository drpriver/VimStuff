from __future__ import annotations
import vim
import os
import re
from typing import NamedTuple

class Location(NamedTuple):
    linenumber: int
    filename: str

def get_current_location() -> Location:
    cb = vim.current.buffer
    cw = vim.current.window
    pos = cw.cursor
    name = cb.name
    try:
        rname = os.path.relpath(name)
    except:
        pass
    else:
        if '..' not in rname:
            name = rname
    return Location(pos[0], name)

def get_visual_selection() -> str:
    start_pos = vim.eval('getpos("\'<")')
    _, start_line, start_col, _ = start_pos
    end_pos = vim.eval('getpos("\'>")')
    _, end_line, end_col, _ = end_pos
    cb = vim.current.buffer
    start = int(start_line)-1
    end = int(end_line)
    txt = cb[start:end]
    if end - start == 1:
        return txt[0][int(start_col)-1:int(end_col)]
    begin = txt[0][int(start_col)-1:]
    ending = txt[-1][:int(end_col)]
    if len(txt) > 2:
        mid = '\n'.join(txt[1:-2])
    else:
        mid = ''
    return begin + ' ' + mid + ' ' + ending

class DebugState:
    def __init__(self, bufid:int) -> None:
        self.bufid = bufid
        self.dbg_line_buf: int|None = None
        self.dbg_line: int|None = None

    def set_breakpoint(self) -> None:
        loc = get_current_location()
        if vim.eval('&ft') == 'python':
            cmd = f'call term_sendkeys({self.bufid}, "break {loc.filename}:{loc.linenumber}\\<Enter>")'
        else:
            cmd = f'call term_sendkeys({self.bufid}, "break set -f {loc.filename} -l {loc.linenumber}\\<Enter>")'
        vim.command(cmd)

    def run_to(self) -> None:
        loc = get_current_location()
        if vim.eval('&ft') == 'python':
            cmd = f'call term_sendkeys({self.bufid}, "tbreak {loc.filename}:{loc.linenumber}\\<Enter>c\\<Enter>")'
        else:
            cmd = f'call term_sendkeys({self.bufid}, "break set -o true -f {loc.filename} -l {loc.linenumber}\\<Enter>c\\<Enter>")'
        vim.command(cmd)

    def print_ident(self) -> None:
        cword = vim.eval("expand('<cword>')")
        if vim.eval('&ft') == 'python':
            cmd = f'call term_sendkeys({self.bufid}, "pp {cword}\\<Enter>")'
        else:
            cmd = f'call term_sendkeys({self.bufid}, "p {cword}\\<Enter>")'
        vim.command(cmd)

    def print_selection(self) -> None:
        sel = get_visual_selection()
        if vim.eval('&ft') == 'python':
            cmd = f'call term_sendkeys({self.bufid}, "pp {sel}\\<Enter>")'
        else:
            cmd = f'call term_sendkeys({self.bufid}, "p {sel}\\<Enter>")'
        vim.command(cmd)

    def next(self) -> None:
        cmd = f'call term_sendkeys({self.bufid}, "n\\<Enter>")'
        vim.command(cmd)
        if vim.eval('&ft') == 'python':
            self._recenter()
    def up(self) -> None:
        cmd = f'call term_sendkeys({self.bufid}, "up\\<Enter>")'
        vim.command(cmd)
        self._recenter()
    def _recenter(self) -> None:
        cmd = f'call term_sendkeys({self.bufid}, "rc\\<Enter>")'
        vim.command(cmd)
    def down(self) -> None:
        cmd = f'call term_sendkeys({self.bufid}, "down\\<Enter>")'
        # print(cmd)
        vim.command(cmd)
        self._recenter()
    def run(self) -> None:
        cmd = f'call term_sendkeys({self.bufid}, "run\\<Enter>")'
        vim.command(cmd)
    def cont(self) -> None:
        cmd = f'call term_sendkeys({self.bufid}, "c\\<Enter>")'
        vim.command(cmd)
        if vim.eval('&ft') == 'python':
            self._recenter()
    def step(self) -> None:
        cmd = f'call term_sendkeys({self.bufid}, "s\\<Enter>")'
        vim.command(cmd)
        if vim.eval('&ft') == 'python':
            self._recenter()
    def stepout(self) -> None:
        if vim.eval('&ft') == 'python':
            cmd = f'call term_sendkeys({self.bufid}, "return\\<Enter>")'
        else:
            cmd = f'call term_sendkeys({self.bufid}, "thread step-out\\<Enter>")'
        vim.command(cmd)
        if vim.eval('&ft') == 'python':
            self._recenter()
    def trace(self) -> None:
        cmd = f'call term_sendkeys({self.bufid}, "bt\\<Enter>")'
        vim.command(cmd)

    def quit(self) -> None:
        if vim.eval('&ft') == 'python':
            cmd = f'call term_sendkeys({self.bufid}, "die\\<Enter>")'
        else:
            cmd = f'call term_sendkeys({self.bufid}, "q\\<Enter>\\<Enter>")'
        vim.command(cmd)
        self.remove_dbgline()

    def remove_dbgline(self) -> None:
        if self.dbg_line is None:
            return
        cmd = f"call prop_remove({{'type':'dbgline', 'bufnr':{self.dbg_line_buf}}}, {self.dbg_line}, {self.dbg_line})"
        vim.command(cmd)
        self.dbg_line = None
        self.dbg_line_buf = None

    def set_dbgline(self) -> None:
        cb = vim.current.buffer
        cw = vim.current.window
        pos = cw.cursor
        line = pos[0]
        self.dbg_line = line
        self.dbg_line_buf = cb.number
        cmd=f"call prop_add({line}, 1, {{'type':'dbgline', 'length':8}})"
        # print(cmd)
        vim.command(cmd)




state = None

def set_dbg() -> None:
    global state
    if state:
        state.remove_dbgline()
        return
    setup_mappings()
    state = DebugState(vim.current.buffer.number)

def set_dbgline() -> None:
    if not state: return
    state.set_dbgline()

def setup_mappings() -> None:
    vim.command('nnoremap <silent> a :python3 debug.set_breakpoint()<CR>')
    vim.command("nnoremap <silent> n :python3 debug.next()<CR>")
    vim.command("nnoremap <silent> <cr> :python3 debug.run_to()<CR>")
    vim.command("nnoremap <silent> p :python3 debug.print_ident()<CR>")
    vim.command("vnoremap <silent> p :python3 debug.print_selection()<CR>")
    vim.command("nnoremap <silent> i :python3 debug.print_ident()<CR>")
    vim.command("vnoremap <silent> i :python3 debug.print_selection()<CR>")
    vim.command("nnoremap <silent> u :python3 debug.up()<CR>")
    vim.command("nnoremap <silent> <nowait> d :python3 debug.down()<CR>")
    vim.command("nnoremap <silent> s :python3 debug.step()<CR>")
    vim.command("nnoremap <silent> q :python3 debug.close()<CR>")
    vim.command("nnoremap <silent> r :python3 debug.run()<CR>")
    vim.command("nnoremap <silent> c :python3 debug.cont()<CR>")
    vim.command("nnoremap <silent> o :python3 debug.stepout()<CR>")
    vim.command("nnoremap <silent> t :python3 debug.trace()<CR>")
    vim.command("nnoremap <silent> <nowait> <2-leftmouse> :python3 debug.print_ident()<CR>")
    vim.command("nnoremap <esc> :python3 debug.remove_mappings()<CR>")
    if state:
        vim.command("nunmap <leader>b")

def remove_mappings() -> None:
    vim.command("nunmap a")
    vim.command("nunmap n")
    vim.command("nunmap <cr>")
    vim.command("nunmap p")
    vim.command("vunmap p")
    vim.command("nunmap i")
    vim.command("vunmap i")
    vim.command("nunmap u")
    vim.command("nunmap d")
    vim.command("nunmap s")
    vim.command("nunmap q")
    vim.command("nunmap r")
    vim.command("nunmap c")
    vim.command("nunmap o")
    vim.command("nunmap t")
    vim.command("nunmap <2-leftmouse>")
    vim.command("set nocursorline")
    vim.command("nunmap <esc>")
    if state:
        vim.command("nnoremap <leader>b :python3 debug.setup_mappings()<CR>")

def close() -> None:
    global state
    if not state: return
    state.quit()
    state = None
    remove_mappings()

def set_breakpoint() -> None:
    if not state: return
    state.set_breakpoint()

def run_to() -> None:
    if not state: return
    state.run_to()

def print_selection() -> None:
    if not state: return
    state.print_selection()

def print_ident() -> None:
    if not state: return
    state.print_ident()

def next() -> None:
    if not state: return
    state.next()

def up() -> None:
    if not state: return
    state.up()

def down() -> None:
    if not state: return
    state.down()

def step() -> None:
    if not state: return
    state.step()

def run() -> None:
    if not state: return
    state.run()

def cont() -> None:
    if not state: return
    state.cont()


def stepout() -> None:
    if not state: return
    state.stepout()

def trace() -> None:
    if not state: return
    state.trace()

vim.command('hi DBGLINE term=underline cterm=underline gui=underline')
vim.command("call prop_type_add('dbgline', {'combine':v:true, 'highlight':'DBGLINE'})")


# add to your vimrc
r'''
python3 << endpy
import sys
import os
sys.path.append(os.path.expanduser('~/.vim'))
import debug
endpy

nnoremap <leader>b :python3 debug.set_breakpoint()<CR>
'''



