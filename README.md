# Andy's zsh plugin for setting iTerm2 titles and colors

This plugin provides three functions for setting an iTerm2 tab's title and color:

* `iterm2_tab_title` with alias `tt`
* `iterm2_tab_color` with alias `tc`
* `iterm2_tab_color_named` with alias `tcn`

See [`iterm2-tabs.zsh`](iterm2-tabs.zsh) for more details, and examples.

Colors may be set either as RGB triples or as named colors, where the list of color names (from [jacaetevha/finna-be-octo-hipster](https://github.com/jacaetevha/finna-be-octo-hipster)) is hard-coded - but accessible via tab completion.

Most of the work is done by [a python script](iterm2_tabs.py) (because I wanted to define the colors declaratively), which expects python 3 to be available.  If you don't have python 3 installed yet, I highly recommend you try [pyenv](https://github.com/pyenv/pyenv).

Note that to set tab titles using this plugin you do *not* need to enable the `Terminal may set tab/window title` option on your iTerm2 profile - in fact, I recommend that you *don't* set that, because if you do, other processes can overwrite the title you've chosen.  That option allows the tab title to be set using [proprietary escape codes](https://www.iterm2.com/documentation-escape-codes.html); this plugin sets the title via AppleScript instead.

If you want to set tab title and/or color automatically when you enter some directory, try
[Tarrasch/zsh-autoenv](https://github.com/Tarrasch/zsh-autoenv) in conjunction with this plugin.

Andy Gimblett, andy@barefootcode.com. 2017
