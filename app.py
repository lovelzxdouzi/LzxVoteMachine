from libs.readAccounts import *
from libs.Auto_Sign import *
from libs.goCenter import *
from libs.putSeed import *
from libs.Status import *


"""
 超话打榜规则：
 8 个 超话签到
 8 次 帖子评论
 20 个 被评论
"""

# main app:
if __name__ == '__main__':
    """
    # 新小号打榜流程
    1. login 登录
    2. focus & sign 关注 主副超话，并签到
    3. go to task_center & get scores 进入送分中心，领取基础分数
    4. make comments 自动 8 条评论
    5. send scores 送分
    
    # 假设第一天种下的土豆都发芽了，则分数会保存并积累到下一天。
    # No.[2] 非常重要!!! 没有关注超话，在超话内发帖毫无意义！不会得分！
    """
    global result
    accounts = readAccounts().get()
    for name, pswd in accounts.items():
        driver = webdriver.Chrome()
        try:
            print('账号：{} 正在打榜：'.format(name))
            # TODO: 设置进度记录仪
            driver = Login(driver, name, pswd).run()
            print('操作进度：登录完成')

            # TODO：登录之后一定要检测一下是否登陆成功！

            driver = goCenter(driver).run()
            print('操作进度：领分完成')
            driver = AutoSign(driver).run()
            print('操作进度：自动签到完成')
            driver = doComments(driver).run()
            print('操作进度：自动评论完成')

            driver = putSeed(driver).run()
            print('操作进度：播种完成')
            driver = goCenter(driver).sendScore()

            driver.close()
        except TimeoutException as t:
            print(u'出现超时现象。挖土豆机已经终止')
            driver.close()
            pass
        except WebDriverException as e:
            print(e)
            print(u'挖土豆机浏览器引擎出现问题，当前账号打榜已终止。')
            driver.close()

# TODO:
""" 
    登录后，验证一下是否真的登录了！！
    单个账号的进度
    8 个超话的自动签到
"""
