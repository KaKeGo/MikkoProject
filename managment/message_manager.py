import discord
import datetime

from discord.ext import commands


class MessageManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.delete_emoji_id = 1332461938352980008  #Delete emoji ID

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Check member has permissions"""
        if payload.emoji.id != self.delete_emoji_id:
            return
        
        member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
        if not member or member.bot:
            return
        
        if not member.guild_permissions.administrator:
            #Remove reaction if not permissions
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, member)

            try:
                await member.send("You don't have permission to mark messages for deletion.")
            except:
                pass

            await self.bot.send_log(
                f"**{member.name}** tried to mark message for deletion without permissions"
            )

    @commands.command(name='delete_marked')
    @commands.has_permissions(administrator=True)
    async def delete_marked_messages(self, ctx, channel: discord.TextChannel = None):
        """Delete all messages marked with delete emoji (Admin only)"""
        try:
            try:
                await ctx.message.delete()
            except:
                pass

            deleted_count = 0
            channel_stats = {}
            channels = [channel] if channel else ctx.guild.text_channels

            for text_channel in channels:
                try:
                    channel_deleted = 0
                    async for message in text_channel.history(limit=1000):
                        for reaction in message.reactions:
                            if isinstance(reaction.emoji, discord.Emoji) and reaction.emoji.id == self.delete_emoji_id:
                                await message.delete()
                                deleted_count += 1
                                channel_deleted += 1
                                break

                    if channel_deleted > 0:
                        channel_stats[text_channel.name] = channel_deleted
                except discord.Forbidden:
                    continue

            if channel:
                await ctx.send(f"Deleted {deleted_count} marked messages from {channel.mention}.")
                await self.bot.send_log(
                    f"**{ctx.author.name}** deleted {deleted_count} marked messages from {channel.name}"
                )
            else:
                await ctx.send(f"Deleted {deleted_count} marked messages from all channels.")
                
                log_message = f"**{ctx.author.name}** deleted messages:\n"

                for channel_name, count in channel_stats.items():
                    log_message += f"- **{channel_name}**: {count} messages\n"
                log_message += f"**Total**: {deleted_count} messages"

                await self.bot.send_log(log_message)

        except Exception as e:
            await ctx.send(f"Error deleting messages: {str(e)}")

    @delete_marked_messages.error
    async def delete_marked_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            #Send message with no permission
            error_message = await ctx.send("You don't have permission to use this command!")
            #Delete message from channel
            try:
                await ctx.message.delete()
            except:
                pass
            # Usuwamy naszą wiadomość o błędzie po 5 sekundach
            await error_message.delete(delay=5)

async def setup(bot):
    await bot.add_cog(MessageManager(bot))
