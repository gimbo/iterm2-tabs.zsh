"""iterm2_tabs.py - set iTerm2 tab titles and colors, via its python API."""

import argparse
import random
from collections import namedtuple

import iterm2


class Color(namedtuple('ColorBase', ('red', 'green', 'blue'))):

    @classmethod
    def random(cls):
        return cls(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def __str__(self):
        return '({}, {}, {})'.format(self.red, self.green, self.blue)


def main():
    args = parse_args()
    if args.list_colors:
        return list_color_names()
    if args.show_colors:
        return show_colors()
    if args.color is not None:
        set_current_tab_color_by_escape_codes(args.color)
    if args.title is not None:
        iterm2.run_until_complete(make_iterm2_run_fn(args.title))


def list_color_names():
    """List color names - basically for tab completion."""
    for color_name in COLORS:
        print(color_name)


def show_colors():

    """List color names and show the actual colors."""

    max_name_length = max(
        [len(color_name) for color_name in COLORS]
    )

    def colorize(msg, fg, bg):
        _fg = '\x1b[38;2;{};{};{}m'.format(*fg)
        _bg = '\x1b[48;2;{};{};{}m'.format(*bg)
        _reset = '\x1b[0m'
        return '{}{}{}{}'.format(_fg, _bg, msg, _reset)

    for color_name, (r, g, b) in COLORS.items():
        color_name = color_name.ljust(max_name_length)
        white_on_color = colorize(color_name, fg=(255, 255, 255), bg=(r, g, b))
        black_on_color = colorize(color_name, fg=(0, 0, 0), bg=(r, g, b))
        print('{} {} {}'.format(color_name, white_on_color, black_on_color))


def set_current_tab_color_by_escape_codes(color):
    template = '\033]6;1;bg;{component};brightness;{value}\a'
    for component, value in color._asdict().items():
        print(template.format(component=component, value=value), end='')


def make_iterm2_run_fn(tab_title):

    async def iterm2_run_fn(connection):
        window = await get_current_window(connection)
        if window is None:
            return
        await set_current_tab_title(window, tab_title)

    return iterm2_run_fn


async def get_current_window(connection):
    app = await iterm2.async_get_app(connection)
    return app.current_terminal_window


async def set_current_tab_title(window, title):
    tab = window.current_tab
    if tab is None:
        return
    session = tab.current_session
    await session.async_set_name(title)
    await tab.async_set_title(title)


def parse_args():

    def color_component(value):
        int_value = int(value)
        if not (0 <= int_value <= 255):
            raise argparse.ArgumentTypeError(
                '{} not in range 0-255'.format(value)
            )
        return int_value

    parser = argparse.ArgumentParser()

    parser.add_argument('--title', '-t', help='Set tab title to given title')

    color_group = parser.add_mutually_exclusive_group()
    color_group.add_argument(
        '--color',
        '-C',
        nargs='?',
        help=(
            'Set tab color to given (named) color specified by name; '
            'use the -L or -S options to see the available color names'
        ),
    )
    color_group.add_argument(
        '--rgb',
        nargs=3,
        metavar=('RED', 'GREEN', 'BLUE'),
        type=color_component,
        help='Set tab color to given color specified by RGB values',
    )
    color_group.add_argument(
        '--random-named-color',
        '-R',
        action='store_true',
        help=(
            'Set tab color to a random color from the list of known color '
            'names, and echo that name and its RGB values'
        ),
    )
    color_group.add_argument(
        '--random-color',
        '-r',
        action='store_true',
        help='Set tab color to a random color and echo its RGB values',
    )

    parser.add_argument(
        '--show-colors',
        '-S',
        action='store_true',
        help='List available color names with demo blocks, and exit',
    )
    parser.add_argument(
        '--list-colors',
        '-L',
        action='store_true',
        help='List available color names, and exit',
    )

    args = parser.parse_args()
    if args.color is not None:
        try:
            args.color = Color(*COLORS[args.color])
        except KeyError:
            print('Unknown color: {}'.format(args.color))
            exit(1)
    elif args.rgb is not None:
        args.color = Color(*args.rgb)
    elif args.random_named_color:
        name, rgb = random.choice(list(COLORS.items()))
        print(name, rgb)
        args.color = Color(*rgb)
    elif args.random_color:
        args.color = Color.random()
        print(args.color)
    return args


# Tab colors from https://github.com/jacaetevha/finna-be-octo-hipster
COLORS = {
    'maroon': (128, 0, 0),
    'dark_red': (139, 0, 0),
    'brown': (165, 42, 42),
    'firebrick': (178, 34, 34),
    'crimson': (220, 20, 60),
    'tomato': (255, 99, 71),
    'coral': (255, 127, 80),
    'indian_red': (205, 92, 92),
    'light_coral': (240, 128, 128),
    'dark_salmon': (233, 150, 122),
    'salmon': (250, 128, 114),
    'light_salmon': (255, 160, 122),
    'orange_red': (255, 69, 0),
    'dark_orange': (255, 140, 0),
    'gold': (255, 215, 0),
    'dark_golden_rod': (184, 134, 11),
    'golden_rod': (218, 165, 32),
    'pale_golden_rod': (238, 232, 170),
    'dark_khaki': (189, 183, 107),
    'khaki': (240, 230, 140),
    'olive': (128, 128, 0),
    'yellow_green': (154, 205, 50),
    'dark_olive_green': (85, 107, 47),
    'olive_drab': (107, 142, 35),
    'lawn_green': (124, 252, 0),
    'chart_reuse': (127, 255, 0),
    'green_yellow': (173, 255, 47),
    'dark_green': (0, 100, 0),
    'forest_green': (34, 139, 34),
    'lime': (0, 255, 0),
    'lime_green': (50, 205, 50),
    'light_green': (144, 238, 144),
    'pale_green': (152, 251, 152),
    'dark_sea_green': (143, 188, 143),
    'medium_spring_green': (0, 250, 154),
    'spring_green': (0, 255, 127),
    'sea_green': (46, 139, 87),
    'medium_aqua_marine': (102, 205, 170),
    'medium_sea_green': (60, 179, 113),
    'light_sea_green': (32, 178, 170),
    'dark_slate_gray': (47, 79, 79),
    'teal': (0, 128, 128),
    'dark_cyan': (0, 139, 139),
    'aqua': (0, 255, 255),
    'cyan': (0, 255, 255),
    'light_cyan': (224, 255, 255),
    'dark_turquoise': (0, 206, 209),
    'turquoise': (64, 224, 208),
    'medium_turquoise': (72, 209, 204),
    'pale_turquoise': (175, 238, 238),
    'aqua_marine': (127, 255, 212),
    'powder_blue': (176, 224, 230),
    'cadet_blue': (95, 158, 160),
    'steel_blue': (70, 130, 180),
    'corn_flower_blue': (100, 149, 237),
    'deep_sky_blue': (0, 191, 255),
    'dodger_blue': (30, 144, 255),
    'light_blue': (173, 216, 230),
    'sky_blue': (135, 206, 235),
    'light_sky_blue': (135, 206, 250),
    'midnight_blue': (25, 25, 112),
    'navy': (0, 0, 128),
    'dark_blue': (0, 0, 139),
    'medium_blue': (0, 0, 205),
    'royal_blue': (65, 105, 225),
    'blue_violet': (138, 43, 226),
    'indigo': (75, 0, 130),
    'dark_slate_blue': (72, 61, 139),
    'slate_blue': (106, 90, 205),
    'medium_slate_blue': (123, 104, 238),
    'medium_purple': (147, 112, 219),
    'dark_magenta': (139, 0, 139),
    'dark_violet': (148, 0, 211),
    'dark_orchid': (153, 50, 204),
    'medium_orchid': (186, 85, 211),
    'purple': (128, 0, 128),
    'thistle': (216, 191, 216),
    'plum': (221, 160, 221),
    'violet': (238, 130, 238),
    'magenta_fuchsia': (255, 0, 255),
    'orchid': (218, 112, 214),
    'medium_violet_red': (199, 21, 133),
    'pale_violet_red': (219, 112, 147),
    'deep_pink': (255, 20, 147),
    'hot_pink': (255, 105, 180),
    'light_pink': (255, 182, 193),
    'pink': (255, 192, 203),
    'antique_white': (250, 235, 215),
    'beige': (245, 245, 220),
    'bisque': (255, 228, 196),
    'blanched_almond': (255, 235, 205),
    'wheat': (245, 222, 179),
    'corn_silk': (255, 248, 220),
    'lemon_chiffon': (255, 250, 205),
    'light_golden_rod_yellow': (250, 250, 210),
    'light_yellow': (255, 255, 224),
    'saddle_brown': (139, 69, 19),
    'sienna': (160, 82, 45),
    'chocolate': (210, 105, 30),
    'peru': (205, 133, 63),
    'sandy_brown': (244, 164, 96),
    'burly_wood': (222, 184, 135),
    'tan': (210, 180, 140),
    'rosy_brown': (188, 143, 143),
    'moccasin': (255, 228, 181),
    'navajo_white': (255, 222, 173),
    'peach_puff': (255, 218, 185),
    'misty_rose': (255, 228, 225),
    'lavender_blush': (255, 240, 245),
    'linen': (250, 240, 230),
    'old_lace': (253, 245, 230),
    'papaya_whip': (255, 239, 213),
    'sea_shell': (255, 245, 238),
    'mint_cream': (245, 255, 250),
    'slate_gray': (112, 128, 144),
    'light_slate_gray': (119, 136, 153),
    'light_steel_blue': (176, 196, 222),
    'lavender': (230, 230, 250),
    'floral_white': (255, 250, 240),
    'alice_blue': (240, 248, 255),
    'ghost_white': (248, 248, 255),
    'honeydew': (240, 255, 240),
    'ivory': (255, 255, 240),
    'azure': (240, 255, 255),
    'snow': (255, 250, 250),
    'black': (0, 0, 0),
    'dim_gray_dim_grey': (105, 105, 105),
    'gray_grey': (128, 128, 128),
    'dark_gray_dark_grey': (169, 169, 169),
    'silver': (192, 192, 192),
    'light_gray_light_grey': (211, 211, 211),
    'gainsboro': (220, 220, 220),
    'white_smoke': (245, 245, 245),
    'white': (255, 255, 255),
    'pure_red': (255, 0, 0),
    'pure_orange': (255, 165, 0),
    'pure_green': (0, 128, 0),
    'pure_blue': (0, 0, 255),
    'pure_yellow': (255, 255, 0),
    'red': (195, 89, 76),
    'orange': (219, 154, 88),
    'green': (65, 174, 76),
    'blue': (92, 155, 204),
    'yellow': (240, 240, 0),
}


if __name__ == '__main__':
    main()
