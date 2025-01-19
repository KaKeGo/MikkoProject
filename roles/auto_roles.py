import discord

from discord.ext import commands
from typing import List


class AutoRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.auto_roles = [
            1324786764698615978,
            1324788130993143858,
            1324788491426467982,
            1324802816220467261,
            1324788381175255143,
            1324788592303935578,
            1324788269191528458,
            1324805503490068544
        ]
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Add auto roles when member joins"""
        try:
            await self.bot.user_db.add_user(member)

            added_roles = []
            failed_roles = []

            for role_id in self.auto_roles:
                role = member.guild.get_role(role_id)
                if role:
                    try:
                        await member.add_roles(role_id)
                        added_roles.append(role.name)
                    except Exception as e:
                        failed_roles.append(f"{role.name} (Error: {str(e)})")
                else:
                    failed_roles.append(f"Role ID {role_id} not found")
            
            log_message = f"**New member joined:**\n"

            if added_roles:
                log_message += "**Added roles:**\n"
                for role_name in added_roles:
                    log_message += f"Role added: {role_name}\n"

            if failed_roles:
                log_message += "**Failed to add roles:**\n"
                for error in failed_roles:
                    log_message += f"Role not added: {error}\n"

            await self.bot.send_log(log_message)

        except Exception as e:
            await self.bot.send_log(f"Error in auto roles system: {str(e)}")

    @commands.command(name='check_roles')
    @commands.has_permissions(administrator=True)
    async def check_missing_roles(self, ctx):
        """Check and add missing roles to all members"""
        try:
            status_message = await ctx.send("Checking roles for all members")
            members_updated = 0
            members_checked = 0

            for member in ctx.guild.members:
                members_checked += 1
                roles_added = []

                for role_id in self.auto_roles:
                    role = ctx.guild.get_role(role_id)
                    if role and role not in member.roles:
                        try:
                            await member.add_roles(role)
                            roles_added.append(role.name)
                        except Exception as e:
                            await self.bot.send_log(f"Error adding {role.name} to {member.display_name}: {str(e)}")
                
                if roles_added:
                    members_updated += 1
                    await self.bot.send_log(
                        f"**Added missing roles to:**\n"
                        f"Member: <@{member.id}>\n"
                        f"Added: {', '.join(roles_added)}"
                    )

                if members_checked % 10 == 0:
                    await status_message.edit(content=f"Checking roles... {members_checked}/{len(ctx.guild.members)} members checked")

            await status_message.edit(
                content=f"Check completed!\n"
                f"Checked: {members_checked} members\n"
                f"Updated: {members_updated} members"
            )

        except Exception as e:
            await ctx.send(f"Error: {str(e)}")
            
    @commands.command(name='show_auto_roles')
    @commands.has_permissions(administrator=True)
    async def show_auto_roles(self, ctx):
        """Show all autoroles configured in the system"""
        message = "**Configured Auto Roles:\n"
        for role_id in self.auto_roles:
            role = ctx.guild.get_role(role_id)
            if role:
                message += f"{role.name} (ID: {role.id})\n"
            else:
                message += f"Invalid Role (ID: {role.id})\n"
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(AutoRoles(bot))
