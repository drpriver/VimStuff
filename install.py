# assumes this in ~/.vim

import shutil
import glob
shutil.copy('vimrc', '../.vimrc')

pyfiles = glob.glob('*.py')
pyfiles.remove('install.py')
for f in pyfiles:
    shutil.copy(f, '..')

