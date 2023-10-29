from pydantic import BaseModel


class VPC(BaseModel):
    version: float
    youtube_analytics_api_token: str
    download_root_directory: str
    amount_video_content: int
    keywords: list
