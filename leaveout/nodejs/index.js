const dayjs = require('dayjs');
const puppeteer = require('puppeteer');
const request = require('request');
const cron = require('node-cron');
const { privateData, account } = require('./config.js');
const { commonData, pageURL } = require('./content.js');

const time = +new Date() + 3600 * 24 * 1000
const qj_data = Object.assign({
  QJKSRQ: dayjs(time).format("YYYY-MM-DD 00:00"),
  QJJSRQ: dayjs(time).format("YYYY-MM-DD 23:59"),
}, commonData, privateData);
let maxFailNum = 10; // 最大请求次数
let cnt = 0; // 已经请求的次数
let noLeaved = 0;

addLeaveOutRecord();

// cron.schedule("0 * * * * *", () => {
//   cnt = 0;
//   addLeaveOutRecord();
//   console.log('每分钟在第 0 秒运行一个任务');
// })

/***************************************************************************/

function addLeaveOutRecord() {
  Promise.all([
    getCookie(pageURL[0], account, "MOD_AUTH_CAS"),
    getCookie(pageURL[1], account, "_WEU")
  ])
    .then(res => {
      let cookie = `MOD_AUTH_CAS=${res[0]}; _WEU=${res[1]};`;
      xj(cookie); // 销假
      cnt = 0; // 归零
      qj(cookie); // 请假
    })
}

async function getCookie(url, account, cookieName) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  if (cookieName === "_WEU") {
    url = url.replace("xxxxxx", +new Date()).replace("yyyyyy", account.gid);
  }
  await page.goto(url);
  await page.type('#username', account.username);
  await page.type('#password', account.password);
  if (cookieName === "_WEU") {
    await page.click('button[type="submit"]');
  } else {
    await page.click('#xsfw');
  }
  await page.waitForNavigation({
    waitUntil: 'load',
    timeout: 0
  });
  const cookies = await page.cookies();
  const res = cookies.filter(v => v.name === cookieName)[0].value;
  await browser.close();
  return res;
}

function xj(cookie) {
  if (cnt < maxFailNum) cnt++;
  else {
    console.log("销假已经到达最大请求次数！");
    cnt = 0;
    return
  };
  request.post({
    url: pageURL[2],
    headers: {
      "cookie": cookie,
    },
    form: {
      XSBH: account.username,
      pageSize: 100,
      pageNumber: 1
    }
  }, function (error, response, body) {
    if (response.statusCode === 200) {
      const res = JSON.parse(body).datas.wdqjbg.rows;
      // 获取未请假的条目
      const unleaveItem = res.filter(item => item.XJZT === "0");
      noLeaved = unleaveItem.length;
      if (noLeaved) {
        unleaveItem.forEach(item => {
          const { SQBH, XSBH, SHZT_DISPALY, XM, THZT } = item;
          // 对每一条进行请假
          request.post({
            url: pageURL[3],
            headers: {
              "Cookie": cookie,
            },
            form: {
              data: JSON.stringify({
                SQBH: SQBH,
                XSBH: +XSBH,
                SHZT: SHZT_DISPALY,
                SQR: XSBH,
                SQRXM: XM,
                THZT: THZT,
                XJFS: "2",
                XJSJ: dayjs().format('YYYY-MM-DD+HH:mm:ss'),
                XJRQ: dayjs().format('YYYY-MM-DD'),
              })
            }
          }, function (error, response, body) {
            body.description === "成功" && noLeaved--;
          })
        })
      }
    }
  })
  if (!noLeaved) console.log("销假成功！");
  else xj();
}

function qj(cookie) {
  if (cnt < maxFailNum) cnt++;
  else {
    console.log("请假已经到达最大请求次数！");
    return
  };
  request.post({
    url: pageURL[4],
    headers: {
      "Cookie": cookie
    },
    form: {
      data: JSON.stringify(qj_data)
    }
  }, function (error, response, body) {
    if (body.indexOf("成功") === -1) qj();
    else console.log("请假成功！");
  });
}