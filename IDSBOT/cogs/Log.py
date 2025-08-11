import discord
from discord.ext import commands
from rich.console import Console

console = Console()

class VoiceLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1404332603691241573  
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # ดึง channel log
        LOG = await self.bot.fetch_channel(self.log_channel_id)

        # กรณี user เข้าห้อง
        if before.channel is None and after.channel is not None and not after.afk and not member.bot:
            embed = discord.Embed(
                title="JOIN VOICE CHAT",
                description=f"{member.display_name} เข้าห้อง {after.channel.mention}.",
                color=discord.Color.dark_purple()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await LOG.send(embed=embed)

        # กรณี user ย้ายห้อง
        elif after.channel and before.channel and before.channel != after.channel and not member.bot:
            embed = discord.Embed(
                title="MOVE VOICE CHAT",
                description=f"{member.display_name} ย้ายจาก {before.channel.mention} ไป {after.channel.mention}",
                color=discord.Color.dark_purple()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await LOG.send(embed=embed)

        # กรณี user กลับจาก AFK
        elif after.channel and before.afk and not after.afk and not member.bot:
            embed = discord.Embed(
                title="AFK",
                description=f"{member.display_name} ได้กลับมาจากการ AFK แล้ว",
                color=discord.Color.dark_purple()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        # กรณี user ออกจากห้อง
        elif after.channel is None and before.channel is not None and not before.afk and not member.bot:
            embed = discord.Embed(
                title="LEAVE VOICE CHAT",
                description=f"{member.display_name} ออกจากห้อง {before.channel.mention}.",
                color=discord.Color.dark_purple()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await LOG.send(embed=embed)

def setup(bot):
    bot.add_cog(VoiceLogs(bot))
