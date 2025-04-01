<!--
 * @Author         : kanzakiD
 * @Date           : 2024-02-10 00:00:00
 * @LastEditors    : kanzakiD
 * @LastEditTime   : 2021-02-10 00:00:00
 * @Description    : None
 * @GitHub         : https://github.com/KanzakiD/nonebot-plugin-ai-topia
-->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-ai-topia

_✨ NoneBot2 AI乌托邦对话插件 ✨_


</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot_plugin_ai_topia">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_ai_topia.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
</p>

## 更新记录
2025/2/12
整体功能已完成

## 使用方式
首先去插件目录找config.py 填写乌托邦的apikey、secret和roleId

私聊或群聊@机器人 即可对话


## 安装（没发到pypi和nonebot商店，以下都暂时用不了喵）

1. 使用 nb-cli 安装，不需要手动添加入口，更新使用 pip (推荐)

```
nb plugin install nonebot_plugin_ai_topia
```

2. 使用 pip 安装和更新，初次安装需要手动添加入口 （新版默认不带 bot.py 文件）

```
pip install --upgrade nonebot_plugin_ai_topia
```

pip 安装后在 Nonebot2 入口文件（例如 bot.py ）增加：

```python
nonebot.load_plugin("nonebot_plugin_ai_topia")
```
