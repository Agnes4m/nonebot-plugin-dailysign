from datetime import date

from nonebot.log import logger

from nene.utils_.event import MessageEvent_
from nene.utils_.models import DailySign, LoginTable


async def get_sign_in(user_id: int,event:MessageEvent_):
    msg: str = ""
    usr_id = await LoginTable.get_user_info(event)
    if usr_id:
        ...
        # user_id = int(usr_id.qq)
    last_sign = await DailySign.get_last_sign(user_id,event)
    # 判断是否已签到
    today = date.today()
    logger.debug(f"last_sign: {last_sign}")
    logger.debug(f"today: {today}")
    if today == last_sign:
        msg = "你今天已经签到了，不要贪心噢。"
        return msg

    # 签到名次
    sign_num = await DailySign.filter(last_sign=today).count() + 1

    # 设置签到
    data = await DailySign.sign_in(user_id=user_id)

    msg_txt = f"本群第 {sign_num} 位 签到完成\n"
    msg_txt += f"获得金币：+{data.today_gold} (总金币：{data.all_gold})\n"
    msg_txt += f"累计签到次数：{data.sign_times}\n"
    msg_txt += f"连续签到次数：{data.streak}\n"
    msg += msg_txt
    return msg

async def check_login_msg(event:MessageEvent_):
    return await LoginTable.get_user_info(event)

def split_text_and_number(text:str):
    """文字与数字分离"""
    string_part = ""
    number_part = ""

    for char in text:
        if char.isdigit():
            number_part += char
        else:
            string_part += char

    # 将数字部分转换为整数
    if number_part:
        number_part = int(number_part)

    return string_part, number_part

async def bind_login(text,event):
    platform,account_number = split_text_and_number(text)
    if not account_number:
        account_number = None
    return await LoginTable.create_login(event,platform,account_number)