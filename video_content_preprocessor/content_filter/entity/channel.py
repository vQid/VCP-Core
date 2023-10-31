class Channel:
    def __init__(self, name, subscribers, videos, description, creation_date):
        self.name = name
        self.subscribers = subscribers
        self.videos = videos
        self.description = description
        self.creation_date = creation_date

    def get_info(self):
        info = f"Channel Name: {self.name}\n"
        info += f"Subscribers: {self.subscribers}\n"
        info += f"Number of Videos: {self.videos}\n"
        info += f"Description: {self.description}\n"
        info += f"Creation Date: {self.creation_date}\n"
        return info