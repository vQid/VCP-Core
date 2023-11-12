import json
from pathlib import Path

import openai
import typer

from video_content_preprocessor.console import console
from video_content_preprocessor.content_filter import vcp_filter, VideoChecker
from video_content_preprocessor.downloader import vcp_downloader
from video_content_preprocessor.downloader.video_audio_downloader import check_highest_available, \
    download_highest_video_and_audio
from video_content_preprocessor.downloader.video_clipper import _extract_video_clips
from video_content_preprocessor.validator import _load_and_validate_yaml

app = typer.Typer()

app.add_typer(vcp_downloader)
app.add_typer(vcp_filter)


@app.command(name="fetch-videos", help="Get potential videos from a predefined cfg keywords.")
def _run_config(yml_path: Path):
    vcp = _load_and_validate_yaml(yml_path)
    print("Checking data")
    vc = VideoChecker(vcp)
    try:
        print("Running vc")
        vc.run()
        _filter_captions(vcp.download_root_directory)
    except Exception as e:
        console.print(f"Exception {e} occured...")


@app.command(name="download-videos", help="Download all CreativeCommon Content from a predefined configuration file.")
def _run_config(yml_path: Path):
    vcp = _load_and_validate_yaml(yml_path)
    urls = _get_video_urls_list(Path(vcp.download_root_directory) / "vcp")
    for url in urls:
        try:
            print(f"Downloading {url}")
            download_highest_video_and_audio(url, vcp)
            pass
        except Exception as e:
            console.print(f"Exception {e} occurred...")


@app.command(name="enrich-chat-gpt")
def _enrich_caption(yml_path: Path):
    vcp = _load_and_validate_yaml(yml_path)
    subpath = Path(vcp.download_root_directory) / "vcp"
    print(vcp.model_context)

    if subpath.is_dir():
        print("Sub directories in '{}':".format(subpath))
        for item in subpath.iterdir():
            if item.is_dir():
                print(item.name)
                for file in item.iterdir():
                    if file.is_file():
                        # Überprüfen Sie, ob der Dateiname mit "Captions-" beginnt und mit ".json" endet
                        if file.name.startswith('filtered_captions.txt'):
                            print(f"Found file {file}")
                            filtered_captions = []
                            # Datei gefunden, lesen Sie den Inhalt

                            with open(file, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                                # Entferne Zeilenumbrüche und füge alle Zeilen zu einem String zusammen
                                continuous_text = ' '.join(line.strip() for line in lines)
                            openai.organization = vcp.open_ai_org_id
                            openai.api_key = vcp.open_ai_api_token
                            response = openai.ChatCompletion.create(
                                model="gpt-4",  # Ersetze dies mit dem korrekten Modellnamen, falls erforderlich
                                messages=[
                                    {"role": "system", "content": "You are a helpful assistant."},
                                    {"role": "user",
                                     "content": f"\"{vcp.model_context}\" \n\n The transcript for analysis is as follows: {continuous_text}"},
                                ],
                            )

                            # Zugriff auf den 'text' innerhalb des ersten Objekts im 'choices' Array.
                            text_content = response["choices"][0]["message"]["content"]

                            target_enriched_file = subpath / item.name / "chat-gpt-powered.txt"

                            # Überprüfen Sie, ob die Datei existiert, und löschen Sie sie, wenn sie existiert
                            if target_enriched_file.exists():
                                target_enriched_file.unlink()
                            with open(target_enriched_file, 'w') as file:
                                file.write(text_content)


@app.command(name="create-shorts", help="Download all CreativeCommon Content from a predefined configuration file.")
def _run_config(yml_path: Path):
    vpc = _load_and_validate_yaml(yml_path)
    subpath = Path(vpc.download_root_directory) / "vcp"

    if subpath.is_dir():
        print("Sub directories in '{}':".format(subpath))
        for item in subpath.iterdir():
            file_path = None
            mp4 = None
            if item.is_dir():
                print(item.name)
                for file in item.iterdir():
                    if file.is_file():
                        # Check whether context file is available
                        if file.name.startswith('chat-gpt-powered.txt'):
                            file_path = file
                        elif file.name.endswith('.mp4'):
                            mp4 = file
                if file_path is not None and mp4 is not None:
                    _extract_video_clips(file_path, mp4)
                else:
                    console.print("Either mp4 not available OR text file is not found!")


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
                                        # f.write(f'{text} ({start:.3f})\n')
                                        f.write(f'{text} ({start:.3f}:{duration:.3f})\n')


if __name__ == "__main__":
    app()
