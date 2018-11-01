from libs.readAccounts import *
from libs.CheckLock import *
from libs.Auto_Sign import *
from libs.goCenter import *
from libs.putSeed import *
from libs.Status import *

import libs.log
import sys
import os.path
import datetime

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

    # 得到当前时间
    start = time.time()
    start_s = datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    logger.debug('当前时间是：%s', start_s)
    
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

    index = 0
    total = len(accounts)
    logger.debug('账号读取完毕， 一共%d个账号', total)

    for name, pswd in accounts.items():
        index += 1
        driver = webdriver.Chrome(driver_path)
        driver.implicitly_wait(0.1)

        # 重置切号标志
        config.reset()
        
        try:
            logger.debug('-----账号(%d/%d)：%s 正在打榜:-----', index, total, name)
            print('-----账号(%d/%d)：%s 正在打榜:-----' %(index,total,name))
            # TODO: 设置进度记录仪
            driver = Login(driver, name, pswd).run()

            # 如果是死号，就切号
            if config.getNextAccount():
                config.addError()
                try:
                    driver.quit()
                except AttributeError as a:
                    logger.debug('AttributeError - %s', a)
                continue
            
            logger.debug('操作进度：登录完成')
            print('INFO: 操作进度：登录完成')

            driver = CheckLock(driver).run()
            # 如果账号被锁定，跳出，切号
            if config.getIsLock():
                config.addLock()
                try:
                    driver.quit()
                except AttributeError as a:
                    logger.debug('AttributeError - %s', a)
                continue

            logger.debug('操作进度：账号没有被锁定')
            print('INFO: 操作进度：账号没有被锁定')
            
            driver = AutoSign(driver).run()
            
            
            logger.debug('操作进度：自动签到完成')
            print('INFO: 操作进度：自动签到完成')
            driver = goCenter(driver).run()
            logger.debug('操作进度：领分完成')
            print('INFO: 操作进度：领分完成')
            driver = doComments(driver).run()
            logger.debug('操作进度：自动评论完成')
            print('INFO: 操作进度：自动评论完成')
            driver = putSeed(driver).run()
            logger.debug('操作进度：播种完成')
            print('INFO: 操作进度：播种完成')
            driver = goCenter(driver).sendScore()
            config.addSuccess()
            
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
            pass

        print('##############################')
        print('##############################')
        print('#### 账号总数：%d' %(total))
        print('#### 当前账号：%d' %(index))
        print('#### success：%d' %(config.getSuccess()))
        print('#### error：%d' %(config.getError()))
        print('#### lock：%d' %(config.getLock()))
        print('#### 一共送分：%d' %(config.getScore()))
        print('##############################')
        print('##############################')

        logger.debug('##############################')
        logger.debug('##############################')
        logger.debug('#### 账号总数：%d', total)
        logger.debug('#### 当前账号：%d', index)
        logger.debug('#### success：%d', config.getSuccess())
        logger.debug('#### error：%d', config.getError())
        logger.debug('#### lock：%d', config.getLock())
        logger.debug('#### 一共送分：%d', config.getScore())
        logger.debug('##############################')
        logger.debug('##############################')
    
    # 得到当前时间
    end = time.time()
    end_s = datetime.datetime.fromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')
    logger.debug('当前时间是：%s', end_s)

    # 得到打榜用时
    time_used = str(datetime.timedelta(end - start))

    print('##############################')
    print('##############################')
    print('#### 打榜完成')
    print('#### 开始时间：%s' %(start_s))
    print('#### 完成时间：%s' %(end_s))
    print('#### 总用时：%s' %(time_used))
    print('#### 账号总数：%d' %(total))
    print('#### success：%d' %(config.getSuccess()))
    print('#### error：%d' %(config.getError()))
    print('#### lock：%d' %(config.getLock()))
    print('#### 一共送分：%d' %(config.getScore()))
    print('##############################')
    print('##############################')

    logger.debug('##############################')
    logger.debug('##############################')
    logger.debug('#### 打榜完成')
    logger.debug('#### 开始时间：%s', start_s)
    logger.debug('#### 完成时间：%s', end_s)
    logger.debug('#### 总用时：%s', time_used)
    logger.debug('#### 账号总数：%d', total)
    logger.debug('#### success：%d', config.getSuccess())
    logger.debug('#### error：%d', config.getError())
    logger.debug('#### lock：%d', config.getLock())
    logger.debug('#### 一共送分：%d', config.getScore())
    logger.debug('##############################')
    logger.debug('##############################')

# TODO:
""" 
    单个账号的进度
    -upgrade version: 只给评论小分队用的 自动评论器专业版
    -upgrade version: 只给阅读小分队用的 自动点赞转发专业版
"""
