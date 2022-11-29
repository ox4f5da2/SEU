import asyncio
import json
import sys
import os
import time

import requests
from pyppeteer import launch

awaitFun = asyncio.get_event_loop().run_until_complete
dir_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def readTxt(path):
  """
    读取文件
  """
  try:
    print("{}/txt/{}".format(dir_path, path))
    with open("{}/txt/{}".format(dir_path, path), encoding="utf-8") as f:
      config = eval(f.read())
  except FileNotFoundError:
    writeLog(startTime, "请检查文件是否与程序位于同一路径", "")
    sys.exit(1)
  except SyntaxError:
    writeLog(startTime, "请检查配置文件格式是否正确", "")
    sys.exit(1)
  return config


def getTime(delta):
  """
    获取指定请假的开始和结束时间
  """
  currentTime = time.localtime(time.time() + delta * 3600 * 24)
  timeData = {
    "QJKSRQ": time.strftime("%Y-%m-%d 00:00", currentTime),
    "QJJSRQ": time.strftime("%Y-%m-%d 23:59", currentTime)
  }
  return timeData


def getCurrentTime():
  """
    获取指定时间
  """
  currentTime = time.localtime(time.time())
  timeData = {
    "XJSJ": time.strftime("%Y-%m-%d+%H:%M:%S", currentTime),
    "XJRQ": time.strftime("%Y-%m-%d", currentTime)
  }
  return timeData


def getYearAndMonth():
  """
    获取当前年份和月份
  """
  currentTime = time.localtime(time.time())
  return time.strftime("%Y-%m", currentTime)


async def getCookie(url, account, cookieName):
  """
    获取指定键值的cookie
  """
  browser = await launch({ "headless": True })
  page = await browser.newPage()
  if cookieName == "_WEU":
    url = url.replace("xxxxxx", str(int(time.time() * 1000))).replace("yyyyyy", account["gid"])
  
  await page.goto(url)
  await page.type("#username", account["username"])
  await page.type("#password", account["password"])
  if cookieName == "_WEU":
    await page.click('button[type="submit"]')
  else:
    await page.click("#xsfw")
  await page.waitForNavigation({ "waitUntil": "load", "timeout": 0 })
  cookies = await page.cookies()
  await browser.close()
  return [elem for elem in cookies if elem["name"] == cookieName][0]["value"]


def xj(common, config, cookies, cnt, maxFailNum):
  """
    销假
  """
  if cnt > maxFailNum: return "销假已经达到最大次数!"
  pageSize = 1000
  url = common["pageURL"][2]
  data = { "XSBH": config["account"]["username"], "pageSize": pageSize, "pageNumber": 1 }
  while True:
    response = requests.post(url=url, cookies=cookies, data=data)
    records = json.loads(response.content.decode())["datas"]["wdqjbg"]
    totalSize = records["totalSize"]
    qj_records = [elem for elem in records["rows"] if elem["XJZT"] == "0"] # 获取未请假的记录
    currentTime = getCurrentTime()
    num = len(qj_records)
    flag = True
    for item in qj_records:
      form = { 
        "data": json.dumps({
          "SQBH": item["SQBH"],
          "XSBH": int(item["XSBH"]),
          "SHZT": item["SHZT_DISPALY"],
          "SQR": item["XSBH"],
          "THZT": item["THZT"],
          "SQRXM": item["XM"],
          "XJFS": "2",
          "XJSJ": currentTime["XJSJ"],
          "XJRQ": currentTime["XJRQ"],
        })
      }
      response = requests.post(url=common["pageURL"][3], cookies=cookies, data=form)
      status = json.loads(response.content.decode())["description"]
      if status == "成功": num -= 1
    if num > 0: flag = False
    if pageSize * data["pageNumber"] >= totalSize: break
    data["pageNumber"] += 1
  if not flag: 
    xj(common, config, cookies, cnt + 1, maxFailNum)
  return "销假全部完成!"
  

def qj(common, qj_data, cookies, cnt, maxFailNum):
  """
    请假
  """
  if cnt > maxFailNum: return "销假已经达到最大次数!"
  response = requests.post(url=common["pageURL"][4], cookies=cookies, data={ "data": json.dumps(qj_data) })
  status = json.loads(response.content.decode())["description"]
  if status != "成功":
    qj(common, qj_data, cookies, cnt + 1, maxFailNum)
  return "请假成功!"


def writeLog(startTime, res1, res2):
  """
    打印日志
  """
  dirname = "{}/log".format(dir_path)
  filename = "{}/{}-log.txt".format(dirname, getYearAndMonth())
  if not os.path.exists(dirname):
    os.mkdir(dirname)
  if not os.path.exists(filename):
    os.system(r"touch {}".format(filename))
  log = open(filename, mode="a")
  log.write("---------- start ----------\n运行程序时间: {}\n{}\n{}\n---------- end ----------\n\n".format(startTime, res1, res2))


if __name__ == "__main__":
  startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
  config = readTxt("config.txt")
  common = readTxt("common.txt")
  timeData = getTime(config["cron"]["delta"])
  qj_data = { **config["privateData"], **common["commonData"], **timeData }
  MOD_AUTH_CAS = awaitFun(getCookie(common["pageURL"][0], config["account"], "MOD_AUTH_CAS"))
  _WEU = awaitFun(getCookie(common["pageURL"][1], config["account"], "_WEU"))
  cookie = { "MOD_AUTH_CAS": MOD_AUTH_CAS, "_WEU": _WEU }
  res1 = xj(common, config, cookie, 0, 10)
  res2 = qj(common, qj_data, cookie, 0, 10)
  writeLog(startTime, res1, res2)