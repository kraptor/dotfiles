" Specify a directory for plugins
" - For Neovim: stdpath('data') . '/plugged'
" - Avoid using standard Vim directory names like 'plugin'
call plug#begin('~/.vim/plugged')

Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'preservim/nerdtree', { 'on':  'NERDTreeToggle' }
Plug 'morhetz/gruvbox'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'preservim/nerdcommenter'
Plug 'easymotion/vim-easymotion'
" CoC needs NodeJS and yarn
Plug 'neoclide/coc.nvim' , { 'branch' : 'release' }

" Initialize plugin system
call plug#end()

" Enable some options
set number
set showmatch
syntax on
set bg=dark

" Key bindings
set  <C-b>=^B
nmap <C-b> :NERDTreeToggle<CR>

" Configure gruvbox
let g:gruvbox_contrast_dark = 'hard'
autocmd vimenter * ++nested colorscheme gruvbox

" Configure airline
let g:airline#extensions#tabline#enabled = 1
"let g:airline_theme='simple'

" Configure NERDCommenter
set <C-\>=^ç
noremap <C-\> :call NERDComment(0, "toggle")<CR>
filetype plugin on

" Configure CoC extensions
let g:coc_global_extensions = ['coc-json', 'coc-git']
" Show autocomplete when Tab is pressed
inoremap <silent><expr> <Tab> coc#refresh()
" GoTo code navigation.
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" Easymotion keybindings
nmap s <Plug>(easymotion-s)
nmap t <Plug>(easymotion-t)
