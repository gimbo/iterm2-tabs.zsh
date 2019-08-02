# Andy's zsh plugin for setting iTerm2 titles and colors

This plugin provides five functions for setting an iTerm2 tab's title/session name, and color:

* `iterm2_tab_title` with alias `tt`
* `iterm2_tab_color` with alias `tc`
* `iterm2_tab_color_named` with alias `tcn`
* `iterm2_tab_color_random` with alias `tcr`
* `iterm2_tab_color_random_named` with alias `tcnr`

See [`iterm2-tabs.zsh`](iterm2-tabs.zsh) for more details, and examples.

Colors may be set either as RGB triples or as named colors, where the list of color names (from [jacaetevha/finna-be-octo-hipster](https://github.com/jacaetevha/finna-be-octo-hipster)) is hard-coded - but accessible via tab completion.

* `tcn --show-colors` shows the list of available color names, along with a demo of each color;
* `tcn --list-colors` just shows the names; this is what tab completion triggers.

Most of the work is done by [a python script](iterm2_tabs.py), which expects to communicate with iTerm2 via [its python API](https://iterm2.com/python-api/), meaning:

* You need to be running iTerm version 3.3 or higher, otherwise the API isn't available; if you're on an earlier version, see [version 1.0.0 of this tool](https://github.com/gimbo/iterm2-tabs.zsh/tree/1.0.0), which uses AppleScript instead of the API.
* You need to set the `ITERM2_PYTHON_PATH` environment variable to point to a python executable with the iTerm API libraries installed; again, see [the iTerm2 Python API docs](https://iterm2.com/python-api/) for more info on this.

Note that to set tab titles using this plugin you do *not* need to enable the `Terminal may set tab/window title` option on your iTerm2 profile - in fact, I recommend that you *don't* set that, because if you do, other processes can overwrite the title you've chosen.  That option allows the tab title to be set using [proprietary escape codes](https://www.iterm2.com/documentation-escape-codes.html); this plugin sets the title via the API instead.  It also sets the tab's session name, because without that, if you bury/unbury a session, you lose the title; apologies if that doesn't work for you, but I did it that way because it works for me. :-) Improvements welcome.

If you want to set tab title and/or color automatically when you enter some directory, try
[Tarrasch/zsh-autoenv](https://github.com/Tarrasch/zsh-autoenv) in conjunction with this plugin.

Andy Gimblett, andy@barefootcode.com. 2017-2019
