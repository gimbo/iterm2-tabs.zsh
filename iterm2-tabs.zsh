# zsh plugin for setting iTerm2 tab/window titles and tab colors
#
# Andy Gimblett, 2017-2020
#
# This provides the following six functions (and their aliases):
#
# iterm2_window_title           (wt)
# iterm2_tab_title              (tt)
# iterm2_tab_color              (tc)
# iterm2_tab_color_named        (tcn)
# iterm2_tab_color_random       (tcr)
# iterm2_tab_color_random_named (tcnr)
#
# Setting the window or tab title is performed in a straightforward manner via
# an echo with some control codes; there are two prerequisites for this to
# work:
#
# 1. The option "Applications in terminal may change the title" option
#    must be ticked in your iTerm2 profile's "General" preferences
#    tab. You need to ensure this.
#
# 2. For tab titles: the DISABLE_AUTO_TITLE env var must be set to "true"; this
#    prevents iTerm2 from automatically overwriting the tab title with a
#    session name, job name, etc. This env var is set for you automatically by
#    the iterm2_tab_title function, so you don't need to do anything here
#    except be aware that those automatic updates won't be happening once you
#    explicitly define a title - which is presumably what you wanted to have
#    happen. :-)
#
# All the colour-related commands are handled by a python script (in
# the same directory).
#
# The colors are taken from
# https://github.com/jacaetevha/finna-be-octo-hipster; I didn't use
# that directly because I didn't like having one function per color.
#
# If you want to set title/color automatically when you enter some
# directory, these functions work well in conjunction with the
# Tarrasch/zsh-autoenv plugin.

# We expect the python script to be in the same folder as the script
# you're reading now
#
_iterm2_tabs_py=${0:a:h}/iterm2_tabs.py

# Set window title, e.g.
#
# $ iterm2_window_title hello
# $ iterm2_window_title Long titles OK
#
# https://www.reddit.com/r/zsh/comments/jp18n3/how_to_rename_iterm2_window_title_with_zsh/gbdj1et/
#
iterm2_window_title () {
    export DISABLE_AUTO_TITLE="true"
    echo -ne "\e]2;$*\a"
}
alias wt=iterm2_window_title


# Set tab title, e.g.
#
# $ iterm2_tab_title hello
# $ iterm2_tab_title Long titles OK
#
# # https://www.reddit.com/r/zsh/comments/jp18n3/how_to_rename_iterm2_window_title_with_zsh/gbdj1et/
#
iterm2_tab_title () {
    export DISABLE_AUTO_TITLE="true"
    echo -ne "\e]1;$*\a"
}
alias tt=iterm2_tab_title


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
