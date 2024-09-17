from pyrogram import Client, filters, enums 
from pyrogram.types import ChatJoinRequest , Message , InlineKeyboardButton , InlineKeyboardMarkup
from config import FSUB_CHANNEL1 , FSUB_CHANNEL2
from .database import joinReq
from pyrogram.errors import ChatAdminRequired , UserNotParticipant
@Client.on_chat_join_request(filters.chat[FSUB_CHANNEL1 , FSUB_CHANNEL2])
async def join_reqs(client, message: ChatJoinRequest):
    try:
        await joinReq.add_join_req(message.from_user.id , message.chat.id)
    except Exception as e:
        print("Error in adding join request" , e)
        return
    
@Client.on_chat_member_updated(filters.chat(FSUB_CHANNEL1 , FSUB_CHANNEL2))
async def join_reqs(client, message: ChatJoinRequest):
    try:
        await joinReq.remove_join_req(message.from_user.id , message.chat.id)
    except Exception as e:
        print("Error in removing join request" , e)
        return
async def isJoined(client : Client , message : Message):
    try:
        for i in [FSUB_CHANNEL1 , FSUB_CHANNEL2]:
            try: 
                user = await client.get_chat_member(i , message.from_user.id)
            except UserNotParticipant:
                is_requested = await joinReq.find_join_req(message.from_user.id , i)
                if is_requested:
                    continue
                else:
                    invite_link1 = await client.create_chat_invite_link(FSUB_CHANNEL1, creates_join_request=True)
                    invite_link2 = await client.create_chat_invite_link(FSUB_CHANNEL2, creates_join_request=True)
                    btn = [[
                        InlineKeyboardButton('🔍 Join Updates Channel', url=f"{invite_link1.invite_link}")
                    ], 
                    [InlineKeyboardButton('🔍 Join Updates Channel', url=f"{invite_link2.invite_link}")]
                    ]
                    reply_markup = InlineKeyboardMarkup(btn)
                    return await message.reply(text="**Please Join Updates Channel To Use This Bot.**", reply_markup=reply_markup)
            except Exception as e:
                continue
        return True
    except Exception as e:
        print(e)
        return True