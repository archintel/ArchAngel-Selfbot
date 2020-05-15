# Function name must be the same as the file name without '.py'
# Make the parameters (bot, msg, prefix, cfg) in that order

async def example(bot, msg, prefix, cfg):
    # Here you put what you would usually put in on_message().
    # For example:
    if msg.author == bot.user:
        if msg.content.startswith(f"{prefix}hey"):
            await msg.channel.send("> Hello!")
        else:
            return False
    else:
        return False
