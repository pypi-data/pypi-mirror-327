import httpx,nonebot
from.Login import topia_login

from pathlib import Path
from .config import Config
from nonebot import get_plugin_config
from nonebot.rule import to_me
from nonebot.params import EventMessage
from nonebot.plugin import on_message,on_command,PluginMetadata
from nonebot.adapters import Message
# 本地存储
from nonebot import require
import nonebot_plugin_localstore as store # type: ignore
require("nonebot_plugin_localstore")


## plugin meta data
__plugin_meta__= PluginMetadata(
    name= "ai_topia",
    description= "接入ai乌托邦pro对话",
    usage= "暂无",
    type= "application",
    homepage= "https://github.com/KanzakiD/nonebot-plugin-ai-topia",
)


## config
plugin_config= get_plugin_config(Config)
config= nonebot.get_driver().config

# api config
api_key= getattr(config, "ai_topia_key", "")
api_secret= getattr(config, "ai_topia_secret", "")
role_id= getattr(config, "ai_topia_roleid", "")


# token文件句柄
data_file= store.get_plugin_data_file("localstore.txt")


## 对话模块
mes= on_message(rule=to_me(),priority=plugin_config.ai_topia_priority)

@mes.handle()
async def handle_function(args: Message = EventMessage()):
    # 检测非空消息
    if user_content := args.extract_plain_text():

        # 是否获取过token，杜绝每次加载进行无意义post请求影响性能
        if data_file.exists():
            temp_token= data_file.read_text()
        else:
            # 执行login方法获取token，顺便检查配置是否填写
            temp_token= topia_login(api_key,api_secret)
            if api_key == "" or api_secret == "" or role_id == "" or temp_token == "error":
                await mes.finish("token请求失败，请检查配置填写")


        # body
        body= {'appUserId': '2', 'content': user_content, "roleId": role_id}
        headers= {'Content-Type': 'application/json; charset=utf-8','Authorization': f'Bearer {temp_token}'}
        sc_url= 'https://pro.ai-topia.com/apis/chat/sendChat'
        
        # post请求
        async with httpx.AsyncClient() as client:
            res= await client.post(
                sc_url,
                headers= headers,
                json= body
            )
            # 检查是否请求成功
            if res.status_code == 200:
                data= res.json()
                # 检查json合法并处理
                if "content" in data["data"]:
                    await mes.finish(data["data"]["content"])
                else:
                    await topia_login(api_key,api_secret)
                    await mes.send("数据结构不符合预期或token过期，已尝试重置token，请重新对话或检查apikey配置")
                    await mes.finish(f"数据为：{data}")
            else:
                await topia_login(api_key,api_secret)
                await mes.finish("请求失败，已尝试重置token，请重新对话或检查apikey配置")