from .database import Database
from create_databases import SecretSanta


class SecretSantaModel(Database):
    def __init__(self):
        super().__init__()

    async def add(self, user_id: int, address: str, server_id: int, note: str = ""):
        new = SecretSanta(
            user_id=user_id,
            server_id=server_id,
            address=address,
            note=note
        )
        self.session.add(new)
        return self.session.commit()

    async def get_by_user_id(self, user_id:int):
        return self.session.query(SecretSanta).filter_by(user_id=user_id).one_or_none()

    async def get_all(self, guild_id):
        return self.session.query(SecretSanta).filter_by(server_id=guild_id).all()



