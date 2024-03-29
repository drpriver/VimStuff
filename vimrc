set undofile
set undodir=$HOME/.vim/undo
set undolevels=1000
set undoreload=10000 
set directory^=$HOME/.vim/swap//
set splitright
set splitbelow
set shortmess+=I
set backspace=indent,eol,start
set nu
set linebreak
set wrap
set path-=/usr/include
set path+=**
set wildmenu
set wildignore=*.pyc
set wildignore+=**/Bin/**
set wildignore+=**/*.dSYM/**
set wildignore+=**/DWARF/**
set wildignore+=*.png
set wildignore+=*.jpg
set wildignore+=*.pdf
set wildignore+=*.so
set wildignore+=*.dylib
set wildignore+=*.o
set wildignore+=*.exe
set wildignore+=*.lib
set wildignore+=*.dll
set wildignore+=*.egg-info
set noshowcmd
set autoread
set autoindent
set mouse=a
set foldcolumn=0
set smartindent
set foldtext=getline(v:foldstart)
set fillchars=fold:\ 
set breakindent
set showbreak=\ \ 
set breakat=\ 
set hidden
set diffopt+=iwhite
set completeopt=longest,menuone
set signcolumn=number
set foldignore=
set background=dark
set incsearch
set hlsearch
command! -nargs=+ -complete=file Grep execute 'silent grep! <args>' | redraw! | cfirst
filetype plugin on
syntax on
runtime ftplugin/man.vim

command W w
command Q q

nnoremap <silent> j gj
nnoremap k gk
nnoremap ; :
nnoremap <bs> <c-^>
nnoremap <Space> za
nnoremap <S-Space> zA
" nnoremap , :<C-U>marks<CR>:normal! '
nnoremap <leader>p :Nuake<CR>
nnoremap <leader><Tab> gt
nnoremap <leader><S-Tab> gT
nnoremap <leader>w <c-w><c-w>
nnoremap <silent> <leader>] :vert term<CR>
nnoremap <silent> <leader>s :silent! syntax<space>sync<space>fromstart<CR>:silent! redraw!<CR>:silent! nohlsearch<CR>
nnoremap g* :execute "Grep -w " . expand("<cword>") <CR>
nnoremap <leader>r :%s/\s\+$//g<cr>:silent! syntax<space>sync<space>fromstart<CR>:silent! redraw!<CR>:silent! nohlsearch<CR>


nmap <leader>c <Plug>SlimeParagraphSend
nnoremap <C-Right> :cn<CR>
nnoremap <C-Left> :cp<CR>

tnoremap <leader>p <C-\><C-n>:Nuake<CR>
tnoremap <leader>w <c-w><c-w>
tnoremap <leader><tab> <c-w>:tabnext<cr>

inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"
inoremap <expr> j pumvisible() ? "\<Down>" : "j"
inoremap <expr> k pumvisible() ? "\<Up>" : "k"
inoremap <expr> <C-n> pumvisible() ? '<C-n>' : '<C-n><C-r>=pumvisible() ? "\<lt>Down>" : ""<CR>'

xmap <leader>c <Plug>SlimeRegionSend


au BufNewFile,BufReadPost *.h set filetype=c
au BufNewFile,BufReadPost *.m set filetype=objc
au BufNewFile,BufReadPost *.m setlocal et sw=4 ts=4 sts=4
au BufNewFile,BufReadPost *.fish set filetype=fish
au FileType fish setlocal sw=4 ts=4 sts=4 et
au BufNewFile,BufReadPost *.md set filetype=markdown
au BufNewFile,BufReadPost *.dnd set filetype=dnd
au BufNewFile,BufReadPost *.tql set filetype=taxonomy
au BufNewFile,BufReadPost *.dep set filetype=make
au FileType taxonomy setlocal et sw=4 ts=4 sts=4
au FileType markdown setlocal foldexpr=MarkdownLevel() foldmethod=expr ts=2 et
au FileType d setlocal formatoptions+=orj
au BufEnter *.py setlocal kp=:python3\ parse_import.get_py_help()\ #
" au BufEnter *.py setlocal kp=:tab\ term\ ++close\ pydoc3
au BufEnter *.py setlocal makeprg=mypy\ .
au BufEnter *.txt setlocal tabstop=4
if &diff
    " au BufEnter *.c,*.d,*.cpp,*.h,*.js,*.py setlocal foldmethod=diff
else
    au BufEnter *.c,*.d,*.cpp,*.h,*.js,*.py,*.m,*.mm,*.ts setlocal foldmethod=indent
endif
au BufEnter *.c,*.d,*.cpp,*.h,*.js,*.py,*.m,*.ts setlocal cinkeys-=:
au BufEnter *.js setlocal sts=4 ts=4 sw=4 et
au BufEnter *.c,*.d,*.cpp,*.h,*.hpp,*.m,*.ts setlocal ts=4 sw=4 sts=4 et
au BufEnter *.ts setlocal errorformat=%+A\ %#%f\ %#(%l\\\,%c):\ %m,%C%m
au BufEnter *.c,*.cpp,*.h,*.hpp setlocal cindent
au BufEnter *.c,*.cpp,*.h,*.hpp setlocal cindent cino=l1,L0
au BufEnter *.c,*.h syn keyword cStatement assert
au BufEnter *.c,*.h syn keyword cType Nonnull Nullable warn_unused NullUnspec force_inline
au BufEnter *.vim,*.vimrc setlocal ts=4 sw=4 sts=4 et
au BufEnter *.py syn keyword pythonBuiltin List Iterable Optional Tuple Type Dict Set Union NamedTuple

hi FoldColumn ctermbg=none ctermfg=0 guibg=bg
hi LineNr ctermfg=239
hi String ctermfg=1
" hi String cterm=italic ctermfg=1
hi Folded ctermfg=35 ctermbg=none guibg=bg guifg=darkgray
hi Folded ctermfg=1
hi SignColumn ctermbg=0
hi TabLine ctermfg=Green
hi TabLine ctermbg=Black
hi TabLineSel cterm=underline
hi TabLineFill ctermfg=Black
hi StatusLine cterm=none ctermfg=14 ctermbg=0
hi StatusLineNC ctermfg=6 ctermbg=0 cterm=none
hi VertSplit cterm=bold ctermfg=0
hi TabLine cterm=none
hi TabLine ctermfg=none
hi TabLine ctermbg=none
hi TabLineFill ctermfg=none
hi TabLineFill cterm=none
hi TermLineNc ctermbg=0
hi TermLine ctermbg=0
hi StatusLineTermNc ctermbg=0
hi StatusLineTerm ctermbg=0
hi EndOfBuffer ctermfg=0
hi Search ctermbg=16 ctermfg=12
hi PMenu ctermbg=0 ctermfg=none

let g:python_no_builtin_highlight=1

let g:netrw_liststyle=3
let g:netrw_banner=0

let c_no_curly_error = 1

let g:slime_target = "vimterminal"
let g:slime_vimterminal_cmd = "python3"

set tabline=%!MyTabLine()  " custom tab pages line
function! MyTabLine()
  let s = ''
  " loop through each tab page
  for i in range(tabpagenr('$'))
    if i + 1 == tabpagenr()
      let s .= '%#TabLineSel#'
    else
      let s .= '%#TabLine#'
    endif
    if i + 1 == tabpagenr()
      let s .= '%#TabLineSel#' " WildMenu
    else
      let s .= '%#Title#'
    endif
    " set the tab page number (for mouse clicks)
    let s .= '%' . (i + 1) . 'T '
    " set page number string
    let s .= i + 1 . ''
    " get buffer names and statuses
    let n = ''  " temp str for buf names
    let m = 0   " &modified counter
    let buflist = tabpagebuflist(i + 1)
    " loop through each buffer in a tab
    for b in buflist
      if getbufvar(b, "&buftype") == 'help'
        " let n .= '[H]' . fnamemodify(bufname(b), ':t:s/.txt$//')
      elseif getbufvar(b, "&buftype") == 'quickfix'
        " let n .= '[Q]'
      elseif getbufvar(b, "&modifiable")
        let n .= fnamemodify(bufname(b), ':t') . ', ' " pathshorten(bufname(b))
      endif
      if getbufvar(b, "&modified")
        let m += 1
      endif
    endfor
    " let n .= fnamemodify(bufname(buflist[tabpagewinnr(i + 1) - 1]), ':t')
    let n = substitute(n, ', $', '', '')
    " add modified label
    if m > 0
      let s .= '+'
      " let s .= '[' . m . '+]'
    endif
    if i + 1 == tabpagenr()
      let s .= ' %#TabLineSel#'
    else
      let s .= ' %#TabLine#'
    endif
    " add buffer names
    if n == ''
      let s.= '[New]'
    else
      let s .= n
    endif
    " switch to no underlining and add final space
    let s .= ' '
  endfor
  let s .= '%#TabLineFill#%T'
  return s
endfunction

function! MarkdownLevel()
  let h = matchstr(getline(v:lnum), '^\s*#\+') 
  if empty(h)
    return "="
  else 
    return ">" . len(h)
  endif
endfunction

" Python modules
python3 << endpy
import sys
import os
sys.path.append(os.path.expanduser('~/.vim'))
import fix
import parse_import
import dnd_outline
import debug
endpy


vmap <leader>e :python3 fix.fixed_lines()<CR>
vmap <CR> :python3 fix.toggle_comments()<CR>
vmap <leader><CR> :python3 fix.css_toggle_comments()<CR>
function! g:DndOutLineGoToNode()
    :python3 dnd_outline.current_outline.select()
endfunction

" [o]utline is the mnemonic
nnoremap <leader>o :python3 dnd_outline.toggle()<CR>

function MyFilter(winid, key)
    if mode()[0] == 'c'
        return 0
    endif
    if a:key=="\<ESC>" || a:key == "x" || a:key == "q"
        if mode()[0] != 'i'
            call popup_close(a:winid, 0)
            return 1
        endif
    endif
    if a:key=="\<C-C>"
        call popup_close(a:winid, 0)
        return 1
    endif
    if a:key == "\<down>"
        let l:info = popup_getpos(a:winid)
        call popup_setoptions(a:winid, {'firstline':l:info['firstline']+1})
        return 1
    endif
    if a:key == "\<up>"
        let l:info = popup_getpos(a:winid)
        call popup_setoptions(a:winid, {'firstline':l:info['firstline']-1})
        return 1
    endif
    return 0
endfunction

let s:line_num=0
function Unclose(winid, result)
    if a:result==-1
        let l:info = popup_getpos(a:winid)
        let s:line_num = l:info['firstline']
        call HtagFunc(g:name, s:line_num)
        return
    endif
    let s:line_num=0
endfunction
    
let s:w = 0
function g:HtagFunc(name, l)
    " this is so effing janky
    let g:name = a:name
    let l:tl = taglist(a:name)
    let l:t = l:tl[0]
    let l:buf = bufadd(l:t['filename'])
    if a:l
        let l:l = a:l
        let s:line_num=l:l
    else
        let l:cur_l = line(".")
        let l:cur = bufnr("%")
        call execute('buffer ' . l:buf)
        let l:cmd = strpart(l:t['cmd'], 2)
        let l:cmd = substitute(l:cmd, "\\$", "", "")
        let l:cmd = '/\V' .  l:cmd
        call execute(l:cmd)
        let l:l = line(".")-2
        call execute('buffer ' . l:cur)
        call execute(':' . l:cur_l)
        let s:line_num=l:l
    endif
    let l:opts = {'moved':[0,999], 'maxheight':10,'minwidth':100, 'wrap':'FALSE', 'firstline': l:l, 'callback': 'Unclose', 'filter': 'MyFilter', 'border':[1,1,1,1]}
    let s:w = popup_atcursor(l:buf, l:opts)
    return 0
endfunction

command! -nargs=1 -complete=tag Htag :call HtagFunc(<f-args>, 0)
nnoremap <C-H> :execute "Htag " . expand("<cword>") <CR>
if filereadable(".vimrc")
    if expand('~') != getcwd()
        source ./.vimrc
    endif
endif
command! CdGit :exec 'cd' fnameescape(fnamemodify(finddir('.git',escape(expand('%:p:h'), ' ') . ';'), ':h'))

"Plugins
call plug#begin('~/.vim/plugged')

Plug 'ycm-core/YouCompleteMe', { 'do': './install.py --clang-completer' }
" I couldn't get this to work on macos (would timeout on launch of program)
" It's not that big a deal anyway, I can just use xcode
" Plug 'puremourning/vimspector', {'do': './install_gadget.py --enable-python'}

" Initialize plugin system
Plug 'ziglang/zig.vim'
if has('macunix')
    Plug 'rizzatti/dash.vim'
endif

call plug#end()

"YouCompleteMe junk
let g:ycm_disable_signature_help=1
let g:ycm_auto_hover=''
let g:ycm_auto_trigger=0
let g:ycm_open_loclist_on_ycm_diags=0
let g:ycm_show_diagnostics_ui=0
let g:ycm_key_list_select_completion = ['<TAB>', '<Down>']
let g:ycm_key_list_stop_completion = ['<C-y>', '<CR>']
let g:ycm_min_num_of_chars_for_completion=8
let g:ycm_global_ycm_extra_conf='/Users/drpriver/.vim/ycm_extra.py'
let g:ycm_clangd_args=['--header-insertion=never']
let g:ycm_disable_for_files_larger_than_kb=8000

nnoremap <silent> <c-\> :YcmCompleter GoTo<CR>:silent! foldo!<CR>:silent! redraw!<CR>
nnoremap <silent> <leader>a :YcmCompleter GoToAlternateFile<CR>
nnoremap <silent> <leader>d :YcmCompleter GoToDefinition<CR>:silent! foldo!<CR>:silent! redraw!<CR>
nmap <leader>q <plug>(YCMHover)

function g:Novel()
    set bg=light
    hi PMenu ctermbg=15
    hi Search ctermbg=3
    hi StatusLine ctermfg=0 ctermbg=none cterm=italic
    hi StatusLineNC ctermfg=0 ctermbg=none cterm=none
    hi TermLine ctermbg=none ctermfg=0
    hi TermLineNc ctermbg=none ctermfg=0 cterm=italic
    hi StatusLineTermNc ctermbg=none
    hi StatusLineTerm ctermbg=none
    hi PreProc ctermfg=91
    hi CPreProc ctermfg=91
    hi cFunction ctermfg=124
    hi Comment ctermfg=0 cterm=italic
    hi Statement ctermfg=0
    hi Identifier ctermfg=27
    hi Type ctermfg=27
    return 0
endfunction

function g:Dark()
    set bg=dark
    hi PMenu ctermbg=0 ctermfg=none
    hi Search ctermbg=16 ctermfg=12
    hi StatusLine cterm=none ctermfg=14 ctermbg=0
    hi StatusLineNC ctermfg=6 ctermbg=0 cterm=none
    return 0
endfunction

if $LIGHTMODE == "1"
    call Novel()
else
    call Dark()
end
let &t_SI = "\<Esc>[6 q"
let &t_SR = "\<Esc>[4 q"
let &t_EI = "\<Esc>[2 q"
let g:vim_json_warnings = 0

let g:netrw_silent = 1

function g:Tapi_open(_, arglist)
    let l:current_win = win_getid()
    python3 debug.set_dbg()
    exe "1wincmd w"
    exe "silent! edit " . a:arglist[0]
    exe "silent! " . a:arglist[1]
    setlocal cursorline
    setlocal cursorlineopt=number
    normal! zR
    normal! zz
    call win_gotoid(l:current_win)
endfunction
