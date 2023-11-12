import re
from pathlib import Path

from moviepy.editor import *
from pytube import YouTube


def clean_filename(filename):
    """
    Cleans the file name by removing or replacing special characters.
    """
    # Ersetzen Sie Sonderzeichen durch Unterstriche oder entfernen Sie sie
    return re.sub(r'[\\/*?:"<>|]', '_', filename)


def download_highest_video_and_audio(download_url: str, vcp_config):
    """
        Downloads and merges the highest quality video and audio streams from a given YouTube video URL.

        This function first identifies the highest resolution video stream and the best quality audio stream available for the given YouTube video. It then downloads these streams separately to a specified directory. After downloading, the video and audio streams are merged into a single MP4 file using the moviepy library. The final video file is saved with a sanitized filename that excludes problematic characters. Temporary files created during the process are cleaned up afterwards.

        Args:
        download_url (str): The URL of the YouTube video to be downloaded.
        vcp_config: Configuration object containing settings such as the download root directory.

        Returns:
        None. The output is the creation of a merged video file in the specified directory.

        Note:
        - The function requires the pytube library for downloading video and audio streams and the moviepy library for merging these streams.
        - The filename of the final video file is cleaned of special characters to avoid file system errors.
        """

    print("Initiating download.")
    yt = YouTube(download_url)

    # Clean up the file name
    clean_title = clean_filename(yt.title)

    # Find the highest video resolution stream
    video_stream = yt.streams.filter(only_video=True).order_by('resolution').desc().first()
    # Find the corresponding audio stream
    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').desc().first()

    # Set the download path
    item_saving_directory = Path(vcp_config.download_root_directory) / "vcp" / yt.video_id
    item_saving_directory.mkdir(exist_ok=True)

    # Download video and audio
    video_file_path = video_stream.download(output_path=item_saving_directory, filename_prefix="video_")
    audio_file_path = audio_stream.download(output_path=item_saving_directory, filename_prefix="audio_")

    # Merge video and audio
    final_video = CompositeVideoClip([VideoFileClip(video_file_path).set_audio(AudioFileClip(audio_file_path))])
    final_video_path = item_saving_directory / f"{clean_title}.mp4"
    final_video.write_videofile(str(final_video_path), codec="libx264", audio_codec="aac")

    # Clean up: Remove temporary files
    Path(video_file_path).unlink(missing_ok=True)
    Path(audio_file_path).unlink(missing_ok=True)

    print(f"Video and audio merged and saved to {final_video_path}")


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
    item_saving_directory = "DOWNLOAD_ROOT_DIRECTORY" / yt.video_id
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
    item_saving_directory = "DOWNLOAD_ROOT_DIRECTORY" / yt.video_id
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
