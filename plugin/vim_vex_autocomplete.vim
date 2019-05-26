function! ExpandVexSignature(completion)
pythonx << EOF
from vim_vex_autocomplete import autocomplete
from UltiSnips import snippet_manager
import vim

completion = vim.eval('a:completion')
text = autocomplete.get_snippet(completion)

if text:
    autocomplete.clear(len(completion['word']))
    snippet_manager.UltiSnips_Manager.expand_anon(text)
    vim.command('redraw!')
EOF
endfunction

autocmd! CompleteDone *.vex :call ExpandVexSignature(v:completed_item)

let s:current_directory = expand('<sfile>:p:h')
execute ':set tags+=' . fnamemodify(s:current_directory, ':h') . '/ctags/vex-tags'
