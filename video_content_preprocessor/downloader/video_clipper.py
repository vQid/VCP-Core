import re
from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip


def _extract_video_clips(text_file_path, video_file_path):
    # Umwandeln der Pfade in Path-Objekte
    text_file_path = Path(text_file_path)
    video_file_path = Path(video_file_path)

    # Liste für ID-Tags
    id_tags = []

    # Einlesen der HTML-Tags aus der Textdatei
    with text_file_path.open('r') as file:
        content = file.read()

        # Finden und Verarbeiten generischer Tags (z.B. <video>, <a>, etc.)
        for match in re.finditer(r"<(\w+)\s+id=\"(\d+)\" starttime=\"([\d.]+)\" duration=\"([\d.]+)\">(.*?)</\1>",
                                 content):
            tag, id, starttime, duration, text = match.groups()
            id_tags.append(
                {'tag': tag, 'id': id, 'starttime': float(starttime), 'duration': float(duration), 'text': text})

    # Erstellen des Unterordners für die Clips
    shorts_dir = video_file_path.parent / 'shorts'
    shorts_dir.mkdir(exist_ok=True)

    # Durchgehen der ID-Tags und Schneiden der Video-Clips
    for tag in id_tags:
        start = tag['starttime']
        end = start + tag['duration'] + 1.0
        clip_id = tag['id']

        with VideoFileClip(str(video_file_path)) as video:
            # Ausschneiden des Clips
            clip = video.subclip(start, end)

            # Speichern des Clips im Unterordner
            clip_path = shorts_dir / f"{clip_id}.mp4"
            clip.write_videofile(str(clip_path), codec="libx264")

    print("Video-Clips wurden erfolgreich erstellt und gespeichert.")

