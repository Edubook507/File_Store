from pyrogram import Client
from pyrogram.types import  Message , InlineKeyboardButton , InlineKeyboardMarkup
from config import FSUB_CHANNEL1 , FSUB_CHANNEL2 , BOT_USERNAME
from .database import joinReq
from pyrogram.errors import UserNotParticipant
async def isJoined(client : Client , message : Message , command= None):
    try:
        if not FSUB_CHANNEL1 or not FSUB_CHANNEL2 :
            return True
        for i in [FSUB_CHANNEL1 , FSUB_CHANNEL2]:
            try: 
                await client.get_chat_member(i , message.from_user.id)
            except UserNotParticipant:
                is_requested = await joinReq.find_join_req(message.from_user.id , i)
                if is_requested:
                    continue
                else:
                    invite_link1 = await client.create_chat_invite_link(FSUB_CHANNEL1, creates_join_request=True)
                    invite_link2 = await client.create_chat_invite_link(FSUB_CHANNEL2, creates_join_request=True)
                    btn = [[
                        InlineKeyboardButton('ᴄʜᴀɴɴᴇʟ1', url=f"{invite_link1.invite_link}"),
                        InlineKeyboardButton('ᴄʜᴀɴɴᴇʟ2', url=f"{invite_link2.invite_link}") 
                    ], 
                    [InlineKeyboardButton('♻️ ɢᴇᴛ ғɪʟᴇ ♻️', url=f"https://t.me/{BOT_USERNAME}?start={command}") if command else InlineKeyboardButton('♻️ ᴛʀʏ ᴀɢᴀɪɴ ♻️', url=f"https://t.me/{BOT_USERNAME}?start=try")]
                    ]
                    reply_markup = InlineKeyboardMarkup(btn)
                    await message.reply(text="**Please Join Channel1 & Channel2 To Use This Bot.**", reply_markup=reply_markup)
                    return False            
            except Exception as e:
                continue
        return True
    except Exception as e:
        print(e)
        return True
