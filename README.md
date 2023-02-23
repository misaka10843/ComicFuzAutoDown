## ComicFuzAutoDown

定时检测comicFuz中的Kirara系列杂志更新，并且在有新内容时调用[misaka10843/ComicFuz-Down](https://github.com/misaka10843/ComicFuz-Down)进行下载

## 如何使用

请先添加给此程序每天11点运行，添加之后，本程序将会每天晚上11点检测三次（11点开始每五分钟检测一次）

如果检测到有新的杂志更新，会将杂志ID发送到**ComicFuz-Down**进行下载

## 为什么没看见使用API请求？

~~因为懒的写proto~~因为发现可以直接get网页后获取下一步渲染的数据（其中包括当前的杂志列表）

所以就直接get而不是再写个proto后解析API（虽然这样做可能更高效）

## setting.json配置

在您第一次启动了本程序后，将会提示您配置settings.json

其中，`account`中的两项为必填

`MagazineID`中的四项需要填写对应杂志的**最新**ID

如果不需要检测某一个，可以直接添加`null`
(ID的话比如`https://comic-fuz.com/magazine/25812`那么ID就是**25812**)

`outputPath`为下载到哪一个文件夹，请输入正确路径(选填)

`proxies`中的两项为代理地址(选填)

注意，下载使用的地址为`https`，获取资料等其他数据为两项自动使用
```json
{
  "outputPath": "",
  "account":{
    "mail":"",
    "password":""
  },
  "MagazineID":
  {
    "kirara": null,
    "max": null,
    "carat": null,
    "forward": null
  },
  "proxies":
  {
    "http": "",
    "https": ""
  }
}
```