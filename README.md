# Quickstart
1. Go to [Spotify applications](https://developer.spotify.com/dashboard/applications) and create your app
2. Get CLIENT_ID and CLIENT_SECRET from your Spotify app and fill them in `.env`, see `.env.example` for example.
3. Create and activate venv `python -m venv venv && . venv/bin/activate`
4. Install requirements `python -m pip install -r requirements.txt`
5. Fill `config.yml`, use `config.yml.example` as example.
6. Export variables from `.env` e.g. using `dotenv` or `export` and run `python main.py --help` to see available commands.

## Commands
### add-episodes
This will add new episodes from configured podcasts into your playlist, unless you have already heard them. Only episodes newer than configured horizon will be added.

### prune-episodes
This will remove episodes older than given horizon. If configured, this will also remove already listened episodes.