import discord
import requests

from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1273027752408387695)
        if channel:
            #Download user avatar
            avatar_url = member.avatar.url
            response = requests.get(avatar_url)
            avatar = Image.open(BytesIO(response.content)).convert("RGBA")

            #Round the avatar
            large_size = (200, 200)
            avatar = avatar.resize(large_size, Image.LANCZOS)
            mask = Image.new('L', large_size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + large_size, fill=255)
            avatar.putalpha(mask)

            avatar = avatar.resize((100, 100), Image.LANCZOS)

            #Add border to the avatar
            border_large_size = (220, 220)
            border_avatar = Image.new('RGBA', border_large_size, (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(border_avatar)
            border_draw.ellipse((0, 0) + border_large_size, fill=(0, 0, 0, 255))
            border_avatar = border_avatar.resize((110, 110), Image.LANCZOS)

            avatar_position = ((border_avatar.size[0] - avatar.size[0]) // 2, (border_avatar.size[1] - avatar.size[1]) // 2)

            border_avatar.paste(avatar, avatar_position, avatar)

            #Create new image
            base_width = 500
            base_height = 200
            base = Image.open(requests.get("https://wallpapercave.com/wp/wp11259639.jpg", stream=True).raw)
            base = base.resize((base_width, base_height))

            #Round the corners of the base image
            corner_radius = 4
            mask = Image.new('L', base.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0) + base.size, corner_radius, fill=255)
            base.putalpha(mask)

            base = ImageOps.expand(base, border=5, fill=(0, 0, 0))

            draw = ImageDraw.Draw(base)

            #Add transparent black background for text
            text_background_width = 435
            text_background_height = 110
            text_background = Image.new('RGBA', (text_background_width, text_background_height), (0, 0, 0, 128))
            text_background_mask = Image.new('L', (text_background_width, text_background_height), 128)
            mask_draw = ImageDraw.Draw(text_background_mask)
            mask_draw.rounded_rectangle((0, 0, text_background_width, text_background_height), 10, fill=128)
            text_background.putalpha(text_background_mask)
            text_background_position = (8 + 50, 50)
            base.paste(text_background, text_background_position, text_background)

            #Add avatar to image
            base.paste(border_avatar, (10, 50), border_avatar)

            #Add welcome message
            font_regular = ImageFont.truetype("fonts/ProtestRevolution-Regular.ttf", 15)
            font_bold = ImageFont.truetype("fonts/Lacquer-Regular.ttf", 18)

            # Text to welcome
            welcome_text = f"Yo! {member.name}"
            welcome_text_2 = "Welcome to the server!"
            welcome_text_3 = "We're excited to have you with us."
            welcome_text_4 = "Make yourself at home!"

            # Calculate text width and position for centering using textbbox
            text_bbox = draw.textbbox((0, 0), welcome_text, font=font_bold)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = text_background_position[0] + (text_background_width - text_width) // 2

            # Draw bold text for "Yo! {member.name}"
            draw.text(
                (text_x, text_background_position[1] + 10),
                welcome_text,
                (255, 255, 255), font=font_bold
            )

            # Calculate position for "Welcome to the server!"
            welcome_text_2_bbox = draw.textbbox((0, 0), welcome_text_2, font=font_regular)
            welcome_text_2_width = welcome_text_2_bbox[2] - welcome_text_2_bbox[0]
            welcome_text_2_x = text_background_position[0] + (text_background_width - welcome_text_2_width) // 2

            # Draw "Welcome to the server!"
            draw.text(
                (welcome_text_2_x, text_background_position[1] + 40),
                welcome_text_2,
                (255, 255, 255), font=font_regular
            )

            # Calculate position for "We're excited to have you with us."
            welcome_text_3_bbox = draw.textbbox((0, 0), welcome_text_3, font=font_regular)
            welcome_text_3_width = welcome_text_3_bbox[2] - welcome_text_3_bbox[0]
            welcome_text_3_x = text_background_position[0] + (text_background_width - welcome_text_3_width) // 2

            # Draw "We're excited to have you with us."
            draw.text(
                (welcome_text_3_x, text_background_position[1] + 60),
                welcome_text_3,
                (255, 255, 255), font=font_regular
            )

            # Calculate position for "Make yourself at home!"
            welcome_text_4_bbox = draw.textbbox((0, 0), welcome_text_4, font=font_regular)
            welcome_text_4_width = welcome_text_4_bbox[2] - welcome_text_4_bbox[0]
            welcome_text_4_x = text_background_position[0] + (text_background_width - welcome_text_4_width) // 2

            # Draw "Make yourself at home!"
            draw.text(
                (welcome_text_4_x, text_background_position[1] + 80),
                welcome_text_4,
                (255, 255, 255), font=font_regular
            )
            
            with BytesIO() as image_binary:
                base.save(image_binary, 'PNG')
                image_binary.seek(0)
                await channel.send(file=discord.File(fp=image_binary, filename='welcome.png'))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(1273027752408387695)
        if channel:
            # Create new image for goodbye message
            avatar_url = member.avatar.url
            response = requests.get(avatar_url)
            avatar = Image.open(BytesIO(response.content)).convert("RGBA")

            # Round the avatar
            large_size = (200, 200)
            avatar = avatar.resize(large_size, Image.LANCZOS)
            mask = Image.new('L', large_size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + large_size, fill=255)
            avatar.putalpha(mask)

            avatar = avatar.resize((100, 100), Image.LANCZOS)

            # Add border to the avatar
            border_large_size = (220, 220)
            border_avatar = Image.new('RGBA', border_large_size, (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(border_avatar)
            border_draw.ellipse((0, 0) + border_large_size, fill=(0, 0, 0, 255))
            border_avatar = border_avatar.resize((110, 110), Image.LANCZOS)

            avatar_position = ((border_avatar.size[0] - avatar.size[0]) // 2, (border_avatar.size[1] - avatar.size[1]) // 2)

            border_avatar.paste(avatar, avatar_position, avatar)

            # Create new image for goodbye message
            base_width = 500
            base_height = 200
            base = Image.open(requests.get("https://wallpapercave.com/wp/wp7816297.jpg", stream=True).raw)
            base = base.resize((base_width, base_height))

            # Round the corners of the base image
            corner_radius = 4
            mask = Image.new('L', base.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0) + base.size, corner_radius, fill=255)
            base.putalpha(mask)

            base = ImageOps.expand(base, border=5, fill=(0, 0, 0))

            draw = ImageDraw.Draw(base)

            # Add transparent black background for text
            text_background_width = 435
            text_background_height = 110
            text_background = Image.new('RGBA', (text_background_width, text_background_height), (0, 0, 0, 128))
            text_background_mask = Image.new('L', (text_background_width, text_background_height), 128)
            mask_draw = ImageDraw.Draw(text_background_mask)
            mask_draw.rounded_rectangle((0, 0, text_background_width, text_background_height), 10, fill=128)
            text_background.putalpha(text_background_mask)
            text_background_position = (8 + 50, 50)
            base.paste(text_background, text_background_position, text_background)

            # Add avatar to image
            base.paste(border_avatar, (10, 50), border_avatar)

            # Add goodbye message
            font_regular = ImageFont.truetype("fonts/ProtestRevolution-Regular.ttf", 15)
            font_bold = ImageFont.truetype("fonts/Lacquer-Regular.ttf", 18)

            # Text for goodbye
            goodbye_text = f"Goodbye, {member.name}!"
            goodbye_text_2 = "We're sad to see you go."
            goodbye_text_3 = "Take care and hope to see you again!"

            # Calculate text width and position for centering using textbbox
            goodbye_text_bbox = draw.textbbox((0, 0), goodbye_text, font=font_bold)
            goodbye_text_width = goodbye_text_bbox[2] - goodbye_text_bbox[0]
            goodbye_text_x = text_background_position[0] + (text_background_width - goodbye_text_width) // 2

            # Draw bold text for "Goodbye, {member.name}!"
            draw.text(
                (goodbye_text_x, text_background_position[1] + 10),
                goodbye_text,
                (255, 255, 255), font=font_bold
            )

            # Calculate position for "We're sad to see you go."
            goodbye_text_2_bbox = draw.textbbox((0, 0), goodbye_text_2, font=font_regular)
            goodbye_text_2_width = goodbye_text_2_bbox[2] - goodbye_text_2_bbox[0]
            goodbye_text_2_x = text_background_position[0] + (text_background_width - goodbye_text_2_width) // 2

            # Draw "We're sad to see you go."
            draw.text(
                (goodbye_text_2_x, text_background_position[1] + 40),
                goodbye_text_2,
                (255, 255, 255), font=font_regular
            )

            # Calculate position for "Take care and hope to see you again!"
            goodbye_text_3_bbox = draw.textbbox((0, 0), goodbye_text_3, font=font_regular)
            goodbye_text_3_width = goodbye_text_3_bbox[2] - goodbye_text_3_bbox[0]
            goodbye_text_3_x = text_background_position[0] + (text_background_width - goodbye_text_3_width) // 2

            # Draw "Take care and hope to see you again!"
            draw.text(
                (goodbye_text_3_x, text_background_position[1] + 60),
                goodbye_text_3,
                (255, 255, 255), font=font_regular
            )

            with BytesIO() as image_binary:
                base.save(image_binary, 'PNG')
                image_binary.seek(0)
                await channel.send(file=discord.File(fp=image_binary, filename='goodbye.png'))


async def setup(bot):
    await bot.add_cog(Welcome(bot))
