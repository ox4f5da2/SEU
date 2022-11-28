# 每日请假 leaveout

## python 版本
- 首先需要运行命令 `pip3 install -r requirements.txt`，这里需要终端运行地址与 `requirements.txt` 文件所在位置关系
- 其次登录[东南大学研究生请假系统](http://ehall.seu.edu.cn/amp3/index.html#/home)的`研究生请假审批`服务后打开任意一次请假记录，把 `config.txt` 文件里除最后一个之外的 **空字符串** 补全
- 接着终端运行命令 `where python3` 填入最后一个空字符串，即 `python3_path` 所对应的值
- 然后将电脑的 **用户名** 填写入倒数第二个空字符串中，即 `username` 所对应的值
- 最后如果是 MAC 电脑运行 `cron.py` 文件就能开启每日定时执行，否则运行 `main.py`
- 运行日志存储在 `log` 文件夹下，按 **月份存储**

> 注意：记得开启 crontab 任务，给 crontab 文件读写权限，否则不能执行。如果不能定时执行任务，那么单独运行 `main.py` 也可，**单独运行表示想当前时刻立即请假**，本人使用的 python 版本为 `3.9.6`。
> 如果为 Windows 电脑，定时任务请自己设置，详情可以参考这篇[博客](https://blog.csdn.net/shammy_feng/article/details/124178086)。


## nodejs 版本
- 首先安装 nodejs，最好是最新的稳定版本
- 如果是第一次运行要在终端输入命令 `npm i` 安装 `node_module` 依赖项目
- 最后运行命令 `npm run leaveout` 等待请假完成
- 运行命令的时候要进入 nodejs 文件夹

> nodejs 版本不能每日定时执行，试了很多方式都没成功，同时只能请第二天的假，`config.js` 中的空字符串处与 python 版本一样填写即可