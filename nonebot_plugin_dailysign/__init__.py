from nonebot import on_fullmatch, require
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

from nene.utils_.config import Config
from nene.utils_.event import GroupEvent_, MessageEvent_, S
from nene.utils_.usrinfo import G,U

from .data_source import get_sign_in

require("nonebot_plugin_tortoise_orm")
from nonebot_plugin_tortoise_orm import add_model  # noqa: E402

add_model("nonebot_plugin_dailysign.models")

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


@sign.handle()
async def _(event: MessageEvent_):
    user_id = int(event.get_user_id())
    if isinstance(MessageEvent_,GroupEvent_):
        group_id = await G.get_group_id(event)
        group_id = int(group_id)
        logger.debug(f"群 group_id: 用户 {user_id} 签到")
        msg = await get_sign_in(user_id, group_id)
        await S.send_text(msg)
    else:
        user_id = await U.get_user_id(event)
