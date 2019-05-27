# vim-vex-complete

A Vim plugin that auto-completes functions for VEX (SideFX Houdini's scripting language). 

## Demo
![Demo](https://user-images.githubusercontent.com/10103049/58389190-1054be80-7fdd-11e9-869b-ea5d8635e3bd.gif)


## How To Use
Select one of the VEX functions from Vim's tag completion and cycle
through the function's arguments, one at a time.


## Installation
This plugin depends on the [UltiSnips Vim plugin](https://github.com/SirVer/ultisnips)

If you're using a Vim plugin mananger such as [vim-plug](https://github.com/junegunn/vim-plug), all you have to do is add these lines to your .vimrc:

```vim
Plug 'SirVer/ultisnips'
Plug 'ColinKennedy/vim-vex-complete'
```

Restart Vim, run `:PlugInstall`, and you're ready to go.

If you don't use vim-plug, use your Vim plugin manager's equivalent commands.


## Mappings
vim-vex-complete relies on UltiSnips to move between the arguments. The
mappings that are used are set by UltiSnips, not this plugin.

That said, UltiSnips default to "Ctrl + j" to move forward and "Ctrl + k" to move backwards.
You can set your own mappings by adding these lines to your .vimrc:

```vim
let g:UltiSnipsJumpForwardTrigger = <c-j>
let g:UltiSnipsJumpBackwardTrigger = <c-k>
```
