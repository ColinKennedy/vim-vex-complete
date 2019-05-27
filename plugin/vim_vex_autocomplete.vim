" A function that converts completed VEX functions into automatic UltiSnips snippets
function! s:ExpandVexSignature(completion)
pythonx << EOF
from vim_vex_autocomplete import autocomplete
from UltiSnips import snippet_manager
import vim

completion = vim.eval('a:completion')
text = autocomplete.get_snippet(completion)

if text:
    # Clear out the original completed text and replace it with our own snippet
    autocomplete.clear(len(completion['word']))
    snippet_manager.UltiSnips_Manager.expand_anon(text)
    vim.command('redraw!')
EOF
endfunction

autocmd! CompleteDone *.vex :call s:ExpandVexSignature(v:completed_item)

" Add the tags file so that it shows up in Vim's tag-completion menu
let s:current_directory = expand('<sfile>:p:h')
execute ':set tags+=' . fnamemodify(s:current_directory, ':h') . '/ctags/vex-tags'
