import os
import sys
import asyncio
import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands
from rich.console import Console

console = Console()

class RestartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_restart_task = self.bot.loop.create_task(self.auto_restart_by_schedule())

    async def auto_restart_by_schedule(self):
        tz = ZoneInfo("Asia/Bangkok")
        restart_hours = [0, 3, 6, 9, 12, 15, 18, 21]

        while True:
            now = datetime.datetime.now(tz=tz)
            next_hour = min((h for h in restart_hours if h > now.hour), default=restart_hours[0] + 24)
            next_restart = now.replace(hour=next_hour % 24, minute=0, second=0, microsecond=0)
            if next_hour < now.hour:
                next_restart += datetime.timedelta(days=1)
            wait_seconds = (next_restart - now).total_seconds()

            console.log(f"⏳ รอรีสตาร์ทบอทที่ {next_restart} (เวลาไทย) อีก {wait_seconds:.0f} วินาที")
            await asyncio.sleep(wait_seconds)

            console.log("♻️ รีสตาร์ทบอทอัตโนมัติ (เวลาไทย)...")
            await self.bot.close()
            os.execl(sys.executable, sys.executable, *sys.argv)

    @discord.slash_command(name="restart", description="รีสตาร์ทบอท (เฉพาะผู้ที่มี Role ที่กำหนดเท่านั้น)")
    async def restart(self, interaction):
        allowed_role_ids = [1008638970911002684, 1004645617622069348, 1185942925163647066, 1037741810749030511]
        if not any(role.id in allowed_role_ids for role in interaction.user.roles):
            await interaction.response.send_message("⛔ คุณไม่มีสิทธิ์ใช้คำสั่งนี้", ephemeral=True)
            return

        await interaction.response.send_message("♻️ กำลังรีสตาร์ทบอท...", ephemeral=True)
        await self.bot.close()
        os.execl(sys.executable, sys.executable, *sys.argv)


def setup(bot):
    bot.add_cog(RestartCog(bot))
