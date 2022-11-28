// 可以先请一次假把信息填了
const privateData = {
  DZQJSY_DISPLAY: "因事出校（当天往返）", // 请假类型
  QJXZ_DISPLAY: "因公", // 请假属性
  YGLX_DISPLAY: "实验", // 因公类型，如果QJXZ_DISPLAY填的因私这个就不填
  QJSY: "去无线谷努力科研", // 请假详情
  XXDZ: "江宁无线谷6102", // 详细地址
  JJLXR: "", // 紧急联系人
  JJLXRDH: "", // 紧急联系人电话
  JZXM: "", // 家长姓名
  JZLXDH: "", // 家长联系电话
  DSXM: "", // 导师姓名
  DSDH: "", // 导师电话
  FDYXM: "", // 辅导员姓名
  FDYDH: "", // 辅导员电话
}

const account = {
  username: "",
  password: "",
  // 登录研究生请假后的URL里的gid参数
  gid: ""
}

module.exports = {
  privateData,
  account
}