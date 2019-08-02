# zsh plugin for setting iTerm2 tab titles and colors
#
# Andy Gimblett, 2017-2019
#
# This provides the following three functions (and their aliases):
#
# iterm2_tab_title              (tt)
# iterm2_tab_color              (tc)
# iterm2_tab_color_named        (tcn)
# iterm2_tab_color_random       (tcr)
# iterm2_tab_color_random_named (tcnr)

# This script defers to a python script (in the same directory) for
# most of the lifting; that python script is able to set a tab's color
# using ANSI escape codes, and is able to set a tab's title (and, at
# the same time, its session name) using the iterm2 python API - which
# means this machinery requires iterm2 version at least 3.3.

# For this to work, you need to set the env var ITERM2_PYTHON_PATH to
# point to an iTerm2-installed python executable, e.g. something like:
# ~/Library/ApplicationSupport/iTerm2/iterm2env/versions/3.7.2/bin/python
# See https://iterm2.com/python-api/ for more info.

# The colors are taken from
# https://github.com/jacaetevha/finna-be-octo-hipster; I didn't use
# that directly because I didn't like having one function per color.

# If you want to set title/color automatically when you enter some
# directory, these functions work well in conjunction with the
# Tarrasch/zsh-autoenv plugin.

# We expect the python script to be in the same folder as the script
# you're reading now:

_iterm2_tabs_py=${0:a:h}/iterm2_tabs.py


check_env_var() {
    if [ -z "${ITERM2_PYTHON_PATH+1}" ]; then
        echo "Env var ITERM2_PYTHON_PATH not set"
        return 1
    fi
}


# Set tab title, e.g.
#
# $ iterm2_tab_title hello
# $ iterm2_tab_title Long titles OK
#
iterm2_tab_title () {
    check_env_var && $ITERM2_PYTHON_PATH $_iterm2_tabs_py --title "$*"
}
alias tt=iterm2_tab_title


# Set tab color with r g b triple, e.g.
#
# $ iterm2_tab_color 127 45 98
#
iterm2_tab_color() {
    check_env_var && $ITERM2_PYTHON_PATH $_iterm2_tabs_py --rgb $1 $2 $3
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
    check_env_var && $ITERM2_PYTHON_PATH $_iterm2_tabs_py --color $1
}
alias tcn=iterm2_tab_color_named


# Set tab color to some random RBG value, and echo it, e.g.
#
# $ iterm2_tab_color_random
#
iterm2_tab_color_random() {
    check_env_var && $ITERM2_PYTHON_PATH $_iterm2_tabs_py --random-color
}
alias tcr=iterm2_tab_color_random


# Set tab color to some random named color, and echo the name and RGB values,
# e.g.
#
# $ iterm2_tab_color_random_named
#
iterm2_tab_color_random_named() {
    check_env_var && $ITERM2_PYTHON_PATH $_iterm2_tabs_py --random-named-color
}
alias tcnr=iterm2_tab_color_random_named


# Set up tab completion for iterm2_tab_color_named

_tab_color_completion() {
    _values $($ITERM2_PYTHON_PATH $_iterm2_tabs_py --list-colors)
}
compdef _tab_color_completion iterm2_tab_color_named
