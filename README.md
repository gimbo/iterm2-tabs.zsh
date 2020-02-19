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

Most of the color-related work is done by [a python script](iterm2_tabs.py).

Note that to set tab titles using this plugin you do need to enable the `Applications in terminal may change the title` option on your iTerm2 profile, allowing the title to be set by `echo`s of [proprietary escape codes](https://www.iterm2.com/documentation-escape-codes.html). This does unfortunately mean that other processes that do that same can then overwrite the title you've chosen, but this is the simplest and most reliable way to make this happen.  I experimented for a while with using the iTerm2 python API to set the session name, which is nicely "sticky", but since the 3.3.9 release the security model made that more inconvenient than seemed worthwhile, so I've reverted to the escape code technique.

If you want to set tab title and/or color automatically when you enter some directory, try
[Tarrasch/zsh-autoenv](https://github.com/Tarrasch/zsh-autoenv) in conjunction with this plugin.

Andy Gimblett, andy@barefootcode.com. 2017-2020
