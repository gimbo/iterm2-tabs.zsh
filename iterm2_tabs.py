#!/usr/bin/env python3

"""iterm2_tabs.py - set iTerm2 tab titles and colors."""


import argparse
from subprocess import Popen, PIPE
import tempfile


# Tab colors from https://github.com/jacaetevha/finna-be-octo-hipster
COLORS = (
    ('maroon', (128, 0, 0)),
    ('dark_red', (139, 0, 0)),
    ('brown', (165, 42, 42)),
    ('firebrick', (178, 34, 34)),
    ('crimson', (220, 20, 60)),
    ('tomato', (255, 99, 71)),
    ('coral', (255, 127, 80)),
    ('indian_red', (205, 92, 92)),
    ('light_coral', (240, 128, 128)),
    ('dark_salmon', (233, 150, 122)),
    ('salmon', (250, 128, 114)),
    ('light_salmon', (255, 160, 122)),
    ('orange_red', (255, 69, 0)),
    ('dark_orange', (255, 140, 0)),
    ('gold', (255, 215, 0)),
    ('dark_golden_rod', (184, 134, 11)),
    ('golden_rod', (218, 165, 32)),
    ('pale_golden_rod', (238, 232, 170)),
    ('dark_khaki', (189, 183, 107)),
    ('khaki', (240, 230, 140)),
    ('olive', (128, 128, 0)),
    ('yellow_green', (154, 205, 50)),
    ('dark_olive_green', (85, 107, 47)),
    ('olive_drab', (107, 142, 35)),
    ('lawn_green', (124, 252, 0)),
    ('chart_reuse', (127, 255, 0)),
    ('green_yellow', (173, 255, 47)),
    ('dark_green', (0, 100, 0)),
    ('forest_green', (34, 139, 34)),
    ('lime', (0, 255, 0)),
    ('lime_green', (50, 205, 50)),
    ('light_green', (144, 238, 144)),
    ('pale_green', (152, 251, 152)),
    ('dark_sea_green', (143, 188, 143)),
    ('medium_spring_green', (0, 250, 154)),
    ('spring_green', (0, 255, 127)),
    ('sea_green', (46, 139, 87)),
    ('medium_aqua_marine', (102, 205, 170)),
    ('medium_sea_green', (60, 179, 113)),
    ('light_sea_green', (32, 178, 170)),
    ('dark_slate_gray', (47, 79, 79)),
    ('teal', (0, 128, 128)),
    ('dark_cyan', (0, 139, 139)),
    ('aqua', (0, 255, 255)),
    ('cyan', (0, 255, 255)),
    ('light_cyan', (224, 255, 255)),
    ('dark_turquoise', (0, 206, 209)),
    ('turquoise', (64, 224, 208)),
    ('medium_turquoise', (72, 209, 204)),
    ('pale_turquoise', (175, 238, 238)),
    ('aqua_marine', (127, 255, 212)),
    ('powder_blue', (176, 224, 230)),
    ('cadet_blue', (95, 158, 160)),
    ('steel_blue', (70, 130, 180)),
    ('corn_flower_blue', (100, 149, 237)),
    ('deep_sky_blue', (0, 191, 255)),
    ('dodger_blue', (30, 144, 255)),
    ('light_blue', (173, 216, 230)),
    ('sky_blue', (135, 206, 235)),
    ('light_sky_blue', (135, 206, 250)),
    ('midnight_blue', (25, 25, 112)),
    ('navy', (0, 0, 128)),
    ('dark_blue', (0, 0, 139)),
    ('medium_blue', (0, 0, 205)),
    ('royal_blue', (65, 105, 225)),
    ('blue_violet', (138, 43, 226)),
    ('indigo', (75, 0, 130)),
    ('dark_slate_blue', (72, 61, 139)),
    ('slate_blue', (106, 90, 205)),
    ('medium_slate_blue', (123, 104, 238)),
    ('medium_purple', (147, 112, 219)),
    ('dark_magenta', (139, 0, 139)),
    ('dark_violet', (148, 0, 211)),
    ('dark_orchid', (153, 50, 204)),
    ('medium_orchid', (186, 85, 211)),
    ('purple', (128, 0, 128)),
    ('thistle', (216, 191, 216)),
    ('plum', (221, 160, 221)),
    ('violet', (238, 130, 238)),
    ('magenta_fuchsia', (255, 0, 255)),
    ('orchid', (218, 112, 214)),
    ('medium_violet_red', (199, 21, 133)),
    ('pale_violet_red', (219, 112, 147)),
    ('deep_pink', (255, 20, 147)),
    ('hot_pink', (255, 105, 180)),
    ('light_pink', (255, 182, 193)),
    ('pink', (255, 192, 203)),
    ('antique_white', (250, 235, 215)),
    ('beige', (245, 245, 220)),
    ('bisque', (255, 228, 196)),
    ('blanched_almond', (255, 235, 205)),
    ('wheat', (245, 222, 179)),
    ('corn_silk', (255, 248, 220)),
    ('lemon_chiffon', (255, 250, 205)),
    ('light_golden_rod_yellow', (250, 250, 210)),
    ('light_yellow', (255, 255, 224)),
    ('saddle_brown', (139, 69, 19)),
    ('sienna', (160, 82, 45)),
    ('chocolate', (210, 105, 30)),
    ('peru', (205, 133, 63)),
    ('sandy_brown', (244, 164, 96)),
    ('burly_wood', (222, 184, 135)),
    ('tan', (210, 180, 140)),
    ('rosy_brown', (188, 143, 143)),
    ('moccasin', (255, 228, 181)),
    ('navajo_white', (255, 222, 173)),
    ('peach_puff', (255, 218, 185)),
    ('misty_rose', (255, 228, 225)),
    ('lavender_blush', (255, 240, 245)),
    ('linen', (250, 240, 230)),
    ('old_lace', (253, 245, 230)),
    ('papaya_whip', (255, 239, 213)),
    ('sea_shell', (255, 245, 238)),
    ('mint_cream', (245, 255, 250)),
    ('slate_gray', (112, 128, 144)),
    ('light_slate_gray', (119, 136, 153)),
    ('light_steel_blue', (176, 196, 222)),
    ('lavender', (230, 230, 250)),
    ('floral_white', (255, 250, 240)),
    ('alice_blue', (240, 248, 255)),
    ('ghost_white', (248, 248, 255)),
    ('honeydew', (240, 255, 240)),
    ('ivory', (255, 255, 240)),
    ('azure', (240, 255, 255)),
    ('snow', (255, 250, 250)),
    ('black', (0, 0, 0)),
    ('dim_gray_dim_grey', (105, 105, 105)),
    ('gray_grey', (128, 128, 128)),
    ('dark_gray_dark_grey', (169, 169, 169)),
    ('silver', (192, 192, 192)),
    ('light_gray_light_grey', (211, 211, 211)),
    ('gainsboro', (220, 220, 220)),
    ('white_smoke', (245, 245, 245)),
    ('white', (255, 255, 255)),
    ('pure_red', (255, 0, 0)),
    ('pure_orange', (255, 165, 0)),
    ('pure_green', (0, 128, 0)),
    ('pure_blue', (0, 0, 255)),
    ('pure_yellow', (255, 255, 0)),
    ('red', (195, 89, 76)),
    ('orange', (219, 154, 88)),
    ('green', (65, 174, 76)),
    ('blue', (92, 155, 204)),
    ('yellow', (240, 240, 0)),
)


