# zsh plugin for setting iTerm2 tab colors and title overrides
#
# Andy Gimblett, 2017-2020
#
# This provides the following five functions (and their aliases):
#
# iterm2_tab_color              (tc)
# iterm2_tab_color_named        (tcn)
# iterm2_tab_color_random       (tcr)
# iterm2_tab_color_random_named (tcnr)
#
# # iterm2_tab_title              (tt)
#
#
# All the colour-related commands are handled by a python script (in the same
# directory).
#
# The colors are taken from
# https://github.com/jacaetevha/finna-be-octo-hipster; I didn't use
# that directly because I didn't like having one function per color.
#
#
# Note that `iterm2_tab_title` simply sets a "tab title override" env var, and
# on its own won't actually affect the tab title.  Previous versions of this
# plugin used iterm2 proprietary escape codes to set the tab title, but I now
# use a more complex (and more powerful) approach to set my tab titles, which
# involves two further steps (not included in this plugin and left as an
# exercise for the reader):
#
# 1. An `iterm2_print_user_vars()` checks if the tab title override env var is
#    set, and if so, copies its value to an iterm2 user variable.
# 2. An AutoLaunch script computes the tab title: if the override is set, it
#    uses that, otherwise it uses some internal logic to automatically choose a
#    title to my preference. (This script is the reason for the change in
#    approach, basically.)  My iterm2 profile is then configured to set the tab
#    title via this scrpt.


# We expect the python script to be in the same folder as the script
# you're reading now
#
_iterm2_tabs_py=${0:a:h}/iterm2_tabs.py


# Set tab color with r g b triple, e.g.
#
# $ iterm2_tab_color 127 45 98
#
iterm2_tab_color() {
    $_iterm2_tabs_py --rgb $1 $2 $3
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


# Set tab color to some random RBG value, and echo it, e.g.
#
# $ iterm2_tab_color_random
#
iterm2_tab_color_random() {
    $_iterm2_tabs_py --random-color
}
alias tcr=iterm2_tab_color_random
# Dark and light variants
tcrd() {
    tc "$((( RANDOM % 128 )))" "$((( RANDOM % 128 )))" "$((( RANDOM % 128 )))"
}
tcrl() {
    tc "$((( RANDOM % 128 ) + 128 ))" "$((( RANDOM % 128 ) + 128 ))" "$((( RANDOM % 128 ) + 128 ))"
}


# Set tab color to some random named color, and echo the name and RGB values,
# e.g.
#
# $ iterm2_tab_color_random_named
#
iterm2_tab_color_random_named() {
    $_iterm2_tabs_py --random-named-color
}
alias tcnr=iterm2_tab_color_random_named


# Set up tab completion for iterm2_tab_color_named

_tab_color_completion() {
    _values $($_iterm2_tabs_py --list-colors)
}
compdef _tab_color_completion iterm2_tab_color_named


# Set tab title override env var, e.g.
#
# $ iterm2_tab_title hello
# $ iterm2_tab_title Long titles OK
#
# See the comment at the top of this file for more info on what's needed to
# actually make this change the tab title.
#
iterm2_tab_title () {
    export TAB_TITLE_OVERRIDE="$*"
}
alias tt=iterm2_tab_title
