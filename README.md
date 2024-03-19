# Andy's zsh plugin for setting iTerm2 tab colors and title overrides

This plugin provides five functions for setting an iTerm2 tab's color and a title override:

* `iterm2_tab_color` with alias `tc`
* `iterm2_tab_color_named` with alias `tcn`
* `iterm2_tab_color_random` with alias `tcr`
* `iterm2_tab_color_random_named` with alias `tcnr`

and:

* `iterm2_tab_title` with alias `tt`

See [`iterm2-tabs.zsh`](iterm2-tabs.zsh) for more details, and examples.

Colors may be set either as RGB triples or as named colors, where the list of color names (from [jacaetevha/finna-be-octo-hipster](https://github.com/jacaetevha/finna-be-octo-hipster)) is hard-coded - but accessible via tab completion.

* `tcn --show-colors` shows the list of available color names, along with a demo of each color;
* `tcn --list-colors` just shows the names; this is what tab completion triggers.

Most of the color-related work is done by [a python script](iterm2_tabs.py).

Note that (unlike previous versions of this plugin), some external machinery is needed to actually set tab titles using the function provided here; see comments in the plugin itself for more details.

Andy Gimblett, <andy@barefootcode.com>. 2017-2024
