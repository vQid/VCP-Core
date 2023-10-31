import pprint
import shutil
from datetime import datetime, timedelta
from pathlib import Path

from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

from video_content_preprocessor.content_filter.entity.video import _write_video_to_csv, Video


class VideoChecker:
    """ Video Checker Thread"""

    def __init__(self, vcp):
        self.youtube = build('youtube', 'v3', developerKey=vcp.youtube_analytics_api_token)
        self.root_sub_directory = Path(vcp.download_root_directory) / "vcp"
        self.keywords_list = vcp
        self.max_results = 10

    def run(self):
        self.search_videos()

    def search_videos(self):
        try:
            # Calculate date and datetime 24 hours
            published_after = datetime.utcnow() - timedelta(days=365)
            published_after_str = published_after.isoformat("T") + "Z"  # Convert to String like ISO 8601-Format

            for query in self.keywords_list:
                print(f"searching for \"{query}\"")
                search_response = self.youtube.search().list(
                    q=query,
                    type="video",
                    part="id,snippet",
                    maxResults=self.max_results,
                    videoLicense="creativeCommon",
                    videoDuration="medium",  # 4-20 minutes
                    publishedAfter=published_after_str,
                ).execute()

                videos = search_response.get('items', [])

                for video_element in videos:
                    video_id = video_element['id']['videoId']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"

                    video_info = None
                    try:
                        print("About to retrieve video info...")
                        video_info = self.youtube.videos().list(
                            part='snippet, contentDetails',
                            id=video_id
                        ).execute()
                    except Exception as e:
                        print(f"Error retrieving video info: {e}")


                    pprint.pprint(video_info)

                    title = video_element['snippet']['title']
                    duration = video_info["items"][0]['contentDetails']['duration']
                    video_instance = Video(video_id, title, duration)

                    videos_data = self.root_sub_directory / video_instance.video_id

                    videos_data.mkdir(parents=True, exist_ok=True)
                    caption_json = "Caption-" + str(video_instance.video_id) + ".json"

                    caption_file_path = videos_data / caption_json

                    # Check if subtitles are available
                    try:
                        captions = self.download_captions_by_url(video_id, caption_file_path)

                        if len(captions) > 0:

                            pprint.pprint(captions)
                            pprint.pprint(video_element)
                            # Generation of the video class instance of passed data
                            videos_data.mkdir(parents=True, exist_ok=True)
                            csv_file = videos_data / ("register" + ".csv")
                            if not csv_file.exists():
                                csv_file.touch()
                            _write_video_to_csv(video_instance, csv_file)

                            if captions:
                                print(f"Video ID: {video_id} has subtitles available.")
                            else:
                                print(f"Video ID: {video_id} does not have subtitles available.")

                    except Exception as e:
                        print(e)
                    else:
                        print(f"The video {video_url} has no captions")

                    current_video_directory_to_delete = Path(videos_data)

                    # Check if the directory exists
                    if current_video_directory_to_delete.exists() and current_video_directory_to_delete.is_dir():
                        # List all the elements in the directory
                        elements = list(current_video_directory_to_delete.iterdir())

                        # Check if the directory is empty
                        if not elements:
                            # Delete the directory
                            shutil.rmtree(current_video_directory_to_delete)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def download_captions_by_url(self, video_id, path_to_save):
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'], preserve_formatting=True)
        pprint.pprint(transcript)
        formatter = JSONFormatter()

        # .format_transcript(transcript) turns the transcript into a JSON string.
        json_formatted = formatter.format_transcript(transcript)

        # Hier bekommen wir eine Liste von Untertiteln
        if len(transcript[0]) > 0:
            if not path_to_save.exists():
                path_to_save.touch()
            with open(path_to_save, 'w', encoding='utf-8') as f:
                f.write(json_formatted)
        return transcript
