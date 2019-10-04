from create_databases import AuditLog, ServerSettings, Base, CustomCommands, Warnings, StarBoardSettings, BirthdaySettings, Birthdays
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import os
import discord
from datetime import datetime
from loguru import logger


class Database:
    def __init__(self):
        engine = create_engine("sqlite:///peribot.db", echo=True)
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

    async def get_server_settings(self, server_id):
        return self.session.query(ServerSettings).filter_by(server_id = server_id).first()

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
        return reports

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
        # role =
        # self.session.add(settings)
        # self.session.commit()

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

