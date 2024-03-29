import vim
from typing import List, NamedTuple
class VisSelection(NamedTuple):
    start_line: int
    end_line: int

def get_visual_selection() -> VisSelection:
    start_pos = vim.eval('getpos("\'<")')
    _, start_line, _, _ = start_pos
    end_pos = vim.eval('getpos("\'>")')
    _, end_line, _, _ = end_pos
    return VisSelection(int(start_line)-1, int(end_line))

class CurrentLines(NamedTuple):
    start:int
    end: int
    lines: List[str]

def get_current_lines() -> CurrentLines:
    start, end = get_visual_selection()
    cb = vim.current.buffer
    lines = cb[start:end]
    return CurrentLines(start, end, lines)

def get_ft() -> str:
    return vim.eval("&ft")
    
def fix_alignment_char(text:List[str], char:str) -> List[str]:
    if char == '|':
        return fix_alignment_all_char(text, char)
    equals_alignment = 0
    for t in text:
        head, *tail = t.split(char)
        equals_alignment = max(len(head.rstrip()), equals_alignment)
    new_text = []
    for t in text:
        if char not in t:
            new_text.append(t.rstrip())
            continue
        head, *tail = t.split(char)
        if char == ':':
            if tail:
                h = (head.rstrip() + ':').ljust(equals_alignment+1)
            else:
                h = head.rstrip()
            h += ' '
        else:
            if tail:
                h = head.rstrip().ljust(equals_alignment) + ' ' + char
            else:
                h = head.rstrip()
            h += ' '
        new_text.append((h + char.join(tail).strip()).rstrip())
    return new_text

def fix_alignment_all_char(text:List[str], char:str) -> List[str]:
    import io
    most = 0
    for t in text:
        most = max(t.count(char), most)
    widths = [0 for _ in range(most+1)]
    for t in text:
        if char not in t:
            continue
        split = t.split(char)
        for i, s in enumerate(split):
            if i == 0:
                l = len(s.rstrip())
            else:
                l = len(s.strip())
            widths[i] = max(widths[i], l)
    new_text = []
    for t in text:
        if char not in t:
            new_text.append(t.rstrip())
            continue
        splits = t.split(char)
        buf = io.StringIO()
        for i, s in enumerate(splits):
            if i == 0:
                buf.write(s.rstrip().ljust(widths[i]))
                continue
            buf.write(' ')
            buf.write(char)
            buf.write(' ')
            buf.write(s.strip().ljust(widths[i]))
        new_text.append(buf.getvalue().rstrip())
        buf.close()
    return new_text
    

def fixed_lines() -> None:
    start, end, lines = get_current_lines()
    chars = [':', '=', '|']
    in_line = []
    for char in chars:
        if char in lines[0]:
            in_line.append(char)
    if not in_line:
        print("aborted: nothing to format in first line")
        return
    for char in in_line:
        fixed = fix_alignment_char(lines, char)
    vim.current.buffer[start:end] = fixed

def toggle_comments() -> None:
    ft = get_ft()
    if ft == 'css': return css_toggle_comments()
    start, end, lines = get_current_lines()
    comment_chars = {
        'python'     : '#',
        'c'          : '//',
        'dave'       : '#',
        'sh'         : '#',
        'fish'       : '#',
        'cpp'        : '//',
        'd'          : '//',
        'js'         : '//',
        'javascript' : '//',
        'vim'        : '"',
        'objc'       : '//',
        'rust'       : '//',
        'typescript' : '//',
        'ds'         : '//',
    }
    chars = comment_chars.get(ft, '#')
    if chars is None:
        print(f"Aborted: unhandled ft: {ft}")
        return
    else:
        fixed = _toggle_comments(lines, chars)
    vim.current.buffer[start:end] = fixed

def _toggle_comments(lines:List[str], comment_chars:str) -> List[str]:
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

def css_toggle_comments() -> None:
    start, end, lines = get_current_lines()
    fixed = []
    for line in lines:
        if '/*' in line:
            fixed.append(line.replace('/*', '').replace('*/',''))
        else:
            l = line.lstrip()
            fixed.append(' '*(len(line)-len(l)) + '/*' + l + '*/')
    vim.current.buffer[start:end] = fixed
