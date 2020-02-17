python3 << endpy
# To use, add source ~/.vim/fix.py
# Probably other ways to do it, but whatever!
import vim
def get_visual_selection():
    start_pos = vim.eval('getpos("\'<")')
    _, start_line, _, _ = start_pos
    end_pos = vim.eval('getpos("\'>")')
    _, end_line, _, _ = end_pos
    return start_line, end_line

def get_current_lines():
    start_, end_ = get_visual_selection()
    start = int(start_) - 1
    end   = int(end_)
    cb = vim.current.buffer
    lines = cb[start:end]
    return start, end, lines

def get_ft():
    return vim.eval("&ft")
    
def fix_alignment_colon(text):
    colon_alignment = 0
    for t in text:
        head, *tail = t.split(':')
        colon_alignment = max(len(head.rstrip()), colon_alignment)
    new_text = []
    for t in text:
        if ':' not in t:
            new_text.append(t.rstrip())
            continue
        head, *tail = t.split(':')
        new_text.append((head.rstrip().ljust(colon_alignment) + (' : ' + (':'.join(tail)).strip() if tail else '')).rstrip())
    return new_text

def fix_alignment_equals(text):
    equals_alignment = 0
    for t in text:
        head, *tail = t.split('=')
        equals_alignment = max(len(head.rstrip()), equals_alignment)
    new_text = []
    for t in text:
        if '=' not in t:
            new_text.append(t.rstrip())
            continue
        head, *tail = t.split('=')
        new_text.append((head.rstrip().ljust(equals_alignment) + (' = ' + ('='.join(tail)).strip() if tail else '')).rstrip())
    return new_text

def fixed_lines():
    start, end, lines = get_current_lines()
    if ':' in lines[0] and '=' not in lines[0]:
        fixed = fix_alignment_colon(lines)
    elif '=' in lines[0] and ':' not in lines[0]:
        fixed = fix_alignment_equals(lines)
    elif ':' in lines[0] and ':' in lines[0]:
        fixed = fix_alignment_equals(fix_alignment_colon(lines))
    else:
        print("aborted: nothing to format in first line")
        return
    vim.current.buffer[start:end] = fixed

def toggle_comments():
    start, end, lines = get_current_lines()
    ft = get_ft()
    comment_chars = {
        'python'     : '#',
        'c'          : '//',
        'dave'       : '#',
        'sh'         : '#',
        'cpp'        : '//',
        'd'          : '//',
        'js'         : '//',
        'javascript' : '//',
        'vim'        : '"',
        'text'       : '#',
        'taxonomy'   : '#',
        'dnd'        : '#',

    }
    chars = comment_chars.get(ft)
    if chars is None:
        print(f"Aborted: unhandled ft: {ft}")
        return
    else:
        fixed = _toggle_comments(lines, chars)
    vim.current.buffer[start:end] = fixed

def _toggle_comments(lines, comment_chars):
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(comment_chars):
            comment = True
        else:
            comment = False
        break
    else:
        return lines

    if comment: # decomment the lines
        for line in lines:
            stripped = line.lstrip()
            if not stripped:
                new_lines.append(line)
            elif not stripped.startswith(comment_chars):
                new_lines.append(line)
            else:
                pos = line.find(comment_chars)
                new_lines.append(line[:pos]+line[pos+len(comment_chars):].strip())
        return new_lines
    else: # comment the lines
        for line in lines:
            stripped = line.lstrip()
            if not stripped:
                new_lines.append(line)
            elif stripped.startswith(comment_chars):
                new_lines.append(line)
            else:
                new_lines.append(' '* (len(line) - len(stripped)) + comment_chars + ' ' + stripped)
        return new_lines

def toggle_c_comments(lines):
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('//'):
            comment = True
        else:
            comment = False
        break
    else:
        return lines

    if comment: # decomment the lines
        for line in lines:
            stripped = line.lstrip()
            if not stripped:
                new_lines.append(line)
            elif not stripped.startswith('//'):
                new_lines.append(line)
            else:
                pos = line.find('//')
                new_lines.append(line[:pos]+line[pos+2:].strip())
        return new_lines
    else: # comment the lines
        for line in lines:
            stripped = line.lstrip()
            if not stripped:
                new_lines.append(line)
            elif stripped.startswith('//'):
                new_lines.append(line)
            else:
                new_lines.append(' '* (len(line) - len(stripped)) + '// ' + stripped)
        return new_lines

def toggle_py_comments(lines):
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#'):
            comment = True
        else:
            comment = False
        break
    else:
        return lines

    if comment: # decomment the lines
        for line in lines:
            stripped = line.lstrip()
            if not stripped:
                new_lines.append(line)
            elif not stripped.startswith('#'):
                new_lines.append(line)
            else:
                pos = line.find('#')
                new_lines.append(line[:pos]+line[pos+1:].strip())
        return new_lines
    else: # comment the lines
        for line in lines:
            stripped = line.lstrip()
            if not stripped:
                new_lines.append(line)
            elif stripped.startswith('#'):
                new_lines.append(line)
            else:
                new_lines.append(' '* (len(line) - len(stripped)) + '# ' + stripped)
        return new_lines

endpy
vmap <leader>e :python3 fixed_lines()<CR>
vmap <CR> :python3 toggle_comments()<CR>
