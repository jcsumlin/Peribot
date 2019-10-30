import os
from datetime import datetime

import discord
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_databases import AuditLog, ServerSettings, Base, CustomCommands, Warnings, StarBoardSettings, \
    BirthdaySettings, Birthdays, StarBoardMessages, StarBoardIgnoredChannels, StarboardAllowedRoles, RemindMe


class Database:
    def __init__(self, path='peribot.db'):
        path = os.path.abspath(path)
        engine = create_engine("sqlite:///" + path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    async def add_server_settings(self, guild: discord.Guild):
        check = self.session.query(ServerSettings).filter_by(server_id=guild.id).first()
        if check is None:
            new_server = ServerSettings(server_id=guild.id,
                                        server_name=guild.name,
                                        prefix="!",
                                        region=str(guild.region),
                                        owner_id=guild.owner_id,
                                        is_premium=False)
            self.session.add(new_server)
            self.session.commit()
            return await self.audit_record(guild.id,guild.name,"Joined new server", 0)
        return await self.audit_record(guild.id,guild.name,"rejoined server", 0)

    async def update_server_settings(self, server_id, prefix=None):
        settings = await self.get_server_settings(server_id)
        if prefix is not None:
            settings.prefix = prefix
            self.session.commit()
            return True
        return False

    async def get_server_settings(self, server_id):
        return self.session.query(ServerSettings).filter(ServerSettings.server_id == server_id).first()

    async def update_server_premium(self, server_id, status: bool):
        server_settings = await self.get_server_settings(server_id)
        server_settings.is_premium = status
        self.session.commit()
        await self.audit_record(server_id, server_settings.server_name, f"Updated premium status to {status}", 0)
        return server_settings

    async def audit_record(self, server_id, server_name, command_invoked, user_id):
        new_audit = AuditLog(server_id=server_id,
                             server_name=server_name,
                             time=datetime.now(),
                             command_invoked=command_invoked,
                             user_id=user_id)
        self.session.add(new_audit)
        self.session.commit()

    async def add_custom_command(self, server_id: int, command: str, result: str, user_id: int):
        if self.session.query(CustomCommands).filter_by(server_id=server_id).filter_by(command=command).first() is None:
            cc = CustomCommands(server_id=server_id,
                                command=command,
                                result=result,
                                added_by_user_id=user_id)
            self.session.add(cc)
            self.session.commit()
        else:
            raise ValueError('That command already exists for this server.')

    async def get_custom_command(self, id, cmd):
        cc = self.session.query(CustomCommands).filter_by(server_id=id).filter_by(command=cmd).one_or_none()
        if cc is not None:
            return cc.result
        return None

    async def get_custom_commands(self, id):
        cc = self.session.query(CustomCommands).filter_by(server_id=id).all()
        if cc is not None and len(cc) > 0:
            return cc
        return None

    async def edit_custom_command(self, server_id, command, result):
        cc = self.session.query(CustomCommands).filter_by(server_id=server_id).filter_by(command=command).first()
        if cc is not None:
            cc.result = result
            self.session.commit()
            return True
        return False

    async def delete_custom_command(self, server_id, command):
        cc = self.session.query(CustomCommands).filter_by(server_id=server_id).filter_by(command=command).first()
        if cc is not None:
            cc.delete()
            self.session.commit()
            return True
        return False

    async def get_all_reports(self, server_id):
        reports = self.session.query(Warnings).filter_by(server_id=server_id).all()
        if reports is not None and len(reports) > 0:
            return reports
        return None

    async def add_warning(self, server_id: int, user, mod, reason):
        new_report = Warnings(date=datetime.utcnow(),
                            server_id=server_id,
                            user_name=user.name,
                            user_id=user.id,
                            mod_name=mod.name,
                            mod_id=mod.id,
                            reason=reason)
        self.session.add(new_report)
        self.session.commit()
        return True

    async def get_user_warns(self, server_id, user_id):
        reports = self.session.query(Warnings)\
            .filter_by(server_id=server_id)\
            .filter_by(user_id=user_id)\
            .all()
        return reports

    async def get_warn(self, server_id: int, warning_id: int):
        report = self.session.query(Warnings)\
            .filter_by(server_id=server_id)\
            .filter_by(id=warning_id)\
            .one_or_none()
        return report

    async def delete_report(self, server_id, warning_id):
        report = self.session.query(Warnings) \
            .filter_by(server_id=server_id) \
            .filter_by(id=warning_id) \
            .one_or_none()
        if report is not None:
            backup = report
            self.session.delete(report)
            self.session.commit()
            return backup
        return None

    async def post_starboard_settings(self, server_id: int, enabled: bool, channel_id: int, emoji: str, threshold: int):
        settings = StarBoardSettings(server_id=server_id,
                                     enabled=enabled,
                                     channel_id=channel_id,
                                     emoji=emoji,
                                     threshold=threshold)

        self.session.add(settings)
        self.session.commit()

    async def birthday_exists(self, ctx):
        user = self.session.query(Birthdays).filter_by(user_id=ctx.author.id).one_or_none()
        if user is None:
            return False
        return user
        pass

    async def get_birthday_settings(self, id):
        settings = self.session.query(BirthdaySettings).filter_by(server_id=id).one_or_none()
        return settings

    async def add_birthday_settings(self, id: int, enabled: bool, channel_id: int, default_message: str):
        new_settings = BirthdaySettings(server_id=id,
                         enabled=enabled,
                         channel_id=channel_id,
                         message=default_message)
        self.session.add(new_settings)
        self.session.commit()
        return new_settings

    async def update_birthday_settings(self, guild_id:int, enabled: bool=None, channel_id: int=None, message: str=None):
        settings = self.session.query(BirthdaySettings).filter_by(server_id=guild_id).one_or_none()
        if settings is not None:
            if enabled is not None:
                settings.enabled = enabled
            if channel_id is not None:
                settings.channel_id = channel_id
            if message is not None:
                settings.message = message
            self.session.commit()
            return settings

    async def get_todays_birthdays(self):
        todays_bdays = []
        res = self.session.query(Birthdays)\
            .filter_by(completed=False)\
            .all()
        for birthday in res:
            if isinstance(birthday.birthday , int):
                birthday.birthday = datetime.fromtimestamp(int(birthday.birthday)/1000)
            if isinstance(birthday.birthday, str):
                birthday.birthday = datetime.strptime(birthday.birthday, '%Y-%m-%d %H:%M:%S')
            else:
                logger.error(f"Birthday is in unrecognized format (not int or string), skipping {birthday}")
                continue
            if birthday.birthday.month == datetime.now().month and birthday.birthday.day == datetime.now().day:
                todays_bdays.append(birthday)

        return todays_bdays

    async def update_birthday(self, id, completed: bool = None, new_birthday: datetime = False):
        birthday = self.session.query(Birthdays).filter_by(id=id).one_or_none()
        if birthday is not None:
            if completed is not None:
                birthday.completed = completed
            if new_birthday is not False:
                birthday.birthday = new_birthday
            self.session.commit()
            return birthday
        return False

    async def add_birthday(self, server_id, user_id, birthday):
        birthday = Birthdays(server_id=server_id,
                  user_id=user_id,
                  birthday=birthday,
                  completed=False)
        self.session.add(birthday)
        self.session.commit()
        return birthday

    async def get_months_bdays(self):
        this_months_bdays = []
        res = self.session.query(Birthdays).all()
        for birthday in res:
            if isinstance(birthday.birthday, int):
                birthday.birthday = datetime.fromtimestamp(int(birthday.birthday) / 1000)
            if isinstance(birthday.birthday, str):
                birthday.birthday = datetime.strptime(birthday.birthday, '%Y-%m-%d %H:%M:%S')
            else:
                logger.error(f"Birthday is in unrecognized format (not int or string), skipping {birthday}")
                continue
            if birthday.birthday.month == datetime.now().month:
                this_months_bdays.append(birthday)
        return this_months_bdays

    async def delete_birthday(self, user_id: int = None, id:int = None):
        if user_id:
            birthday = self.session.query(Birthdays).filter_by(user_id=user_id).delete()
            if birthday != 1:
                raise ValueError("Invalid ID")
            self.session.commit()
        elif id:
            birthday = self.session.query(Birthdays).filter_by(id=id).delete()
            if birthday != 1:
                raise ValueError("Invalid ID")
            self.session.commit()

    async def clear_starboard(self, id: int):
        try:
            stmt = StarBoardMessages.__table__.delete().where(StarBoardMessages.server_id == id)
            self.session.execute(stmt)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    async def get_ignored_starboard_channels(self, server_id: int):
        list_of_channels = []
        channels = self.session.query(StarBoardIgnoredChannels).filter_by(server_id=server_id).all()
        for channel in channels:
            list_of_channels.append(channel.channel_id)
        return list_of_channels

    async def delete_starboard_ignored_channel(self, server_id, channel_id):
        res = self.session.query(StarBoardIgnoredChannels)\
            .filter_by(server_id=server_id)\
            .filter_by(channel_id=channel_id).delete()
        if res == 1:
            return True
        return False

    async def add_starboard_ignored_channel(self, server_id, channel_id):
        channel = StarBoardIgnoredChannels(server_id=server_id,
                                 channel_id=channel_id)
        self.session.add(channel)
        self.session.commit()
        return True

    async def get_starboard_settings(self, server_id):
        settings = self.session.query(StarBoardSettings).filter_by(server_id=server_id).one_or_none()
        return settings

    async def update_starboard_settings(self, server_id, emoji=None, channel_id=None, threshold=None, enabled=None):
        updated = False
        settings = self.session.query(StarBoardSettings).filter_by(server_id=server_id).one_or_none()
        if settings is not None and emoji is not None:
            settings.emoji = emoji
            updated = True
        if settings is not None and channel_id is not None:
            settings.channel_id = channel_id
            updated = True
        if settings is not None and threshold is not None:
            settings.threshold = threshold
            updated = True
        if settings is not None and enabled is not None:
            settings.enabled = enabled
            updated = True
        if updated:
            self.session.commit()
        return updated

    async def get_starboard_roles(self, server_id):
        list_of_roles = []
        roles = self.session.query(StarboardAllowedRoles).filter_by(server_id=server_id).all()
        for role in roles:
            list_of_roles.append(role.role_id)
        return list_of_roles

    async def delete_starboard_role(self, server_id, role_id):
        role = self.session.query(StarboardAllowedRoles).filter_by(server_id=server_id).filter_by(role_id=role_id).one_or_none()
        if role is not None:
            role.delete()
            self.session.commit()
            return True
        return False

    async def post_starboard_role(self, server_id, role_id):
        role = StarboardAllowedRoles(server_id=server_id,
                                     role_id=role_id)
        self.session.add(role)
        self.session.commit()

    async def get_starboard_messages(self, guild_id):
        messages = self.session.query(StarBoardMessages).filter_by(server_id=guild_id).all()
        return messages

    async def get_one_starboard_message(self, guild_id, original_message_id):
        message = self.session.query(StarBoardMessages)\
            .filter_by(server_id=guild_id)\
            .filter_by(original_message_id=original_message_id).one_or_none()
        return message

    async def update_starboard_message(self, original_message_id, starboard_message_id=None, count=None):
        """
        Updates the message data based on the origional_message_id
        :param original_message_id: The ID used to fetch the message that will be updated
        :param starboard_message_id: The message ID found on the starboard if it is preset
        :param count: Number of votes
        :return:
        """
        was_updated = False
        message = self.session.query(StarBoardMessages).filter_by(original_message_id=original_message_id).one_or_none()
        if starboard_message_id is not None:
            message.starboard_message_id = starboard_message_id
            self.session.commit()
            was_updated = True
        if count is not None:
            message.count = count
            self.session.commit()
            was_updated = True
        if was_updated:
            return message
        else:
            return False

    async def post_starboard_message(self, guild_id, original_message_id, starboard_message_id=None, count=0):
        if await self.get_one_starboard_message(guild_id,original_message_id) is None:
            message = StarBoardMessages(server_id=guild_id,
                                        starboard_message_id=starboard_message_id,
                                        original_message_id=original_message_id,
                                        count=count)
            self.session.add(message)
            self.session.commit()
            return message
        else:
            return False

    async def get_reminders(self):
        return list(self.session.query(RemindMe).all())

    async def post_reminder(self, user_id:int, future:int, text:str):
        reminder = RemindMe(user_id=user_id,
                            future=future,
                            text=text,
                            completed=False)
        self.session.add(reminder)
        self.session.commit()

    async def delete_reminder(self, id):
        reminder = self.session.query(RemindMe).filter_by(id=id).delete()
        if reminder == 1:
            self.session.commit()
            return True
        else:
            return False
