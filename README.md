# Lancebot
Discord bot for Reddit purposes

This README.md assumes you already have python and pip. (I used python 3.6.10, not sure on backwards compatibility.) If not, install both

Create a [Reddit App](https://github.com/reddit-archive/reddit/wiki/OAuth2) to generate Client_ID, Username, Password etc. Use [quickstart guide](https://github.com/reddit-archive/reddit/wiki/oauth2-quick-start-example) for a very simple version (It's what I use)

Create Discord App using instructions.

Get relevant python libraries
    
    pip install timeago praw discord random 

Make config.ini file with the following formatting - 

    [DEFAULT]
    discord_token = 
    discord_guild =
    ...
    reddit_client_secret = 
    
    [VAR]
    time = 1591624085
    sub_name = 

