# **挖土豆超话自动打榜机V1.0 [ 用户版 ]**

---

## 项目结构：

- **image**  验证码素材图库
- **libs** 核心功能代码库
  - **Auto_sign.py**    自动登录模块
  - **Compare.py**    验证码图片比较模块
  - **contextLib.py**    截取的一些豆包们写的很好的评论，作文案库
  - **doComment.py**    自动评论模块
  - **goCenter.py**    送分和任务中心模块
  - **Login.py**       登录模块
  - **path_url_lib.py**     可能用到的 xpath 和 url 库
  - **readAccounts.py**    从 txt 文件读取账号模块
- **tools**
  - **chromedriver.exe**     selenium 功能的核心 浏览器引擎
  - **ChromeSetup.exe**    比较新的 Chrome 浏览器安装包，满足使用需求
- **account_set.txt**      可导入账号的文本文件
- **app.py**       主程序
- **captcha.png**     截取的轨迹验证码的主要部分
- **src.png**       截取的轨迹验证码的总体缩略图

---

## 新号打榜流程

1.  **login** 登录

2.  **focus & sign** 关注 主副超话，并签到

3.  **go to task_center & get scores** 进入送分中心，领取基础分数

4.  **make comments** 自动 8 条评论

5.  **send scores** 送分

  **假设第一天种下的土豆都发芽了，则分数会保存并积累到下一天。**
  **No.[2] 非常重要!!! 没有关注超话，在超话内发帖毫无意义！不会得分！**

---
验证码拖动部分的代码参考（其实是copy 23333）
https://github.com/zloveh/WeiBo_login
为了表示感谢，给了这位朋友 star
