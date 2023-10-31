import csv
import uuid
from pathlib import Path

import unicodedata


class Video:
    def __init__(self, video_id, title, duration):
        self.video_id = normalize_text(video_id)
        self.title = normalize_text(title)
        self.duration = duration
        self.video_url = f"https://www.youtube.com/watch?v={video_id}"
        self.video_processed = False

    def get_info(self):
        info = f"YT_ID: {self.video_id}\n"
        info += f"Title: {self.title}\n"
        info += f"Duration: {self.duration} minutes\n"
        return info


def _check_if_video_exists(video_id, csv_file):
    with open(csv_file, "r", newline="") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if row[0] == video_id:
                return True
    return False


def _write_video_to_csv(video: Video, csv_file):
    video_id = video.video_id
    video_exists = _check_if_video_exists(video_id, csv_file)
    if not video_exists:
        try:
            with open(csv_file, "a", newline="", encoding="utf-8", errors="ignore") as file:
                writer = csv.writer(file, delimiter=";")
                print("PRINTING THE VALUES OF VIDEO INSTANCE!")
                print(list(vars(video).values()))
                writer.writerow(list(vars(video).values()))
                print(f"Video with ID '{video.video_id}' has been added to the CSV file.")
        except Exception as e:
            print(e)
    else:
        print(f"Video with ID '{video.video_id}' already exists in the CSV file.")


def normalize_text(text):
    if isinstance(text, str):
        normalized_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        return normalized_text
    elif isinstance(text, list):
        normalized_list = [unicodedata.normalize('NFKD', item).encode('ascii', 'ignore').decode('ascii') for item in text]
        return ' '.join(normalized_list)
    else:
        raise TypeError("Invalid input type. Expected str or list.")