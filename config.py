import dataclasses
import yaml

CONFIG_FILE_PATH = 'config.yml'


@dataclasses.dataclass
class Config:
    podcast_urls: list[str]
    playlist_id: str
    days_back: int
    remove_finished_episodes: bool

    @classmethod
    def from_file(cls, filepath=CONFIG_FILE_PATH):
        with open(filepath, 'rt') as config_file:
            content = config_file.read()
        config = yaml.safe_load(content)

        return cls(**config)