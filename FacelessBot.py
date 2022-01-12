import discord
from discord.ext import commands
from pipelines import ConversationPipeline

class FacelessBot(commands.Bot):
    def __init__(self, command_prefix: str):
        self._command_prefix = command_prefix
        self._desc = '''A bot that pretends.
        (Suggest a better desc?)'''

        super().__init__(command_prefix=self._command_prefix, description=self._desc)

        self.pipe_convo = ConversationPipeline(
            run_name='perpen',
            bot_name=str(self).split('#')[0],
            pretend_target='Walkier',
            pretend_target_target='sup sup',
            checkpoint='model-9500',
            command_prefix=self._command_prefix,
        )

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        activity = discord.Activity(name="I am x")
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_message(self, message):
        if message.author.bot or not self.is_ready:
            return
        elif message.content.startswith(self._command_prefix):
            if message.content.startswith(self._command_prefix+'help'): #TODO: bandage 
                await message.channel.send("the bot can't see message starting with .")
            await self.process_commands(message)
        else:
            await self.pipe_convo.buffer(message)

    def log_command(self, ctx):
        print('log_command tbd', str(ctx.command), str(ctx.author))

    async def reply(self, channel, message):
        await channel.send(self._command_prefix+message)
    
