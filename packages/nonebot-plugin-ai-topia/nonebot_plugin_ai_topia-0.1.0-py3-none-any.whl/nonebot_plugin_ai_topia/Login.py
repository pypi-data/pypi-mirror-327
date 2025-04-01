import httpx
from .config import Config
from nonebot import get_plugin_config

# 本地存储
from nonebot import require
import nonebot_plugin_localstore as store # type: ignore
require("nonebot_plugin_localstore")
from pathlib import Path


async def topia_login(key,secret):


    url= "https://pro.ai-topia.com/apis/login"
    headers= {"Content-Type": "application/json; charset=utf-8"}
    body= {"appId": key,"appSecret": secret} 

    async with httpx.AsyncClient() as client:
        res= await client.post(
            url,
            headers= headers,
            json= body
        )
        

        # 检查返回内容合法
        if res.status_code == 200 and "access_token" in res.json()["data"]:
            data = res.json()
            # 存储token并返回ture
            data_file = store.get_plugin_data_file("localstore.txt")
            data_file.write_text(data["data"]["access_token"])