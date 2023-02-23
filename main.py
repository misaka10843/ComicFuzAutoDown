import os

import requests

from bs4 import BeautifulSoup

from rich import print
from rich import print_json
from rich.console import Console

import json

console = Console()

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0 "
                  ".4664.55 Safari/537.36 Edg/96.0.1054.34 "
}
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}
account ={}
outputPath = ""
def getID():
    global proxies,account,outputPath
    if not os.path.isfile('./settings.json') or os.path.getsize('./settings.json') == 0:
        preSettings = {
            "outputPath": "",
            "account":{
                "mail":"",
                "password":""
            },
            "MagazineID":
                {
                    "kirara": None,
                    "max": None,
                    "carat": None,
                    "forward": None
                },
            "proxies":
                {
                    "http": "",
                    "https": ""
                }
        }
        with open('./settings.json', 'wb') as file:
            file.write(json.dumps(preSettings, indent=4, ensure_ascii=False).encode())
            file.close()
        print("[bold yellow]检测到您可能是第一次启动本程序，请打开settings.json进行相关配置！")
        exit()
    with open('./settings.json', 'r') as file:
        settings = json.load(file)
    if not settings["account"]["mail"] or not settings["account"]["password"]:
        print("[bold red]请在settings.json中按照README填写账号与密码！")
        exit()
    else:
        account = settings["account"]
    outputPath = settings["outputPath"]
    if settings["proxies"]["http"] and settings["proxies"]["https"]:
        proxies = {
            "http": settings["proxies"]["http"],
            "https": settings["proxies"]["https"]
        }
        print("[blue]检测到代理设置，接下来将全程使用代理")
    if settings["MagazineID"]["kirara"]:
        getMagazineInfo(settings["MagazineID"]["kirara"], "kirara")
    if settings["MagazineID"]["max"]:
        getMagazineInfo(settings["MagazineID"]["max"], "max")
    if settings["MagazineID"]["carat"]:
        getMagazineInfo(settings["MagazineID"]["carat"], "carat")
    if settings["MagazineID"]["forward"]:
        getMagazineInfo(settings["MagazineID"]["forward"], "forward")


def getMagazineInfo(ID: int, magazineType: str):
    infoHtml = requests.get("https://comic-fuz.com/magazine/" + str(ID), proxies=proxies, headers=headers)
    soup = BeautifulSoup(infoHtml.content, 'html.parser')
    magazineInfo = soup.find("script", id="__NEXT_DATA__").get_text()
    magazineNowID = json.loads(magazineInfo)["props"]["pageProps"]["magazineIssues"][0]["magazineIssueId"]
    if magazineNowID >= ID:
        print(f"[blue]正在下载MangaTime {magazineType}")
        if proxies["https"]:
            proxyArg = "-y "+proxies["https"].replace('http://', '').replace('https://', '')
        else:
            proxyArg = ""
        print(proxyArg)
        if outputPath:
            try:
                os.system(f"python ./fuzDown/fuz_down.py -u {account['mail']} -p {account['password']} -t token.txt -j 16 -z {ID} -o {outputPath} {proxyArg}")
            except Exception as e:
                print("[bold red]下载程序出错！请检查上方的输出，如果没有提示请直接复制整个输出然后提出issue")
                exit()
        else:
            try:
                os.system(f"python ./fuzDown/fuz_down.py -u {account['mail']} -p {account['password']} -t token.txt -j 16 -z {ID} {proxyArg}")
            except Exception as e:
                print("[bold red]下载程序出错！请检查上方的输出，如果没有提示请直接复制整个输出然后提出issue")
                exit()
        # 更新最新的ID
        with open('./settings.json', 'r') as file:
            settings = json.load(file)
        with open('./settings.json', 'w+') as file:
            settings["MagazineID"][magazineType] = ID
            file.write(json.dumps(settings, indent=4, ensure_ascii=False))
    else:
        print(f"[blue]MangaTime {magazineType}暂时没有新的杂志发布")


def downloadPb2():
    if not os.path.exists("./fuzDown/fuz_pb2.py"):
        print("[yellow]检测到您似乎并没有fuz_pb2.py,正在为您下载中")
        down_res = requests.get("https://github.com/misaka10843/ComicFuz-Down/releases/download/proto-V0.1"
                                "/fuz_pb2.py", proxies=proxies)
        with open("./fuzDown/fuz_pb2.py", 'wb') as file:
            file.write(down_res.content)
        print("[green]下载成功！正在为您继续执行")


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    downloadPb2()
    getID()