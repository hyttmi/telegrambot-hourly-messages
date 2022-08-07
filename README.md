# Telegram bot for scheduled messages

With this bot, you can add some timed messages on your chat.

## Prerequisites

You obviously need to first create a bot with BotFather. Create the bot, grab the API key and set it to environment variable for your user in ~/.bashrc:

    echo 'TELEGRAM_TOKEN="YOUR_TOKEN_HERE"' >> ~/.bashrc

 or globally to /etc/environment with:

    echo 'TELEGRAM_TOKEN="YOUR_TOKEN_HERE"' | sudo tee -a /etc/environment

You need to have Redis installed on your system for storing the messages. If you have snap installed on your system, use:

    sudo snap install redis

After that, install the required libraries with:

    pip install -r requirements.txt

## Running the bot

Add the bot to your chat (as an admin) and you can use the following commands:
    
    /start <minutes> Start the scheduled messages eg. /start 10 will post message to chat every 10 minutes.
    /stop Stops the bot.
    /addmsg Adds message to the database. Just use this command and bot will ask you the text afterwards.
    /showmsg Shows messages from the database, ID and message.
    /delmsg Deletes message from the database. Just use this command and bot will ask you the ID afterwards
    /delall Deletes all messages from the database.
