from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

mod = "mod4"
alt = "mod1"

terminal = "terminator"
browser = "firefox-bin -P"
lock = "xtrlock"
vol_cur = "amixer -D pulse get Master"
vol_up = "amixer -q -D pulse sset Master 2%+"
vol_down = "amixer -q -D pulse sset Master 2%-"

mute = "amixer -q -D pulse set Master toggle"

colors = {
    "grey": "#555555",
    "red": "#DD1144",
    "blue": "#445588",
    "lgrey": "#b8b6b1",
    "green": "#008080",
}

keys = [
    # Switch between windows in current stack pane
    Key([mod], "comma", lazy.layout.down()),
    Key([mod], "period", lazy.layout.up()),
    Key([mod, "control"], "f", lazy.layout.rotate()),   # flip sides
    Key([mod], "Tab", lazy.layout.next()),

    # Swap panes of split stack

    # My beloved terminal and browser
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod, "shift"], "Return", lazy.spawn(browser)),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),

    # Start, stop, restart
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # Security
    Key([alt, "control"], "l", lazy.spawn(lock)),

    # cycle to previous and next group
    Key([mod, "shift"], "comma", lazy.screen.prev_group(skip_managed=True)),
    Key([mod, "shift"], "period", lazy.screen.next_group(skip_managed=True)),

    # Multihead magic
    Key([mod, "control"], "comma", lazy.prev_screen()),
    Key([mod, "control"], "period", lazy.next_screen()),

    # Multimedia
    Key([], "XF86AudioRaiseVolume", lazy.spawn(vol_up)),
    Key([], "XF86AudioLowerVolume", lazy.spawn(vol_down)),
    Key([], "XF86AudioMute", lazy.spawn(mute)),
]

workspaces = [
    {"key": "1", "name": "shell"},
    {"key": "2", "name": "web", "matches": [Match(wm_class=["Firefox"])]},
    {"key": "3", "name": "mail", "matches": [Match(wm_class=["Thunderbird", "Evolution"])]},
    {"key": "4", "name": "4"},
    {"key": "5", "name": "5"},
    {"key": "6", "name": "6"},
    {"key": "7", "name": "7"},
    {"key": "8", "name": "8"},
    {"key": "9", "name": "9"},
    {"key": "0", "name": "0"},
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(Group(workspace["name"], matches=matches))
    keys.append(
        Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen())
    )
    keys.append(Key(
        [mod, alt], workspace["key"],
        lazy.window.togroup(workspace["name"]),
    ))

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2)
]

widget_defaults = dict(
    font='Monospace',
    fontsize=11,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.TextBox(text="Temp:"),
                #widget.ThermalSensor(threshold=65, foreground_alert=colors["red"]),
                #widget.Sep(padding=15),

                #widget.TextBox(text="Battery:"),
                #widget.Battery(battery_name="BAT1", low_foreground=colors["red"]),
                #widget.Sep(padding=15),

                widget.TextBox(text="Light:"),
                widget.Backlight(
                    brightness_file="/sys/class/backlight/intel_backlight/actual_brightness",
                    max_brightness_file="/sys/class/backlight/intel_backlight/max_brightness",
                ),
                widget.Sep(padding=15),

                widget.TextBox(text="Volume:"),
                widget.Volume(get_volume_command=vol_cur.split()),
                widget.Sep(padding=15),

                widget.Notify(
                    foreground_low=colors["red"][1:],
                    foreground_urgent=colors["red"][1:]
                ),
                widget.Spacer(),
                widget.Clock(
                    timezone="Europe/Berlin",
                    format="%Y-%m-%d %a %H:%M:%S"
                ),
            ],
            30
        ),
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method="block",
                    this_current_screen_border=colors["blue"]
                ),
                widget.Spacer(),
                widget.Prompt(),

            ],
            30,
        ),
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method="block",
                    this_current_screen_border=colors["blue"]
                ),
                widget.Spacer(),
                widget.Prompt(),

            ],
            30,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
wmname = "LG3D"


def main(qtile):
    qtile.cmd_warning()


@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()
