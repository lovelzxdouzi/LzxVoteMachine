from libs.readAccounts import *
from libs.Auto_Sign import *
from libs.goCenter import *
from libs.putSeed import *
from libs.Status import *

import sys
import libs.log
import os.path

"""
 超话打榜规则：
 8 个 超话签到
 8 次 帖子评论
 20 个 被评论
"""

# main app
if __name__ == '__main__':

    """
    # 设置日志
    """
    logger = libs.log.setup_custom_logger('test')
    
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

    my_path = os.path.abspath(os.path.dirname(__file__))
    driver_path = os.path.join(my_path, 'tools/chromedriver.exe')

    logger.debug('工作目录：%s', driver_path)
    print('工作目录：', driver_path)

    """
    # 如果读取账号出现问题，写入日志，关闭程序
    """
    try:
        accounts = readAccounts().get()
    except Exception as e:
        logger.debug('Exception - 读取账号时出现问题，程序终止。')
        logger.debug('Exception - %s', e)
        sys.exit()

    logger.debug('账号读取完毕')

    for name, pswd in accounts.items():
        driver = webdriver.Chrome(driver_path)
        try:
            logger.debug('账号：%s 正在打榜!', name)
            print('-----账号：{} 正在打榜：-----'.format(name))
            # TODO: 设置进度记录仪
            driver = Login(driver, name, pswd).run()
            logger.debug('操作进度：登录完成')
            print('INFO: 操作进度：登录完成')
            driver = goCenter(driver).run()
            logger.debug('操作进度：领分完成')
            print('INFO: 操作进度：领分完成')
            driver = AutoSign(driver).run()
            logger.debug('操作进度：自动签到完成')
            print('INFO: 操作进度：自动签到完成')
            driver = doComments(driver).run()
            logger.debug('操作进度：自动评论完成')
            print('INFO: 操作进度：自动评论完成')

            driver = putSeed(driver).run()
            logger.debug('操作进度：播种完成')
            print('INFO: 操作进度：播种完成')
            driver = goCenter(driver).sendScore()

            try:
                driver.quit()
            except AttributeError as a:
                logger.debug('AttributeError - %s', a)
                continue
        except TimeoutException as t:
            logger.debug('TimeoutException - 出现超时现象。挖土豆机已经终止')
            logger.debug('TimeoutException - %s', t)
            print(u'出现超时现象。挖土豆机已经终止')
            driver.quit()
            pass
        except WebDriverException as e:
            logger.debug('WebDriverException - 挖土豆机浏览器引擎出现问题，当前账号打榜已终止。')
            logger.debug('WebDriverException - %s', e)
            print(e)
            print(u'挖土豆机浏览器引擎出现问题，当前账号打榜已终止。')
            driver.quit()

# TODO:
""" 
    单个账号的进度
    -upgrade version: 只给评论小分队用的 自动评论器专业版
    -upgrade version: 只给阅读小分队用的 自动点赞转发专业版
"""
