# vim-vex-complete

A Vim plugin that auto-completes functions for VEX (SideFX Houdini's scripting language). 

## Demo
![demo](https://user-images.githubusercontent.com/10103049/58392599-9974f100-7fef-11e9-8a3c-52a2b5902aec.gif)


## How To Use
Select one of the VEX functions from Vim's tag completion and cycle
through the function's arguments, one at a time.


## Installation
This plugin can be used as-is. But if you'd like arguments to be "steppable"
like they are in the above demo, the [UltiSnips Vim plugin](https://github.com/SirVer/ultisnips) must be installed.

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
