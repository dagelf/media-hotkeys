# Audio pause/cycle hotkeys for Linux

One key to pause everything, then cycle through your music and video players one at a time. Another key to pause all players and mute the output immediately. Small Python scripts for **Omarchy, Hyprland, IceWM, Wayland and X11**, using MPRIS and playerctl; no resident daemon.

`media-cycle` first pauses all players. Further presses play each available source in order, then return to silence. If another player starts outside the cycle, the next press pauses everything again. It waits for players to pause before starting another. Jukebox-owned mpv children are excluded to preserve the jukebox's own state.

`media-pause` pauses all MPRIS players and mutes the default output. Cycling to a player unmutes it. Output control tries PipeWire/WirePlumber (`wpctl`), PulseAudio (`pactl`), then ALSA (`amixer`). Players must expose MPRIS; arbitrary browser audio and calls may not.

## Install

Requires Python 3, playerctl and systemd's busctl, plus one of the output controls above. On Omarchy, WirePlumber supplies wpctl. Install missing packages using your package manager.

```sh
git clone https://github.com/dagelf/media-hotkeys
cd media-hotkeys
install -Dm755 media-cycle ~/.local/bin/media-cycle
install -Dm755 media-pause ~/.local/bin/media-pause
install -Dm644 audio_output.py ~/.local/bin/audio_output.py
```

Keep `~/.local/bin` on PATH. No configuration is overwritten and no service is installed. Remove those three installed files to uninstall. Cycle state lives in `$XDG_RUNTIME_DIR` and expires with the login session.

## Keyboard shortcuts

Choose unused keys or deliberately replace your existing mappings. The examples use Super+P for cycle and Super+Q for pause/mute.

Omarchy Quattro (`~/.config/hypr/bindings.lua`):

```lua
o.bind("SUPER + P", "Cycle audio player", "media-cycle")
o.bind("SUPER + Q", "Pause and mute audio", "media-pause")
```

Use `o.rebind` instead of `o.bind` to replace an existing Omarchy mapping.

Hyprland versions using `.conf` configuration:

```ini
bind = SUPER, P, exec, ~/.local/bin/media-cycle
bind = SUPER, Q, exec, ~/.local/bin/media-pause
```

IceWM (`~/.icewm/keys`):

```text
key "Super+p" media-cycle
key "Super+q" media-pause
```

For other desktops, add custom keyboard shortcuts running these commands.

## Related Linux desktop tools

- [Vampire Slayer: background browser and app idle suspend](https://github.com/dagelf/vampireslayer). Chrome or Firefox eating CPU while you're out for lunch, even when they have nothing to do? Vampire Slayer to the rescue. An Omarchy plugin that suspends idle browser and Electron app families, with media exemptions and ignore lists.
- [Graphic equalizer / PipeWire web EQ](https://github.com/dagelf/eq): ten-band stereo graphic equalizer, preamp, presets, per-output settings, application mixer and MPRIS media controls.
- [Linux CLI utilities](https://github.com/dagelf/utils): original home of these hotkeys.

Search terms: audio pause, audio cycle, pause/cycle hotkeys, media hotkeys, keyboard shortcuts, MPRIS, playerctl, PipeWire, PulseAudio, ALSA, Omarchy, Hyprland, Wayland, X11, IceWM, graphic equalizer, Chrome, Firefox, background browser, idle suspend.

## Validation and license

Run `python3 -m unittest -v`. The tests exercise cycle transitions and output fallback without changing desktop audio. MIT; see [LICENSE](LICENSE).
