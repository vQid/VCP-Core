import json
from pathlib import Path

from pytube import YouTube


def built_video_data(yt: YouTube, video_content_path: Path):
    """ Function to fetch data out of YouTube content into a JSON-File for further usage.

    params:
        yt(YouTube):
            pytube YouTube obj.
        root_path(Path):
            Path in which the file should be created.
    """

    meta_data_absolute_path = video_content_path / "METADATA.json"
    meta_data_absolute_path.touch(exist_ok=True)

    data_dict = {
        "video_url": f"https://www.youtube.com/watch?v={yt.video_id}",
        "video_id": yt.video_id,
        "captions": str(yt.captions),
        "title": yt.title,
        "keywords": yt.keywords,
        "age_restricted": yt.age_restricted,
        "author": yt.author,
        "channel_id": yt.channel_id,
        "channel_url": yt.channel_url,
        "length": yt.length,
        "publish_date": str(yt.publish_date),
        "rating": yt.rating,
        "vid_info": yt.vid_info,
        "thumbnail_url": yt.thumbnail_url,
        "views": yt.views
    }

    with open(meta_data_absolute_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)
