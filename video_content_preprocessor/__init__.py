import json
import re
from pathlib import Path

import typer

from video_content_preprocessor.console import console
from video_content_preprocessor.content_filter import vcp_filter, VideoChecker
from video_content_preprocessor.downloader import vcp_downloader
from video_content_preprocessor.downloader.video_audio_downloader import check_highest_available, \
    download_highest_video_and_audio
from video_content_preprocessor.validator import _load_and_validate_yaml

app = typer.Typer()

app.add_typer(vcp_downloader)
app.add_typer(vcp_filter)


@app.command(name="fetch-videos", help="Download all CreativeCommon Content from a predefined configuration file.")
def _run_config(yml_path: Path):
    vpc = _load_and_validate_yaml(yml_path)
    print("Checking data")
    vc = VideoChecker(vpc)
    try:
        print("Running vc")
        vc.run()
        _filter_captions(vpc.download_root_directory)
    except Exception as e:
        console.print(f"Exception {e} occured...")


@app.command(name="download-videos", help="Download all CreativeCommon Content from a predefined configuration file.")
def _run_config(yml_path: Path):
    vpc = _load_and_validate_yaml(yml_path)
    urls = _get_video_urls_list(Path(vpc.download_root_directory) / "vcp")
    for url in urls:
        try:
            print(f"Downloading {url}")
            download_highest_video_and_audio(url, vpc)
            pass
        except Exception as e:
            console.print(f"Exception {e} occurred...")


def _get_video_urls_list(directory: Path):
    """ Function to get video urls from local download_root_directory"""
    directory_path = Path(directory)
    urls = []
    if directory_path.is_dir():
        print("Sub directories in '{}':".format(directory))
        for item in directory_path.iterdir():
            if item.is_dir():
                url = f"https://www.youtube.com/watch?v={item.name}"
                urls.append(url)
                print(url)
    return urls


def _filter_captions(directory: str):
    directory_path = Path(directory) / "vcp"
    if directory_path.is_dir():
        print("Sub directories in '{}':".format(directory_path))
        for item in directory_path.iterdir():
            if item.is_dir():
                for file in item.iterdir():
                    # Überprüfen Sie, ob die Datei eine Datei (und kein Verzeichnis) ist
                    if file.is_file():
                        # Überprüfen Sie, ob der Dateiname mit "Captions-" beginnt und mit ".json" endet
                        if file.name.startswith('Caption-') and file.name.endswith('.json'):
                            print(f"Found file {file}")
                            filtered_captions = []
                            # Datei gefunden, lesen Sie den Inhalt
                            with open(file, 'r', encoding='utf-8') as f:
                                captions = json.load(f)
                                print(captions)
                            # Filtere alle Untertitel heraus, deren "text"-Feld mit "[" beginnt und mit "]" endet,
                                # und schreibe den Text jedes verbleibenden Untertitels in eine Textdatei
                                filtered_captions_absolute_path = file.parent / "filtered_captions.txt"
                                with open(filtered_captions_absolute_path, 'w') as f:
                                    for caption in captions:
                                        text = caption['text']
                                        if text.startswith('[') and text.endswith(']'):
                                            continue  # überspringe diesen Untertitel, wenn er mit "[" beginnt und mit "]" endet
                                        start = caption['start']
                                        duration = caption['duration']
                                        f.write(f'{text} ({start:.3f}:{duration:.3f})\n')


if __name__ == "__main__":
    app()
