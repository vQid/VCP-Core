""" Module to download video content from YouTube."""

import typer

from video_content_preprocessor.downloader.video_audio_downloader import check_highest_available
from video_content_preprocessor.downloader.video_audio_downloader import download_highest_video_and_audio, \
    download_highest_video, download_highest_audio
from video_content_preprocessor.model.schema import VCP

vcp_downloader = typer.Typer(name="download", help="Module to download video content from YouTube.")


#@vcp_downloader.command(name="ask")
def ask(yt_url: str):
    check_highest_available(yt_url)


#@vcp_downloader.command(name="high")
def test(yt_url: str):
    """Downloads video and audio of given url from YouTube in the best quality.
    yt_url(str):
        YouTube Url of a video.
    """

    pass
    #download_highest_video_and_audio(yt_url)


#@vcp_downloader.command(name="high-video")
def test(yt_url: str, vcp_config: VCP):
    """Downloads <video> in the highest resolution quality.
    yt_url(str):
        YouTube Url of a video.
    """

    download_highest_video(yt_url)


#@vcp_downloader.command(name="high-audio")
def test2(yt_url: str):
    """Downloads <audio> in the highest resolution quality.
    yt_url(str):
        YouTube Url of a video.
    """
    download_highest_audio(yt_url)
