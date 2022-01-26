import spotipy
import spotipy.oauth2
import datetime
import click

from config import Config

SCOPE = "playlist-modify-private,user-read-playback-position"
SPOTIFY_CLIENT = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(scope=SCOPE))
CONFIG = Config.from_file()
HORIZON = datetime.date.today() - datetime.timedelta(days=CONFIG.days_back)


@click.group()
def cli():
  pass


@cli.command()
def add_episodes():
  episode_ids = []
  episodes_in_playlist = SPOTIFY_CLIENT.playlist_items(CONFIG.playlist_id, fields='items.track.uri')
  existing_episode_ids = {episode['track']['uri'] for episode in episodes_in_playlist['items']}

  for podcast_url in CONFIG.podcast_urls:
    episodes = SPOTIFY_CLIENT.show_episodes(podcast_url)

    for episode in episodes['items']:
      episode_release_date = datetime.datetime.strptime(episode['release_date'], '%Y-%m-%d').date()
      if episode_release_date < HORIZON:
        continue
      if episode['resume_point']['fully_played']:
        continue

      if episode['uri'] not in existing_episode_ids:
        episode_ids.append(episode['uri'])

    if episode_ids:
      SPOTIFY_CLIENT.playlist_add_items(CONFIG.playlist_id, episode_ids)


@cli.command()
def prune_episodes():
  episodes_to_delete = set()

  episodes_in_playlist = SPOTIFY_CLIENT.playlist_items(CONFIG.playlist_id, fields='items.track.uri')
  episodes_ids = [episode['track']['uri'] for episode in episodes_in_playlist['items']]
  episodes = SPOTIFY_CLIENT.episodes(episodes_ids)

  for episode in episodes['episodes']:
      episode_release_date = datetime.datetime.strptime(episode['release_date'], '%Y-%m-%d').date()
      if episode_release_date < HORIZON:
        episodes_to_delete.add(episode['uri'])

      if episode['resume_point']['fully_played'] and CONFIG.remove_finished_episodes:
        episodes_to_delete.add(episode['uri'])

  SPOTIFY_CLIENT.playlist_remove_all_occurrences_of_items(CONFIG.playlist_id, list(episodes_to_delete))


if __name__ == '__main__':
  cli()