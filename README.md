# autoRecoder

inschool: 在学校的状态：
1: 在学校 2. 不在学校
isdes: 如果不在学校需要填写,如果在学校则不需要填写： 1. 请假了 2. 没有请假
reason: 没有请假的理由，如果在学校则不需要填写 1. 已经办理校外租房 2. 毕业生，已办理长假手续 3. 已经办理校外实习手续 4. 其他
本项目通过读取环境变量中的信息，进行奕辅导的自动化打卡,依次执行如下信息：

- 使用抓包软件获取`accessToken`
- 到[server 酱](https://sct.ftqq.com/)去注册并获取一个 SendKey,然后写入 github 关键字为`secret`
- 写入省份`province`：湖北省
- 写入城市`city`: 武汉市
- 写入区`area`: 武昌区
- 写入地址信息`address`：湖北省武汉市武昌区武汉大学
- 写入是否在学校`inschool`:
  value: 1. 在学校 2. 不在学校
- 写入请假状态`isdes`:
  **如果在学校填 0**

  value: 1. 请假了 2. 没有请假

- 写入请假理由`reason`:
  **如果在学校填 0**

  value: 1. 已经办理了校外租房 2. 毕业生，已办理长假手续 3. 已经办理校外实习手续 4. 其他

- 写入请假理由的描述`reasondes`:
  **如果在学校填 0**

  value: "寒假在家"

## usage

**强烈建议使用自动执行**

### github actions 自动执行

配置文件在[python-app.yml](https://github.com/TobiasHu2021/autoRepoter/blob/main/.github/workflows/python-app.yml)中修改 cron 选项中的时间配置，目前配置为每天北京时间 08 点 02 分 15 秒执行一次

#### github action 配置

- fork 本项目
- 在自己的 repo 下 Settings/Screts 中设置`accessToken`, `secret`, `latitude`, `longitude`, `province`, `city`, `area` 和 `address`。具体写法上面有样例
- 【可选】如果需要微信通知，可以配置 FT_SCKEY,为[ftqq 微信推送服务](http://sc.ftqq.com/?c=code)中的 sckey
- fork 的项目默认是关闭的，需要手动点击 repo 页的 actions 以 enable
