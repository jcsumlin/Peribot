from .database import Database
from create_databases import BookClub
from loguru import logger


class BookClubModel(Database):
    def __init__(self):
        super().__init__()

    async def add(self, server_id: int, channel_id: int, title: str, interval: int, start: int):
        new = BookClub(
            server_id=server_id,
            channel_id=channel_id,
            title=title,
            interval=interval,
            start=start,
            end=(start + interval) - 1,
        )
        self.session.add(new)
        self.session.commit()
        return new

    async def delete(self, record: BookClub):
        try:
            self.session.delete(record)
            self.session.commit()
        except Exception as e:
            logger.error(e)
            return False
        return True

    async def save(self):
        return self.session.commit()

    async def get_by_channel_id(self, channel_id: int):
        bc = self.session.query(BookClub).filter_by(channel_id=channel_id).one_or_none()
        return bc

    async def get_all(self):
        return self.session.query(BookClub).all()


