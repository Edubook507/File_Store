# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import logging
from struct import pack
import re
import base64
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from config import DB_URI, DB_NAME , FSUB_CHANNEL2 , FSUB_CHANNEL1
# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

COLLECTION_NAME = "Telegram_Files"
JOIN_REQUESTS = "JOIN_REQUESTS"

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


client = AsyncIOMotorClient(DB_URI)
db = client[DB_NAME]
instance = Instance.from_db(db)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


async def get_file_details(query):
    filter = {'file_id': query}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    return filedetails

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref


# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

class JoinRequest():
    def __init__(self , CHANNEL_ID1 : int, CHANNEL_ID2 : int):
            self.channel_id1 = db[str(CHANNEL_ID1)]
            self.channel_id2 = db[str(CHANNEL_ID2)]
            print("JoinRequest Initialised : " , self.channel_id1 , self.channel_id2)
    async def add_join_req(self , user_id , channel_id):
        channel_id = str(channel_id)
        try:
            if channel_id not in [FSUB_CHANNEL1 , FSUB_CHANNEL2]:
                return
            col = self.channel_id1 if channel_id == str(FSUB_CHANNEL1) else self.channel_id2
            await col.update_one({"user_id":user_id},{"$set":{"user_id":user_id}} , upsert = True)
        except Exception as e:
            print('Error in add_join_req : ' , e)
            return
    async def remove_join_req(self , user_id , channel_id):
        try:
            channel_id = str(channel_id)
            if channel_id not in [FSUB_CHANNEL1 , FSUB_CHANNEL2]:
                return
            col = self.channel_id1 if channel_id == str(FSUB_CHANNEL1) else self.channel_id2
            await col.delete_one({"user_id":user_id})
        except Exception as e:
            print('Error in add_join_req : ' , e)
            return
    async def find_join_req(self , user_id , channel_id):
        try:
            channel_id = str(channel_id)
            if channel_id not in [FSUB_CHANNEL1 , FSUB_CHANNEL2]:
                return
            col = self.channel_id1 if channel_id == str(FSUB_CHANNEL1) else self.channel_id2
            return bool(await col.find_one({"user_id":user_id}))
        except Exception as e:
            print('Error in add_join_req : ' , e)
            return
        
joinReq = JoinRequest(FSUB_CHANNEL1 , FSUB_CHANNEL2)

