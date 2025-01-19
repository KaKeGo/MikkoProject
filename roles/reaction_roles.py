import discord

from discord.ext import commands
from typing import Dict, List, Tuple


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.allowed_channels = [
            1273021911181430794,  #rules channel
            1301631161034084372   #roles channel
        ]

        #Rules configuration
        self.rules_roles: Dict[int, List[Tuple[int, int, int]]] = {
            1324814315580166315: [
                (1330535555561296066,       #emoji ID
                    1324786764698615978,    #remove role
                    1302210575224279070,    #add role
                )
            ]
        }

    @commands.Cog.listener()
    async def on_ready(self):
        """Add reaction if not existing"""
        try:
            """Rule role"""
            for message_id in self.rules_roles:
                channel = self.bot.get_channel(self.allowed_channels[0])
                if channel:
                    try:
                        message = await channel.fetch_message(message_id)
                        if message:
                            for emoji_id, _, _ in self.rules_roles[message_id]:
                                emoji = self.bot.get_emoji(emoji_id)
                                if emoji:
                                    # Sprawdź czy reakcja już istnieje
                                    for reaction in message.reactions:
                                        if isinstance(reaction.emoji, discord.Emoji) and reaction.emoji.id == emoji_id:
                                            break
                                    else:
                                        await message.add_reaction(emoji)
                                        await self.bot.send_log(f"Added reaction {emoji} to rules message {message_id}")
                    except discord.NotFound:
                        await self.bot.send_log(f"Rules message {message_id} not found")
                    except Exception as e:
                        await self.bot.send_log(f"Error adding reaction to rules: {str(e)}")

        except Exception as e:
            await self.bot.send_log(f"Error in reaction setup: {str(e)}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """If someone add reaction"""
        if payload.channel_id not in self.allowed_channels:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return
        
        #Check rules role
        if payload.message_id in self.rules_roles:
            for emoji_id, remove_role_id, add_role_id in self.rules_roles[payload.message_id]:
                if payload.emoji.id == emoji_id:
                    try:
                        remove_role = guild.get_role(remove_role_id)
                        add_role = guild.get_role(add_role_id)

                        if remove_role and add_role:

                            if add_role in member.roles:
                                return

                            await member.remove_roles(remove_role)
                            await member.add_roles(add_role)
                            await self.bot.send_log(
                                f"**__Rules accepted by__** <@{member.id}>:\n"
                                f"- Removed: ~~{remove_role.name}~~\n"
                                f"+ Added: {add_role.name}"
                            )

                    except Exception as e:
                        await self.bot.send_log(f"Error in rules roles: {str(e)}")
                    return
                
        #Normal roles
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """If someone remove role"""
        if payload.channel_id not in self.allowed_channels:
            return
        
        #Rule roles
        if payload.message_id in self.rules_roles:
            return

        #Normal roles

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
