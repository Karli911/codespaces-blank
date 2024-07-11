from discord.ext import commands
import discord

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member:discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for {reason}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member:discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for {reason}')
    
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self,ctx,member:discord.Member, *, reason=None):
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)
        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f'Muted {member.mention} for {reason}')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member):
        mute_role = ctx.utils.get(ctx.guild.roles, name = "Muted")
        await member.remove_roles(mute_role)
        await ctx.send(f'Unmuted {member.mention}')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def warn(self,ctx,member:discord.Member, *, reason=None):
        await ctx.send(f'Warned {member.mention} for {reason}')

def setup(bot):
    bot.add_cog(Moderation(bot))