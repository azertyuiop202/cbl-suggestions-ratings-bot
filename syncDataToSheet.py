from requests import Session
import json
import vars

async def syncCelebRatingsToSheets(client):
  channel = await client.fetch_channel(vars.celebRatingsChannelId)
  messages = await channel.history(limit=1000).flatten()
  dataForSheets = []
  for message in messages:
    messageDataForSheets = {"celeb": message.content, "date": message.created_at.strftime("%Y-%m-%d")}
    for reaction in message.reactions:
      emoji = reaction.emoji
      index = vars.ratings.index(emoji)
      messageDataForSheets[str(index + 1)] = reaction.count - 1
    dataForSheets.append(messageDataForSheets)
  postDataToSheets("ratings", dataForSheets)

def addCelebSuggestionToSheets(celeb, link):
  postDataToSheets("celeb-suggestion", {"celeb": celeb, "link": link})

def postDataToSheets(type, payload):
  session = Session()

  response = session.post(url = vars.sheetId, data = json.dumps({"type": type, "data": payload}))

  print(response.text)
  