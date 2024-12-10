import interactions
from interactions.ext.files import command_send
from connections import DataBase

import processing
from scraping import HandSpeak, LifePrint
import settings

client = interactions.Client(settings.token,
                             presence=interactions.ClientPresence(
                                 activities=[
                                     interactions.PresenceActivity(
                                         name="/help", type=interactions.PresenceActivityType.LISTENING)
                                 ]
                             ))
database = DataBase()
lp = LifePrint(database)

@client.event
async def on_ready():
    print('We have logged in.')


@client.command(name="randomsign",
                description="Send a random ASL sign from Lifeprint")
async def randomsign(ctx):
    await ctx.send(lp.randomVid())


@client.command(
    name="sign",
    description="Look up a sign from Lifeprint and Handspeak ASL dictionaries",
    options=[
        interactions.Option(
            name="search_input",
            description="Sign to search",
            type=interactions.OptionType.STRING,
            required=True
        )]
)
async def sign(ctx, search_input):
    hs = HandSpeak()

    results_lp = lp.search(search_input)
    results_hs = hs.search(search_input)

    # if len(results_lp) > 10 or results_hs['numPages'] > 1:
    #    embeds = []
    # pagination
    if len(results_lp) > 15:
        list_string_lp = processing.search_result_list(results_lp[:15])
    else:
        list_string_lp = processing.search_result_list(results_lp)

    if len(results_hs['queryResults']) > 10:
        list_string_hs = processing.search_result_list(
            results_hs['queryResults'][:10], source="hs")
        list_string_hs = list_string_hs[:1028]
    else:
        list_string_hs = processing.search_result_list(
            results_hs['queryResults'], source="hs")

    query_formatted = '+'.join(search_input.split())

    embed = interactions.Embed(
        title=f"Search results: {search_input}"
    )

    embed.add_field(name='Lifeprint.com', value=list_string_lp, inline=True)
    embed.add_field(name='Handspeak.com', value=list_string_hs, inline=True)
    embed.add_field(
        name='Google', value=f'[See Google search results >>](https://www.google.com/search?hl=en&q=ASL+sign+for+{query_formatted})', inline=False)

    await ctx.send(embeds=embed)


@client.command(name='fingerspelling', description="Show the ASL alphabet")
async def fingers(ctx):
    embed = interactions.Embed(
        title="ASL Fingerspelling",
        description='''
        • [Fingerspelling & Numbers: In-depth Introduction >>](https://www.lifeprint.com/asl101/fingerspelling/fingerspelling.htm)\n• [Fingerspelling practice and more >>](https://www.lifeprint.com/asl101/fingerspelling/index.htm)
        '''
    )
    embed.set_footer(text="Lifeprint.com")
    embed.set_image(
        url="https://www.lifeprint.com/asl101/fingerspelling/images/abc1280x960.png")
    await ctx.send(embeds=embed)


@client.command(
    name="help",
    description="Show help information for ASL Assistant."
)
async def help(ctx):
    command_prefix = "/"
    commands = {
        "sign": f"Usage: `{command_prefix}sign dog` | Searches handspeak.com, lifeprint.com and google for the ASL sign. Can search handspeak or lifeprint specifically as well.",
        "randomsign": f"Usage: `{command_prefix}randomsign`  | Gets a random video from lifeprint.com.",
        "wotd": f"Usage: `{command_prefix}wotd` | Gets the Word of the Day from handspeak.com.",
        "fingerspelling": f"Usage: `{command_prefix}fingerspelling` | Shows the ASL alphabet and resources for fingerspelling."
    }

    embed = interactions.Embed(
        title="Commands"
    )
    for command in commands:
        embed.add_field(name=command, value=commands[command], inline=False)
    embed.add_field(name="Support Server", value="https://discord.gg/8tHa6cb")
    embed.add_field(name="Invite me to your server",
                    value="[Use this invite link](https://discord.com/oauth2/authorize?client_id=676113360642899988&scope=bot&permissions=139586825281)")
    await ctx.send(embeds=embed)

client.start()