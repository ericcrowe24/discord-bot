from discord import Embed
from discord import Color


def create_error_embed(message):
    return Embed(title="Error", description=message, color=Color.red())


def find_role(roles, target):
    for r in roles:
        if r.id == int(target):
            return r


def find_members_by_role(members, role):
    found = []

    for member in members:
        if role in member.roles:
            found.append(member)

    return found


def find_member_by_id(members, target):
    for m in members:
        if m.id == int(target):
            return m
