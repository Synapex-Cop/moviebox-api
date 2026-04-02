from pathlib import Path

from moviebox_api.v1.cli.helpers import stream_video_via_mpv, stream_video_via_vlc


class _WithSavedTo:
    def __init__(self, saved_to: Path):
        self.saved_to = saved_to


class _WithoutSavedTo:
    pass


def test_stream_video_via_mpv_skips_items_without_saved_to(monkeypatch):
    captured = {}

    def fake_run(cmd):
        captured["cmd"] = cmd
        return 0

    monkeypatch.setattr("subprocess.run", fake_run)

    stream_video_via_mpv(
        "https://example.com/video.mp4",
        [_WithoutSavedTo(), _WithSavedTo(Path("/tmp/sub.srt"))],
        "/tmp",
    )

    cmd = captured["cmd"]
    assert cmd[0] == "mpv"
    assert "--sid=1" in cmd
    assert "--sub-file=/tmp/sub.srt" in cmd
    assert cmd[-1] == "https://example.com/video.mp4"


def test_stream_video_via_vlc_skips_items_without_saved_to(monkeypatch):
    captured = {}

    def fake_run(cmd):
        captured["cmd"] = cmd
        return 0

    monkeypatch.setattr("subprocess.run", fake_run)

    stream_video_via_vlc(
        "https://example.com/video.mp4",
        [_WithoutSavedTo(), _WithSavedTo(Path("/tmp/sub.srt"))],
        "/tmp",
    )

    cmd = captured["cmd"]
    assert cmd[0] == "vlc"
    assert "--sub-file=/tmp/sub.srt" in cmd
    assert cmd[-1] == "https://example.com/video.mp4"
