import importlib.machinery
import importlib.util
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
import audio_output

loader = importlib.machinery.SourceFileLoader('cycle', str(Path(__file__).with_name('media-cycle')))
spec = importlib.util.spec_from_loader(loader.name, loader)
cycle = importlib.util.module_from_spec(spec)
loader.exec_module(cycle)


class CycleTests(unittest.TestCase):
    def test_pause_cycle_silence(self):
        players = ['browser', 'music']
        self.assertIsNone(cycle.next_source(players, {}, ['music']))
        self.assertEqual(cycle.next_source(players, {'current': None}, []), 'browser')
        self.assertEqual(cycle.next_source(players, {'current': 'browser'}, ['browser']), 'music')
        self.assertIsNone(cycle.next_source(players, {'current': 'music'}, ['music']))

    def test_external_playback_resets_to_pause(self):
        self.assertIsNone(cycle.next_source(['a', 'b'], {'current': 'a'}, ['a', 'b']))

    def test_disappeared_player_advances_from_old_position(self):
        state = {'current': 'b', 'players': ['a', 'b', 'c']}
        self.assertEqual(cycle.next_source(['a', 'c'], state, []), 'c')
        self.assertIsNone(cycle.next_source(['a'], state, []))

    def test_audio_fallback_stops_after_success(self):
        with patch.object(audio_output.subprocess, 'run', side_effect=[FileNotFoundError(), subprocess.CompletedProcess([], 0)]) as run:
            self.assertTrue(audio_output.set_muted(True))
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args.args[0], ['pactl', 'set-sink-mute', '@DEFAULT_SINK@', '1'])

    def test_no_audio_backend_reports_failure(self):
        with patch.object(audio_output.subprocess, 'run', side_effect=FileNotFoundError()):
            self.assertFalse(audio_output.set_muted(False))


if __name__ == '__main__':
    unittest.main()
