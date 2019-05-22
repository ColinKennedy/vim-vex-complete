let s:current_directory = expand('<sfile>:p:h')
execute ':set tags+=' . fnamemodify(s:current_directory, ':h') . '/ctags/vex-tags'