def main():
    args = parse_args()
    if args.list_colors:
        # If listing colors, that's all we do; it's basically for tab
        # completion.
        for k, _ in COLORS:
            print(k)
        return
    if args.title is not None:
        iterm2_tab_title(args.title)
    if args.color is not None:
        try:
            rgb = dict(COLORS)[args.color]
        except KeyError:
            print('Unknown color: {}'.format(args.color))
        else:
            iterm2_tab_color(*rgb)


def iterm2_tab_title(title):
    """Set iTerm2 tab title via AppleScript.

    I set the title via AppleScript rather than echoing escape codes
    because the latter requires that the iTerm2 profile in use has the
    "Terminal may set tab/window title" option set.  The problem isn't
    that I mind having to set that option; rather it's that if that
    option is set, other processes I run later can set the title
    themselves, overwriting my title.  I don't want that: when I set the
    tab title I want it to *stay* set - so I need to keep that option
    switched off, and that means I need to set the title via AppleScript
    instead.  No biggie.

    """
    script = """
    tell application "iTerm"
        tell current session of current window
            set name to "{}"
        end tell
    end tell
    """.format(title)
    with tempfile.NamedTemporaryFile() as tf:
        tf.write(script.encode('utf-8'))
        tf.flush()
        p = Popen(['osascript', tf.name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        p.communicate()


def iterm2_tab_color(r, g, b):
    parts = ['\033]6;1;bg;{};brightness;{}\a'.format(n, v)
             for (n, v) in (('red', r), ('green', g), ('blue', b))]
    print(''.join(parts))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--title', nargs='?',
        help='Set tab title to given title')
    parser.add_argument(
        '--color', nargs='?',
        help='Set tab color to given (named) color')
    parser.add_argument(
        '--list-colors', action='store_true',
        help='List available color names; if specified, only this happens.')
    return parser.parse_args()


if __name__ == '__main__':
    main()