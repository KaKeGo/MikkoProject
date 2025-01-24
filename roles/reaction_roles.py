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

        #Normal roles
        self.normal_roles: Dict[int, List[Tuple[int, int]]] = {
            1332264363444146290: [                          #Role message ID
                (1332264958326603820, 1324788081093509140), #(Emoji ID, Role ID), Polish
                (1332264621997948983, 1324787009763672064), #English
            ],
            1332270390432632904: [ #Hobby Roles
                (1332271182694580284, 1325244899091546262),    #Gamer
                (1332273070400077882, 1325243620827205683),    #Music
                (1332273570050474015, 1324802565027790942),    #Anime
                (1332273986398326837, 1324802924496552070),    #Films
                (1332274472580808704, 1324805622423748643),    #Books
            ],
            1332437974922563625: [ #Game Roles
                (1332438240711671971, 1324802335444308008),    #CS 2
                (1332443942222037142, 1324804844091084902),    #Minecraft
            ]
        }

        # Exclusive roles
        self. exclusive_roles = {
            1332429767328137356: [
                (1332431764441796658, 1330334836644118548), #Female
                (1332431794095521812, 1332429183778951209), #Male
            ]
        }

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
                                f"+  Added: {add_role.name}"
                            )

                    except Exception as e:
                        await self.bot.send_log(f"Error in rules roles: {str(e)}")
                    return

        #Check exclusive roles
        if payload.message_id in self.exclusive_roles:
            for emoji_id, role_id in self.exclusive_roles[payload.message_id]:
                if payload.emoji.id == emoji_id:
                    try:
                        role = guild.get_role(role_id)
                        if role:

                            if role in member.roles:
                                return

                            #Remove role from this same message
                            for other_emoji_id, other_role_id in self.exclusive_roles[payload.message_id]:
                                other_role = guild.get_role(other_role_id)
                                if other_role and other_role in member.roles:
                                    await member.remove_roles(other_role)
                                    #Remove reaction from secound role
                                    message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                                    other_emoji = self.bot.get_emoji(other_emoji_id)
                                    await message.remove_reaction(other_emoji, member)

                            await member.add_roles(role)
                            await self.bot.send_log(
                                f"**__Exclusive role added to__** <@{member.id}>:\n"
                                f"+ Added: {role.name}"
                            )
                    except Exception as e:
                        await self.bot.send_log(f"Error adding exclusive role: {str(e)}")
                    return


        #Check Normal roles
        if payload.message_id in self.normal_roles:
            for emoji_id, role_id in self.normal_roles[payload.message_id]:
                if payload.emoji.id == emoji_id:
                    try:
                        role = guild.get_role(role_id)
                        if role:
                            await member.add_roles(role)
                            await self.bot.send_log(
                                f"**__Role added to__** <@{member.id}>:\n"
                                f"+  Added: {role.name}"
                            )
                    except Exception as e:
                        await self.bot.send_log(f"Error adding normal role: {str(e)}")
                    return
                
        #Check game roles - for gamer role
        if payload.message_id in self.gamer_roles:
            gamer_role = guild.get_role(self.gamer_role_id)
            if gamer_role and gamer_role in member.roles:
                for emoji_id, role_id in self.gamer_roles[payload.message_id]:
                    if payload.emoji.id == emoji_id:
                        try:
                            role = guild.get_role(role_id)
                            if role:
                                await member.add_roles(role)
                                await self.bot.send_log(
                                    f"**Game role added to** <@{member.id}>:\n"
                                    f"+ Added: {role.name}"
                                )
                        except Exception as e:
                            await self.bot.send_log(f"Error adding game role: {str(e)}")
                        return
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """If someone remove role"""
        if payload.channel_id not in self.allowed_channels:
            return
        
        #Rule roles
        if payload.message_id in self.rules_roles:
            return

        #Normal roles
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return
        
        if payload.message_id in self.normal_roles:
            for emoji_id, role_id in self.normal_roles[payload.message_id]:
                if payload.emoji.id == emoji_id:
                    try:
                        role = guild.get_role(role_id)
                        if role:
                            await member.remove_roles(role)
                            await self.bot.send_log(
                                f"**__Role removed from__** <@{member.id}>:\n"
                                f"- Removed: ~~{role.name}~~"
                            )
                    except Exception as e:
                        await self.bot.send_log(f"Error removing normal role: {str(e)}")
                    return
    
    @commands.command(name='check_normal_roles')
    @commands.has_permissions(administrator=True)
    async def check_roles(self, ctx):
        """Check if users have all roles they reacted to"""
        try:
            roles_channel = self.bot.get_channel(self.allowed_channels[1])
            if not roles_channel:
                await ctx.send("Cant find channel with roles!")
                return
            
            missing_roles = []

            all_roles = {**self.normal_roles, **self.exclusive_roles}

            #Check all messages with roles
            for message_id in all_roles:
                message = await roles_channel.fetch_message(message_id)
                if message:
                    for reaction in message.reactions:
                        if isinstance(reaction.emoji, discord.Emoji):
                            #Find role
                            role_id = None
                            for emoji_id, role_id_pair in all_roles[message_id]:
                                if reaction.emoji.id == emoji_id:
                                    role_id = role_id_pair
                                    break

                            if role_id:
                                role = ctx.guild.get_role(role_id)
                                if role:
                                    #Check all users
                                    async for user in reaction.users():
                                        if not user.bot:
                                            member = ctx.guild.get_member(user.id)
                                            if member and role not in member.roles:
                                                missing_roles.append((member, role))

            if missing_roles:
                #Group roles
                user_missing_roles = {}
                for member, role in missing_roles:
                    if member.id not in user_missing_roles:
                        user_missing_roles[member.id] = {"member": member, "roles": []}
                    user_missing_roles[member.id]["roles"].append(role)

                #Send raport
                report = "**__Missing roles:__**\n\n"
                for user_data in user_missing_roles.values():
                    member = user_data["member"]
                    roles = user_data["roles"]
                    report += f"**{member.display_name}** (<@{member.id}>):\n"
                    for role in roles:
                        report += f"- {role.name}\n"
                    report += "\n"

                if len(report) > 2000:
                        parts = [report[i:i+1900] for i in range(0, len(report), 1900)]
                        for part in parts:
                            await ctx.send(part)
                else:
                    await ctx.send(report)

                #Ask to repair
                yes_emoji = self.bot.get_emoji(1330535555561296066)
                no_emoji = self.bot.get_emoji(1332449481538535526)

                msg = await ctx.send(f"Do you want to fix missing roles? (React {yes_emoji} to fix, {no_emoji} to cancel)")
                await msg.add_reaction(yes_emoji)
                await msg.add_reaction(no_emoji)

                def check(reaction, user):
                    return user == ctx.author and (
                        reaction.emoji.id == 1330535555561296066 or 
                        reaction.emoji.id == 1332449481538535526
                    )
                
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

                    if reaction.emoji.id == 1330535555561296066:
                        #Fix roles
                        for member, role in missing_roles:
                            await member.add_roles(role)
                            await self.bot.send_log(
                                f"**__Roles restored to__** <@{member.id}>:\n"
                                f"+ Added: {role.name}"
                            )
                        await ctx.send(f"{yes_emoji} All missing roles have been fixed!")
                    
                    else:
                        await ctx.send(f"{no_emoji} Role fixing cancelled.")
                except TimeoutError:
                    await ctx.send("Time's up. Roles were not fixed.")
            else:
                await ctx.send("All users have correct roles!")

        except Exception as e:
            await ctx.send(f"Check roles Error: {str(e)}")

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
