# zsh plugin for setting iTerm2 tab titles and colors
#
# Andy Gimblett, 2017
#
# This provides the following three functions (and their aliases):
#
# iterm2_tab_title        (tt)
# iterm2_tab_color        (tc)
# iterm2_tab_color_named  (tcn)

# The colors are taken from
# https://github.com/jacaetevha/finna-be-octo-hipster; I didn't use
# that directly because I didn't like having one function per color.

# This script defers to python for most of the lifting, primarily
# because I wanted to define colors declaratively, and zsh's
# associative arrays are a bit weak (in particular you can't really
# have a key/value pair where the key is the color name, and the value
# is an rgb triple).

# If you want to set title/color automatically when you enter some
# directory, these functions work well in conjunction with the
# Tarrasch/zsh-autoenv plugin.

# We expect the python script to be in the same folder as the script
# you're reading now:

_iterm2_tabs_py=${0:a:h}/iterm2_tabs.py


# Set tab title, e.g.
#
# $ iterm2_tab_title hello
# $ iterm2_tab_title Long titles OK
#
iterm2_tab_title () {
    $_iterm2_tabs_py --title "$*"
}
alias tt=iterm2_tab_title


# Set tab color with r g b triple, e.g.
#
# $ iterm2_tab_color 127 45 98
#
iterm2_tab_color() {
    echo -n -e "\033]6;1;bg;red;brightness;$1\a"
    echo -n -e "\033]6;1;bg;green;brightness;$2\a"
    echo -n -e "\033]6;1;bg;blue;brightness;$3\a"
}
alias tc=iterm2_tab_color


# Set tab color by name, e.g.
#
# $ iterm2_tab_color_named maroon
#
# Supports tab completion on the known names (which are defined in the
# python script).
#
iterm2_tab_color_named() {
    $_iterm2_tabs_py --color $1
}
alias tcn=iterm2_tab_color_named


# Set up tab completion for iterm2_tab_color_named

_tab_color_completion() {
    _values $($_iterm2_tabs_py --list-colors)
}
compdef _tab_color_completion iterm2_tab_color_named
