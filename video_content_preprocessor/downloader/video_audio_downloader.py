from pathlib import Path

from pytube import YouTube

from video_content_preprocessor.constants_config import DOWNLOAD_ROOT_DIRECTORY
from video_content_preprocessor.model.schema import VCP
from video_content_preprocessor.utilities.contents_builder import built_video_data


def download_highest_video_and_audio(download_url: str, vcp_config: VCP):
    """
    Function to download the video by URL. The downloaded video will be in the highest video and audio quality.
    :param download_url:
        Full Url to the YouTube video.
    :return:
        null
    """
    print("Initiating download.")
    yt = YouTube(download_url)
    print("Found highest quality video and audio:")
    print(yt.streams.filter(only_video=True).order_by('resolution').desc().first())
    # Find the Video with the highest Video resolution
    video_stream = yt.streams.filter(only_video=True).order_by('resolution').desc().first()
    # Find the fitting audio file.
    print(yt.streams.filter(only_audio=True, file_extension='mp4').desc().first())
    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').desc().first()

    # Set download path of the YouTube content
    item_saving_directory = Path(vcp_config.download_root_directory) / yt.video_id
    item_saving_directory.mkdir(exist_ok=True)

    built_video_data(yt, Path(DOWNLOAD_ROOT_DIRECTORY) / yt.video_id)
    print(f"\nDownloading Video-Stream: \n{yt.streams.filter(only_video=True).order_by('resolution').desc().first()}")
    video_stream.download(output_path=item_saving_directory)
    print(f"Video download completed to {item_saving_directory}")
    print(f"Downloading Audio-Stream: \n{yt.streams.filter(only_audio=True).first()}")
    audio_stream.download(output_path=item_saving_directory, filename=yt.video_id)
    print(f"Audio download completed to {item_saving_directory}")
    print("Download completed.\n")


def download_highest_video(download_url: str):
    """
    Function to download the video by URL. The downloaded video will be in the highest video and audio quality.
    :param download_url:
        Full Url to the YouTube video.
    :return:
        null
    """

    print("Initiating Process.")
    yt = YouTube(download_url)

    # Set download path of the YouTube content
    item_saving_directory = DOWNLOAD_ROOT_DIRECTORY / yt.video_id
    item_saving_directory.mkdir(exist_ok=True)

    print("Found highest quality video and audio:")
    print(yt.streams.filter(only_video=True).order_by('resolution').desc().first())
    # Den Stream mit der höchsten Videoauflösung finden (ohne Audio)
    video_stream = yt.streams.filter(only_video=True).order_by('resolution').desc().first()
    print(f"Downloading Video-Stream: \n{yt.streams.filter(only_video=True).order_by('resolution').desc().first()}")
    video_stream.download(output_path=item_saving_directory)
    print(f"Video download completed to {item_saving_directory}")
    print("Process completed.")


def download_highest_audio(download_url: str):
    """
    Function to download the video by URL. The downloaded video will be in the highest video and audio quality.
    :param download_url:
        Full Url to the YouTube video.
    :return:
        null
    """
    print("Initiating Process.")
    yt = YouTube(download_url)

    # Set download path of the YouTube content
    item_saving_directory = DOWNLOAD_ROOT_DIRECTORY / yt.video_id
    item_saving_directory.mkdir(exist_ok=True)

    print("Found highest quality video and audio:")
    # Den passenden Audio-Stream finden
    print(f"\n{yt.streams.filter(only_audio=True).first()}")
    audio_stream = yt.streams.filter(only_audio=True).first()
    # Definieren Sie den Pfad, wo das Video gespeichert werden soll.
    print(f"Downloading Audio-Stream: \n{yt.streams.filter(only_audio=True, file_extension='mp4').first()}")
    audio_stream.download(output_path=item_saving_directory, filename=yt.video_id)
    print(f"Audio download completed to {item_saving_directory}")
    print("Process completed.")


def check_highest_available(video_url: str):
    """Function to check the highest available qualities"""
    print("Scanning URL...\n")
    yt = YouTube(video_url)

    print("\n\nHighest available resolution:")
    print(yt.streams.filter(only_video=True).order_by('resolution').desc().first())

    print("\n\nHighest available audio:")
    print(yt.streams.filter(only_audio=True, file_extension='mp4').desc().first())
