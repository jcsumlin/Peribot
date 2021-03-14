import datetime
import os

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean, Text, BIGINT
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ServerSettings(Base):
    __tablename__ = 'server_settings'
    server_id = Column(BIGINT, primary_key=True, unique=True)
    server_name = Column(String(255))
    prefix = Column(String(255))
    region = Column(String(255))
    owner_id = Column(BIGINT)
    is_premium = Column(Boolean)


class UserActivityLogs(Base):
    __tablename__ = 'user_activity_log'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    user_id = Column(BIGINT)
    last_online = Column(String(255))
    last_activity = Column(String(255))
    last_nickname = Column(String(255))

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    time = Column(DateTime)
    server_name = Column(String(255))
    command_invoked = Column(String(255))
    user_id = Column(BIGINT)


class CustomCommands(Base):
    __tablename__ = 'custom_commands'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    command = Column(String(255))
    result = Column(Text)
    added_by_user_id = Column(BIGINT)


class YoutubePlaylists(Base):
    __tablename__ = 'youtube_playlists'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    user_id = Column(BIGINT)
    youtube_link = Column(String(255))


class ReactionRolesGroups(Base):
    __tablename__ = 'reaction_roles_groups'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    enabled = Column(Boolean, default=False)
    group_name = Column(String(255))
    group_description = Column(String(255))

class ReactionRoleMessage(Base):
    __tablename__ = 'reaction_role_message'
    id = Column(Integer, autoincrement=True, primary_key=True)
    group_id = Column(Integer, ForeignKey('reaction_roles_groups.id'))
    message_id = Column(BIGINT)


class ReactionRoles(Base):
    __tablename__ = 'reaction_roles'
    id = Column(Integer, autoincrement=True, primary_key=True)
    group_id = Column(Integer, ForeignKey('reaction_roles_groups.id'))
    role_id = Column(BIGINT)
    role_name = Column(String(255))
    role_emoji = Column(String(255))


class AutoWelcomeSettings(Base):
    __tablename__ = 'auto_welcome_settings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    enabled = Column(Boolean, default=False)
    message = Column(Text)
    auto_role_enabled = Column(Boolean, default=False)


class AutoRole(Base):
    __tablename__ = 'auto_role'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('auto_welcome_settings.server_id'))
    role_id = Column(BIGINT)


class ModMailSettings(Base):
    __tablename__ = 'mod_mail_settings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    enabled = Column(Boolean, default=False)
    channel_id = Column(BIGINT)
    at_here = Column(Boolean)


class ModMailReports(Base):
    __tablename__ = 'mod_mail_reports'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('mod_mail_settings.server_id'))
    user_id = Column(BIGINT)
    date_time = Column(DateTime)
    report_message = Column(Text)


class ModMailReportReply(Base):
    __tablename__ = 'mod_mail_report_reply'
    id = Column(Integer, autoincrement=True, primary_key=True)
    report_id = Column(Integer, ForeignKey('mod_mail_reports.id'))
    mod_id = Column(Integer)
    date_time = Column(DateTime)
    reply_message = Column(Text)


class GiveawaySettings(Base):
    __tablename__ = 'giveaway_settings'
    giveaway_msg_id = Column(BIGINT, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    enabled = Column(Boolean, default=False)
    number_of_entries = Column(Integer)
    end_datetime = Column(DateTime)
    open_for_entries = Column(Boolean)
    name = Column(String(255))
    sponsor_user_id = Column(Integer)
    completed = Column(Boolean)


class GiveawayEntries(Base):
    __tablename__ = 'giveaway_entries'
    id = Column(Integer, autoincrement=True, primary_key=True)
    giveaway_msg_id = Column(BIGINT, ForeignKey('giveaway_settings.giveaway_msg_id'))
    user_id = Column(BIGINT)


class BirthdaySettings(Base):
    __tablename__ = 'birthday_settings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    enabled = Column(Boolean, default=False)
    channel_id = Column(BIGINT)
    message = Column(Text)


class Birthdays(Base):
    __tablename__ = 'birthday'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('birthday_settings.server_id'))
    user_id = Column(BIGINT)
    birthday = Column(Text)
    completed = Column(Boolean)


class RemindMe(Base):
    __tablename__ = 'remind_me'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(BIGINT)
    future = Column(Integer)
    text = Column(Text)
    completed = Column(Boolean)


class Warnings(Base):
    __tablename__ = 'warnings'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'), nullable=False)
    date = Column(DateTime, nullable=False)
    user_name = Column(String(32), nullable=False)
    user_id = Column(BIGINT, nullable=False)
    mod_name = Column(String(32), nullable=False)
    mod_id = Column(BIGINT, nullable=False)
    reason = Column(Text, nullable=False)


class StarBoardSettings(Base):
    __tablename__ = 'starboard_settings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    enabled = Column(Boolean, default=False)
    channel_id = Column(BIGINT, nullable=False)
    emoji = Column(String(255), nullable=False)
    threshold = Column(Integer, nullable=False)


class StarBoardIgnoredChannels(Base):
    __tablename__ = 'starboard_ignored_channels'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('starboard_settings.server_id'))
    channel_id = Column(BIGINT, nullable=False)


class StarBoardMessages(Base):
    __tablename__ = 'starboard_messages'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('starboard_settings.server_id'))
    starboard_message_id = Column(BIGINT)
    original_message_id = Column(BIGINT)
    count = Column(Integer)


class StarboardAllowedRoles(Base):
    __tablename__ = 'starbaord_roles'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('starboard_settings.server_id'))
    role_id = Column(BIGINT)


class ModerationLogSettings(Base):
    __tablename__ = 'moderation_log_settings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    enabled = Column(Boolean)
    channel_id = Column(BIGINT)
    join = Column(Boolean)
    leave = Column(Boolean)
    voicechat = Column(Boolean)
    msgedit = Column(Boolean)
    msgdelete = Column(Boolean)
    roleedit = Column(Boolean)
    ban = Column(Boolean)
    reactions = Column(Boolean)
    channels = Column(Boolean)
    nicknames = Column(Boolean)


class ModerationLog(Base):
    __tablename__ = 'moderation_log'
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    event_time = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    event_type = Column(String(255))
    event_description = Column(String(255))


class SecretSanta(Base):
    __tablename__ = "secret_santa"
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    user_id = Column(BIGINT)
    address = Column(String(255))
    note = Column(String(255))


class BookClub(Base):
    __tablename__ = "book_club"
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(BIGINT, ForeignKey('server_settings.server_id'))
    channel_id = Column(BIGINT)
    title = Column(String(255))
    interval = Column(Integer)
    start = Column(Integer)
    end = Column(Integer)


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:password@localhost:49154/db")
    Base.metadata.create_all(bind=engine)
