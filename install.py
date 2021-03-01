# assumes this in ~/.vim/VimFiles

import shutil
import glob
import os
def do_it():
    shutil.copy('vimrc', '../.vimrc')
    pyfiles = glob.glob('*.py')
    pyfiles.remove('install.py')
    for f in pyfiles:
        shutil.copy(f, '..')
    os.makedirs('../autoload', exist_ok=True)
    os.makedirs('../plugin', exist_ok=True)
    os.makedirs('../plugged', exist_ok=True)
    os.makedirs('../undo', exist_ok=True)
    os.makedirs('../swap', exist_ok=True)
    shutil.copy('plug.vim', '../autoload/')
    shutil.copy('beffer.vim', '../plugin/')

if __name__ == '__main__':
    do_it()
