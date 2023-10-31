from pathlib import Path

import typer

from video_content_preprocessor.console import console
from video_content_preprocessor.content_filter import vcp_filter, VideoChecker
from video_content_preprocessor.downloader import vcp_downloader
from video_content_preprocessor.downloader.video_audio_downloader import check_highest_available
from video_content_preprocessor.validator import _load_and_validate_yaml

app = typer.Typer()

app.add_typer(vcp_downloader)
app.add_typer(vcp_filter)


@app.command(name="fetch-videos", help="Download all CreativeCommon Content from a predefined configuration file.")
def _run_config(yml_path: Path):
    vpc = _load_and_validate_yaml(yml_path)
    vc = VideoChecker(vpc)
    try:
        vc.run()
    except Exception as e:
        console.print(f"Exception {e} occured...")

@app.command(name="download-videos", help="Download all CreativeCommon Content from a predefined configuration file.")
def _run_config(yml_path: Path):
    vpc = _load_and_validate_yaml(yml_path)
    vc = VideoChecker(vpc)
    try:
        vc.run()
    except Exception as e:
        console.print(f"Exception {e} occured...")



if __name__ == "__main__":
    app()
