" Specify a directory for plugins
" - For Neovim: stdpath('data') . '/plugged'
" - Avoid using standard Vim directory names like 'plugin'
call plug#begin('~/.vim/plugged')


Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }


" Initialize plugin system
call plug#end()
