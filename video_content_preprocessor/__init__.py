from pathlib import Path

import typer
import yaml
from pydantic import ValidationError

from video_content_preprocessor.content_filter import vcp_filter, VideoChecker
from video_content_preprocessor.downloader import vcp_downloader
from video_content_preprocessor.downloader.video_audio_downloader import check_highest_available
from video_content_preprocessor.validator import _load_and_validate_yaml

app = typer.Typer()

app.add_typer(vcp_downloader)
app.add_typer(vcp_filter)




@app.command(name="run-config", help="Download all CreativeCommon Content from a predefined configuration file.")
def _run_config(yml_path: Path):

    vpc = _load_and_validate_yaml(yml_path)
    vc = VideoChecker(vpc)

if __name__ == "__main__":
    app()
