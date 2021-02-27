# Install the packages

!!! INFO !!!

Visit our [documentation](https://docs.dscb.io) for more information/explanation.

`pip install dscb_io`

Head over to the [Discord developer site](https://discord.com/developers/) to get your Bots Token, Client ID and secret (if you are using the Oauth2 Client). Make sure to also set a redirect URL for your bot.

# Example Application of the Client for www.dscb.io
```py
import dscb_io

client = dscb_io.Client("https://dscb.io/api/v1/") # ("current API url")

client.get(670663150365835285) # returns all user information

client.get(670663150365835285, "bio") # returns the information for "bio"

client.get(670663150365835285, "bio", save=True) # saves returned content into {user-ID}.json
```

# Example Application of the Oauth2 Client
```py
from dscb_io import DiscordOauth2Client
from quart import Quart, redirect, render_template_string, request, url_for

app = Quart(__name__)
app.secret_key = b"some random bytes for the secret quart key"
app.config['DISCORD_CLIENT_ID'] = ""
app.config['DISCORD_CLIENT_SECRET'] = ""
app.config['SCOPES'] = ['identify']
app.config['DISCORD_REDIRECT_URI'] = 'http://127.0.0.1:5000/callback'
app.config['DISCORD_BOT_TOKEN'] = ""

client = DiscordOauth2Client(app)


@app.route('/')
@client.is_logged_in
async def index():
    user = await client.fetch_user()
    return f"Hello, {user.name}!"


@app.route('/login/', methods=['GET'])
async def login():
    return await client.create_session()


@app.route('/callback')
async def callback():
    await client.callback()
    return redirect(url_for('index')) #redirects to "/"


if __name__ == '__main__':
    app.run()
```

# Scopes

- **identify** returns `/users/@me` without `email`.
- **email** returns `/users/@me` with an `email`.
- **connections** returns linked accounts (Youtube, Spotify...)
- **guilds** returns the users guilds
- **guilds.join** can be used to join a guild for a user
