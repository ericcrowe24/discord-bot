import src.RGUE.ShameModule as Shame

commands = {"shame": Shame.process_command}


async def process_command(context, message, db):
    command = message.content.split()[0]
    await commands[command[1:]](context, message, db)
