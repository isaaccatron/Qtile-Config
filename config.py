# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
import os
import subprocess



mod = "mod4"
terminal = "terminator"
files = "thunar"
browser = "brave"
layoutmargins = 5

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    #Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    #Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    #Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    #Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. Immmf current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "t", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "m", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn a command using a prompt widget"),
    Key([mod], "f", lazy.spawn(files), desc="Spawn file managers"),
    Key([mod], "k", lazy.spawn("VBoxManage startvm 'Kali Linux'"), desc="Starts kali vm"),
    Key([mod], "b", lazy.spawn(browser), desc="Starts the browser"),
    Key([mod, "control"], "b", lazy.spawn("blueman-manager"), desc="Opens blueman manager"),
    Key([mod, "control"], "n", lazy.spawn("nm-applet"), desc="Starts nm-applet"),
]

groups = [
    Group("1", label="", matches=[Match(wm_class=["LibreWolf", "firefox", "brave"])]), #Brows
    Group("2", label="", matches=[Match(wm_class=["terminator", "kitty"])], layout="monadwide"), #CMD
    Group("3", label="󰨞", matches=[Match(wm_class=["code-oss"])]), #Dev
    Group("4", label="󰵅", matches=[Match(wm_class=["telegram-desktop", "webcord"])], layout="monadtall"), #Com
    Group("5", label="", layout="max"), #Games
    Group("6", label="", matches=[Match(wm_class=["VirtualBox Machine", "VirtualBox Manager"])]), #VM
    Group("7", label=""), #Video
    Group("8", label="A"), #A
    Group("9", label="B")  #B
]
colors = [
    ['321a16', '321a16'], # Background
    ['dc7360', 'dc7360'], # Colors
    ['6e3a30', '6e3a30'] # Colors but darker
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(margin=layoutmargins, border_focus=colors[1], border_width=2, border_normal=colors[2]),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(margin=layoutmargins, border_width=2, border_focus=colors[1], border_normal=colors[2]),
    layout.MonadWide(margin=layoutmargins, border_width=2, border_focus=colors[1], border_normal=colors[2]),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(fontsize=23, background=colors[0], highlight_method='text', this_current_screen_border=colors[2], active=colors[1], foreground=colors[1], inactive=colors[1], fontshadow='000000'),
                widget.CurrentLayout(background=colors[0]),
                widget.Prompt(background=colors[0]),
                widget.WindowName(background=colors[0]),

                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                #widget.Battery(backgrond=colors[0]),
                widget.Systray(background=colors[0]),
                widget.Backlight(background=colors[0], backlight_name="backlight", brightness_file="/sys/class/backlight/intel_backlight/brightness", max_brightness_file="/sys/class/backlight/intel_backlight/max_brightness", step=5, change_command="brightnessctl set {0}%"),
                widget.Clock(format="%m-%d %I:%M %p", background=colors[0]),
            ],
            25
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        #*layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="unityhub"),
        Match(wm_class="blueman-manager"),
        Match(title="branchdialog"),  # gitk
        Match(wm_class="nm-applet"),
        Match(wm_class="ocs-url"),
        Match(wm_class="JetBrains Toolbox"),
        Match(wm_class="kwalletd5"),
        Match(wm_class="github desktop"),
        Match(wm_class="blueman-applet"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
