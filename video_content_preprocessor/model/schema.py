from pydantic import BaseModel


class VCP(BaseModel):
    version: float
    youtube_analytics_api_token: str
    download_root_directory: str
    amount_video_content: int
    open_ai_org_id: str
    open_ai_api_token: str
    model_context: list
    keywords: list
