"""Mute the default output using the first working Linux audio backend."""
import subprocess


def set_muted(muted):
    commands = [
        ['wpctl', 'set-mute', '@DEFAULT_AUDIO_SINK@', str(int(muted))],
        ['pactl', 'set-sink-mute', '@DEFAULT_SINK@', str(int(muted))],
        ['amixer', 'sset', 'Master', 'mute' if muted else 'unmute'],
    ]
    for command in commands:
        try:
            if subprocess.run(command, capture_output=True, timeout=3).returncode == 0:
                return True
        except (OSError, subprocess.TimeoutExpired):
            pass
    return False
