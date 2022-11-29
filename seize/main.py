import requests
import ddddocr
import os
import time
import asyncio
from pyppeteer import launch

awaitFun = asyncio.get_event_loop().run_until_complete

itemIdMap = {
  "九龙湖": {
    "乒乓球": 7,
    "篮球": 8,
    "排球": 9,
    "羽毛球": 10,
    "舞蹈": 11,
    "健身": 12,
    "武术": 13,
    "跆拳道": 14
  },
  "四牌楼": {
    "羽毛球": 15,
    "乒乓球": 16,
    "网球场": 17
  } 
}


async def getSessionID(config):
  """
    获取SessionID
  """
  browser = await launch({ "headless": True })
  page = await browser.newPage()
  await page.goto("http://yuyue.seu.edu.cn/eduplus/order/initOrderIndex.do?sclId=1&t_s=1669626323839&amp_sec_version_=1&gid_=SjNsdUphZEhWOTdCUHZUSXlvd2tXVzNkMkwrS3ZwaWhNeitKVUhPL0tRby9KYWxlbEZPaytEVVYySVFqOTdYVWRKUjgybFZmVU52SzdjUW10MFlST3c9PQ&EMAP_LANG=zh&THEME=golden")
  await page.waitForNavigation({ "waitUntil": "load", "timeout": 0 })
  await page.type("#username", config["username"])
  await page.type("#password", config["password"])
  await page.click('button[type="submit"]')
  await page.waitForNavigation({ "waitUntil": "load", "timeout": 0 })
  cookies = await page.cookies()
  await browser.close()
  return [elem for elem in cookies if elem["name"] == "JSESSIONID"][0]["value"]



def downloadImg(url, cookies): 
  """
    下载验证码图片
  """
  r = requests.get(url, cookies=cookies)
  # 写入图片
  with open("validateimage.png", "wb") as f:
    f.write(r.content)


def readConfig():
  """
    读取文件
  """
  dir_path = os.path.abspath(os.path.dirname(__file__))
  with open("{}/config.txt".format(dir_path), encoding="utf-8") as f:
    config = eval(f.read())
  return config


def getValidCode():
  """
    识别验证码
  """
  ocr = ddddocr.DdddOcr()
  with open('validateimage.png', 'rb') as f: 
    img_bytes = f.read()
  return ocr.classification(img_bytes)


def request(info, cookies):
  """
    发起预约请求
  """
  url = "http://yuyue.seu.edu.cn/eduplus/order/order/order/judgeUseUser.do?sclId=1"
  form = {
    "ids": "",
    "useTime": "{} {}".format(info["date"], info["time"]),
    "itemId": info["itemId"],
    "allowHalf": 2,
    "validateCode": info["code"],
    "phone": info["phone"],
    "remark": "",
    "useUserIds": ""
  }
  response = requests.post(url=url, data=form, cookies=cookies)
  result = response.content.decode()
  return "新增预约成功" in result


def seize(JSESSIONID, runtime):
  """
    抢场地
  """
  maxExecTime = runtime
  execStart = time.time()
  cookies = { "JSESSIONID": JSESSIONID }
  cntFail = 0
  while True:
    downloadImg(url, cookies)
    code = getValidCode()
    info = { **config, "code": code, "itemId": itemId }
    flag = request(info, cookies)
    execEnd = time.time()
    if flag: return "预约成功"
    if execEnd - execStart >= maxExecTime: return "已到达最大尝试时间"
    cntFail += 1
    if cntFail % 10 == 0:
      print("已经完成第{}次请求, 但预约失败...".format(cntFail))


if __name__ == "__main__":
  os.system("clear")
  url = "http://yuyue.seu.edu.cn/eduplus/validateimage"
  config = readConfig()
  itemId = itemIdMap[config["place"]][config["type"]]
  print("开始获取 cookie, 请等待...")
  JSESSIONID = awaitFun(getSessionID(config=config))
  print("登录所需 cookie 已经获取完成!")
  start = time.time()
  result = seize(JSESSIONID, config["runtime"])
  print(result)
  end = time.time()
  print("用时: {} 秒".format(end - start))