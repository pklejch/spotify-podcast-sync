import spotipy
import datetime
import click

from spotipy.oauth2 import SpotifyOAuth

PODCAST_URLS = ['spotify:show:7CgK022F0Rvtjb2ZoLJeeN', 'spotify:show:2L1T607uBpuxCv6DOISuwa']
PLAYLIST_ID = '4z06aGfukRv9rLJWxoK0d7'
SCOPE = "playlist-modify-private,user-read-playback-position"
DAYS_BACK = 3
REMOVE_FINISHED_EPISODES = True

spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

HORIZON = datetime.date.today() - datetime.timedelta(days=DAYS_BACK)

@click.group()
def cli():
  pass


@cli.command()
def add_episodes():
  episode_ids = []
  episodes_in_playlist = spotify_client.playlist_items(PLAYLIST_ID, fields='items.track.uri')
  existing_episode_ids = {episode['track']['uri'] for episode in episodes_in_playlist['items']}

  for podcast_url in PODCAST_URLS:
    episodes = spotify_client.show_episodes(podcast_url)

    for episode in episodes['items']:
      episode_release_date = datetime.datetime.strptime(episode['release_date'], '%Y-%m-%d').date()
      if episode_release_date < HORIZON:
        continue
      if episode.get('resume_point', {}).get('fully_played', False):
        continue

      if episode['uri'] not in existing_episode_ids:
        episode_ids.append(episode['uri'])

    if episode_ids:
      spotify_client.playlist_add_items(PLAYLIST_ID, episode_ids)


@cli.command()
def prune_episodes():
  episodes_to_delete = set()

  episodes_in_playlist = spotify_client.playlist_items(PLAYLIST_ID, fields='items.track.uri')
  episodes_ids = [episode['track']['uri'] for episode in episodes_in_playlist['items']]
  episodes = spotify_client.episodes(episodes_ids)

  for episode in episodes['episodes']:
      episode_release_date = datetime.datetime.strptime(episode['release_date'], '%Y-%m-%d').date()
      if episode_release_date < HORIZON:
        episodes_to_delete.add(episode['uri'])

      if episode.get('resume_point', {}).get('fully_played', False) and REMOVE_FINISHED_EPISODES:
        episodes_to_delete.add(episode['uri'])

  spotify_client.playlist_remove_all_occurrences_of_items(PLAYLIST_ID, list(episodes_to_delete))


if __name__ == '__main__':
  cli()