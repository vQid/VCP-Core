import typer

from googleapiclient.discovery import build


from video_content_preprocessor.content_filter.video_searcher import VideoChecker

from video_content_preprocessor.constants_config import DEVELOPER_KEY

youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

vcp_filter = typer.Typer(name="filter", help="Module to filter relevant video content from YouTube.")


@vcp_filter.command(name="get-list")
def generate_trends_list(branch_typ: str):
    try:
        thread = VideoChecker()
    except Exception as e:
        print(f"A Error is occured during the execution!!: {e}")


@vcp_filter.command(name="check-vcc")
def generate_trends_list(video_id: str):
    """
        Check if a YouTube video with the given ID has a Creative Commons license.
    """

    try:
        print(f"checking video...")
        res = youtube.videos().list(id=video_id, part='status').execute()
        video = res['items'][0] if res['items'] else None

        if not video:
            typer.echo("Video not found!")
            raise typer.Exit(code=1)

        license_type = video['status']['license']
        if license_type == 'creativeCommon':
            typer.echo(f"Video {video_id} is licensed under Creative Commons.")
        else:
            typer.echo(f"Video {video_id} is not licensed under Creative Commons (License: {license_type}).")

    except Exception as e:
        print(f"A Error is occured during the execution!!: {e}")
