class Welcome():
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        try:
            await self.bot.send_message(f":starcohug: Hey! Listen! {member} is here! :fangirlstar:")
        except Exception as e:
            await self.bot.send_message(member.server.owner,
                                        "There is an error with a newcomer, please report this to the creator.\n {}".format(
                                            e))


def setup(bot):
    bot.add_cog(Welcome(bot))