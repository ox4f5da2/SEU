# SEU
- [SEU](#seu)
  - [每日请假 leaveout](#每日请假-leaveout)
    - [python 版本](#python-版本)
      - [额外功能](#额外功能)
      - [注意⚠️](#注意️)
    - [nodejs 版本](#nodejs-版本)
  - [抢场馆 seize](#抢场馆-seize)
    - [python 版本](#python-版本-1)
      - [注意⚠️](#注意️-1)
  - [开源协议](#开源协议)



## 每日请假 leaveout

### python 版本
- 首先需要运行命令 `pip3 install -r requirements.txt`，这里需要终端运行地址与 `requirements.txt` 文件所在位置关系
- 其次登录 **东南大学网上办事服务大厅** 的 **研究生请假审批** 服务后打开任意一次请假记录，把 `config.txt` 文件里除最后一个之外的 **空字符串** 补全
- 接着终端运行命令 `where python3` 填入最后一个空字符串，即 `python3_path` 所对应的值
- 然后将电脑的 **用户名** 填写入倒数第二个空字符串中，即 `username` 所对应的值
- 最后如果是 MAC 电脑运行 `cron.py` 文件就能开启每日定时执行，否则运行 `main.py`
- 运行日志存储在 `log` 文件夹下，按 **月份存储**


#### 额外功能
现在支持多人同时请假(可以找你同学帮忙，如果不介意告诉他/她你东大的账号密码)，那么只要在 `config.txt` 文件中在 **users** 字段里按照规则增加即可(不限人数)，同时也丰富了打印日志的格式😊

#### 注意⚠️

- 记得开启 crontab 任务，给 crontab 文件读写权限，否则不能执行如果不能定时执行任务，那么单独运行 `main.py` 也可
- **单独运行表示想当前时刻立即请假**，本人使用的 python 版本为 `3.9.6`
- 如果更改了 `config.txt` 文件中的 `cron.time` 的值，需要重新运行 `cron.py` 文件才能重新开启新的定时器
- 如果使用的 Windows 系统，定时任务需要自己手动设置，详情可以参考这篇[博客](https://blog.csdn.net/shammy_feng/article/details/124178086)，不保证一定能设置成功。



### nodejs 版本
- 首先安装 nodejs，最好是最新的稳定版本
- 如果是第一次运行要在终端输入命令 `npm i` 安装 `node_module` 依赖项目
- 最后运行命令 `npm run leaveout` 等待请假完成
- 运行命令的时候要进入 nodejs 文件夹

> nodejs 版本不能每日定时执行，试了很多方式都没成功，同时只能请第二天的假，`config.js` 中的空字符串处与 python 版本一样填写即可



## 抢场馆 seize

### python 版本
- 首先需要运行命令 `pip3 install -r requirements.txt`，这里需要终端运行地址与 `requirements.txt` 文件所在位置关系
- 接着登录[场馆预约系统](http://yuyue.seu.edu.cn/eduplus/order/initOrderIndex.do?sclId=1)选择好要抢的场地地点填入 `config.txt` 文件中的 **place** 字段中，将要抢场地的类型段填入 **type** 字段中，将要抢的时间填入 **time** 和 **date** 字段中
- 然后填写好自己的手机号、账号和密码
- 最后运行 `main.py` 即可，等待程序执行完成



#### 注意⚠️

`config.txt` 文件中的 **runtime** 字段表示程序运行的最大时间(**单位是秒**)，如果超过运行时间还未抢到会自动终止程序，所以可以早上起来后保持电脑处于开机状态，设定好时间，就可以等待程序执行完成；或者可以使用定时任务，在运行时间段保持电脑可运行程序即可。

> 举个例子🌰：如果在早上九点开始抢场馆，且设置的 **runtime** 为 `240`，那么可以在早上 `8:58` 左右运行程序即可，如果预约成功会提前终止，否则在 `9:02` 左右自动结束。



## 开源协议

[MIT 协议](./LICENSE)