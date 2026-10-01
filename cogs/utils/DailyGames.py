from datetime import datetime

from loguru import logger
from sqlalchemy import func, case

from .database import Database
from .dailygame_parser import GameResult
from create_databases import DailyGameChannels, DailyGameResults


class DailyGamesModel(Database):
    def __init__(self):
        super().__init__()
        # Create the tables on existing databases that predate this cog
        DailyGameChannels.__table__.create(bind=self.session.get_bind(), checkfirst=True)
        DailyGameResults.__table__.create(bind=self.session.get_bind(), checkfirst=True)

    def get_all_channel_ids(self):
        return {c.channel_id for c in self.session.query(DailyGameChannels).all()}

    async def get_channels(self, server_id: int):
        return self.session.query(DailyGameChannels).filter_by(server_id=server_id).all()

    async def add_channel(self, server_id: int, channel_id: int, user_id: int):
        if self.session.query(DailyGameChannels).filter_by(channel_id=channel_id).one_or_none() is not None:
            return False
        self.session.add(DailyGameChannels(server_id=server_id, channel_id=channel_id, added_by_user_id=user_id))
        self.session.commit()
        return True

    async def remove_channel(self, channel_id: int):
        channel = self.session.query(DailyGameChannels).filter_by(channel_id=channel_id).one_or_none()
        if channel is None:
            return False
        try:
            self.session.delete(channel)
            self.session.commit()
        except Exception as e:
            logger.error(e)
            self.session.rollback()
            return False
        return True

    async def get_result(self, server_id: int, user_id: int, result: GameResult):
        return self.session.query(DailyGameResults).filter_by(server_id=server_id,
                                                              user_id=user_id,
                                                              game_key=result.game_key,
                                                              mode=result.mode or '',
                                                              game_number=result.number).one_or_none()

    async def add_result(self, server_id: int, channel_id: int, user_id: int, result: GameResult):
        record = DailyGameResults(server_id=server_id,
                                  channel_id=channel_id,
                                  user_id=user_id,
                                  game=result.game,
                                  game_key=result.game_key,
                                  game_number=result.number,
                                  mode=result.mode or '',
                                  attempts=result.attempts,
                                  max_attempts=result.max_attempts,
                                  solved=result.solved,
                                  difficulty=result.difficulty,
                                  posted_at=datetime.now())
        self.session.add(record)
        self.session.commit()
        return record

    async def get_game_modes(self, server_id: int, game_key: str = None, mode: str = None):
        """Distinct (game, game_key, mode) combinations played on a server"""
        query = self.session.query(DailyGameResults.game, DailyGameResults.game_key, DailyGameResults.mode) \
            .filter_by(server_id=server_id)
        if game_key is not None:
            query = query.filter_by(game_key=game_key.lower())
        if mode is not None:
            query = query.filter_by(mode=mode.lower())
        return query.group_by(DailyGameResults.game_key, DailyGameResults.mode) \
            .order_by(DailyGameResults.game_key, DailyGameResults.mode).all()

    def _stats_query(self, server_id: int):
        return self.session.query(DailyGameResults.user_id,
                                  func.avg(DailyGameResults.attempts).label('average'),
                                  func.count(DailyGameResults.id).label('played'),
                                  func.sum(case((DailyGameResults.solved, 1), else_=0)).label('solved'),
                                  func.min(DailyGameResults.attempts).label('best')) \
            .filter(DailyGameResults.server_id == server_id)

    async def get_leaderboard(self, server_id: int, game_key: str, mode: str, min_played: int = 1, limit: int = 10):
        """Ranks players by lowest average attempts, ties broken by most games played"""
        return self._stats_query(server_id) \
            .filter(DailyGameResults.game_key == game_key, DailyGameResults.mode == mode) \
            .group_by(DailyGameResults.user_id) \
            .having(func.count(DailyGameResults.id) >= min_played) \
            .order_by(func.avg(DailyGameResults.attempts).asc(), func.count(DailyGameResults.id).desc()) \
            .limit(limit).all()

    async def get_user_stats(self, server_id: int, user_id: int):
        return self.session.query(DailyGameResults.game,
                                  DailyGameResults.mode,
                                  func.avg(DailyGameResults.attempts).label('average'),
                                  func.count(DailyGameResults.id).label('played'),
                                  func.sum(case((DailyGameResults.solved, 1), else_=0)).label('solved'),
                                  func.min(DailyGameResults.attempts).label('best')) \
            .filter(DailyGameResults.server_id == server_id, DailyGameResults.user_id == user_id) \
            .group_by(DailyGameResults.game_key, DailyGameResults.mode) \
            .order_by(DailyGameResults.game_key, DailyGameResults.mode).all()
