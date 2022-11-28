from crontab import CronTab
import os

# # 定时器基本参数配置
dir_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
with open("{}/txt/config.txt".format(dir_path), encoding="utf-8") as f:
  config = eval(f.read())
cron = config["cron"]
command = "{} {}/py/main.py".format(cron["python3_path"], dir_path, dir_path)

myCron = CronTab(user=cron["username"])
oldCron = myCron.find_comment("leaveout")
for jobs in oldCron: # 删除原来的任务
  myCron.remove(jobs)
job = myCron.new(command=command, comment="leaveout") # 新建定时器任务
exec_time = config["cron"]["time"].split(":")
if exec_time[0] == "":
  job.minute.every(1)
else:
  job.hour.on(int(exec_time[0]))
  job.minute.on(int(exec_time[1]))
myCron.write()