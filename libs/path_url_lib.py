# 这里都是需要用到的 url
mainst_url = 'https://weibo.com/p/100808132000b677812b65d29154c4ec164a96/super_index'
wtd_url = 'https://weibo.com/p/1008081b39f9799c74646813336ad8fa236872/super_index'
zdz_url = 'https://weibo.com/p/100808dabb2c01ce6873ff318f9e6e43211173/super_index'
cdb_url = 'https://weibo.com/p/1008082ba4d2bd5eba02778d7eb105551e72b9/super_index'
xkl_url = 'https://weibo.com/p/1008085db32612886f0e6498427553470911d9/super_index'

vote_url = 'https://huati.weibo.cn/super/pickoppo?page_id=100808132000b677812b65d29154c4ec164a96'

# 登录检查所需 xpath
gn_position_path = '//*[@id="pl_common_top"]/div/div/div[3]'
title_path = '//*[@id="Pl_Core_StuffHeader__1"]/div/div[2]/div/div[2]/h1'
move_ret_path = '//*[@id="patternCaptchaHolder"]/div[1]/div[2]'

# 自动签到 所需 xpath
focus_btn_path = '//*[@id="Pl_Core_StuffHeader__1"]/div/div[2]/div/div[3]/div/div[2]'
sign_btn_poth = '//*[@id="Pl_Core_StuffHeader__1"]/div/div[2]/div/div[3]/div/div[3]/a'

# 自动评论  所需 xpath
head_path = '//*[@id="Pl_Core_MixedFeed__291"]/div/div[2]/div/ul/li[2]/div/span[1]'
comment_btn_path = '//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[2]/div/ul/li[3]/a/span/span'
count_path = '//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[2]/div/ul/li[3]/a/span/span/span/em[2]'
textarea_path = '//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[3]/div/div/div[2]/div[2]/div[1]/textarea'
send_btn_path = '//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/a'

# 送分中心 按钮&信息 xpath
center_path = '//*[@id="app"]/div/div[2]/div[1]/a'
score_info_path = '//*[@id="app"]/div/div[2]/div[1]/span'
select_all_btn_path = '//*[@id="app"]/div/div[1]/div/ul[1]/li[4]'
vote_btn_path = '//*[@id="app"]/div/div[2]/div[2]/span[2]'
rank_info_path = '//*[@id="app"]/div/div[1]/div/div[1]/span'
desc_info_path = '//*[@id="app"]/div/div[1]/div/div[2]'
first_title_path = '//*[@id="app"]/div/section/dl[1]/dt'

# 任务中心 领取分数 xpath
new_user_bonus_path = '//*[@id="app"]/div/section/dl[1]/dd[1]/a[1]'
lxfw_bonus_path = '//*[@id="app"]/div/section/dl[2]/dd[1]/a'
comment_bonus_path = '//*[@id="app"]/div/section/dl[2]/dd[4]/a[2]'
twenty_bonus_path = '//*[@id="app"]/div/section/dl[3]/dd/a[1]'
saved_twenty_bonus_path = '//*[@id="app"]/div/section/dl[3]/dd/a[2]'

# 播种子所需 xpath:
seed_textarea_path = '//*[@id="Pl_Core_PublishV6__287"]/div/div/div/div/div[2]/div[2]/div[1]/textarea'
seed_send_btn_path = '//*[@id="Pl_Core_PublishV6__287"]/div/div/div/div/div[2]/div[2]/div[2]/div[1]/a'
