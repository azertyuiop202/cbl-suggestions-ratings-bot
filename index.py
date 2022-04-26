from discord.ext import commands
import vars

from syncDataToSheet import syncCelebRatingsToSheets, addCelebSuggestionToSheets

client = commands.Bot(command_prefix="!")
client.remove_command("help")

@client.event
async def on_ready():
  print("Bot is now online and ready to roll")
  
#---

@client.event
async def on_message(message):
  if (str(message.channel.id) != vars.celebRatingsChannelId):
    await client.process_commands(message)
    return

  for rating in vars.ratings:
    await message.add_reaction(rating)

  await client.process_commands(message)

@client.command()
@commands.has_any_role('Mod - Pester Us for Help', 'Volunteer')
async def syncRatingsToSheet(ctx):
  await syncCelebRatingsToSheets(client)
  await ctx.send("Celebs are Synced")
  
@client.command()
@commands.has_any_role('Mod - Pester Us for Help', 'Volunteer')
async def addReactionsToAllMessages(ctx):
  channel = await client.fetch_channel(vars.celebRatingsChannelId)
  messages = await channel.history(limit=1000).flatten()
  for message in messages:
    for rating in vars.ratings:
      await message.add_reaction(rating)
      
  await ctx.send("1-5 reactions are added to all messages")
  
@client.command()
@commands.has_any_role('Mod - Pester Us for Help', 'Volunteer')
async def addCelebSuggestion(ctx, *celeb):
  message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
  addCelebSuggestionToSheets(' '.join(celeb), message.jump_url)

  await ctx.send("Celeb added to the sheet")
  
#---
  
client.run(vars.authToken)