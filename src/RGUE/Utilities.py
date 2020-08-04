from discord import Embed
from discord import Color


def create_error_embed(message):
    return Embed(title="Error", description=message, color=Color.red())


def find_role(message, target):
    for r in message.channel.guild.roles:
        if r.id == int(target):
            return r


def find_members_by_role(message, role):
    members = []

    for member in message.channel.guild.members:
        if role in member.roles:
            members.append(member)

    return members


def find_member_by_id(message, target):
    for m in message.channel.guild.members:
        if m.id == int(target):
            return m


def get_target_data(target):
    prefix = target[2]
    did = target[3:-1]

    # if the person invoking the command is on mobile,
    # the exclamation mark is left out of the id for users.
    if '0' <= prefix <= '9':
        prefix = '!'
        did = target[2:-1]
    return did, prefix, target
