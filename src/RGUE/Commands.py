from src.RGUE.ShameModule import shame


async def process_command(context, message, db):
    await shame.ProcessCommand(message, db)

