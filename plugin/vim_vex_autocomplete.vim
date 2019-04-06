function! ExpandVexSignature(completion)
python << EOF
from vim_vex_autocomplete import autocomplete
from UltiSnips import snippet_manager

completion = vim.eval('a:completion')
snippet = autocomplete.get_snippet(completion)

if snippet:
    snippet_manager.UltiSnips_Manager.expand_anon(snippet)
EOF
endfunction


autocmd! CompleteDone *.vex :call ExpandVexSignature(v:completed_item)
