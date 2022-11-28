# 每日请假 leaveout

## python 版本
- 首先需要运行命令 `pip3 install -r requirements.txt`
- 其次登录东南大学研究生请假系统后把 `config.txt` 文件里除最后一个之外的空字符串补全
- 接着终端运行命令 `where python3` 填入最后一个空字符串
- 然后将电脑的用户名填写入倒数第二个空字符串中
- 最后如果是 MAC 电脑运行 `cron.py` 文件，否则运行 `main.py`
- 运行日志存储在 log 文件夹下，按月份存储

> 注意：记得开启 crontab 任务，给 crontab 文件读写权限，否则不能执行，如果不能定时执行任务，那么单独运行 `main.py` 也可，用的python 版本为 `3.9.6`。
> 如果为 Windows 电脑，定时任务请自己设置，详情可以参考这篇[博客](https://blog.csdn.net/shammy_feng/article/details/124178086)。

## nodejs 版本
- 首先安装 nodejs，最好是最新的稳定版本
- 如果是第一次运行要在终端输入命令 `npm i` 安装 `node_module` 依赖项目
- 最后运行命令 `npm run leaveout` 等待请假完成
- 运行命令的时候要进入 nodejs 文件夹

> nodejs 版本不能每日定时执行，试了很多方式都没成功，同时只能请第二天的假，`config.js` 中的空字符串处与 python 版本一样填写即可