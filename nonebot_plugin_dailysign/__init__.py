from nonebot.log import logger
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_fullmatch

from nene.utils_.usrinfo import U
from nene.utils_.config import Config
from nene.utils_.event import S, MessageEvent_

from .data_source import bind_login, get_sign_in, check_login_msg

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_dailysign",
    description="简单的签到插件",
    usage="发送 签到 即可",
    type="application",
    homepage="https://github.com/Agnes4m/nonebot-plugin-dailysign",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

sign = on_fullmatch("签到", priority=5, block=False)
bind = on_command("绑定", priority=5, block=False)
check_bind = on_command("登录信息", aliases={"绑定信息"}, priority=5, block=False)


@sign.handle()
async def _(event: MessageEvent_):
    user_id = await U.get_user_id(event)
    logger.info(user_id)
    if not user_id:
        return
    logger.debug(f"用户 {user_id} 签到")
    msg = await get_sign_in(user_id,event)
    await S.send_text(msg)

@bind.handle()
async def _(event:MessageEvent_,arg:Message = CommandArg()):
    text = arg.extract_plain_text()
    if await bind_login(text,event):
        await S.send_text("绑定成功，可使用`绑定信息`指令查看")
    else:
        ...
        # await S.send_text("绑定出错了..")
    
@check_bind.handle()
async def _(event:MessageEvent_,):
    data = await check_login_msg(event)
    if data is not None:
        msg = f"""
        'qq': {data.qq}
        'qq频道': {data.qqguild}
        'kook': {data.kook}
        'Telegram': {data.Telegram}
        'Discord': {data.Discord}
        'Bilibili': {data.Bilibili}
        'Arcaea': {data.Arcaea}
        'Phigros': {data.Phigros}
        """.strip()
        await S.send_text(msg)
    else:
        await S.send_text("没有绑定信息")
