import bot
import discord
import wikipediaapi
import re
wiki = wikipediaapi.Wikipedia('CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org) generic-library/0.0')

wiki.language = 'es'

if __name__ == '__main__':
    bot.run_discord_bot()


