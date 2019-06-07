'''
zhihuishu.py
智慧树刷课脚本 稳定版
2019-06-07 by Deer
'''

from selenium import webdriver as web
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains


def log(msg):
    print(str(datetime.datetime.now()), '\t', msg)


# def video_is_end(chrome):
def progress_now(chrome):
    bar = chrome.find_elements_by_class_name('progressbar')[0]
    return bar.get_attribute('style').split(':')[-1].split(';')[0].strip()


def init_chrome(username, password):
    options = web.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
             # 'images': 2,
        }
    }
    options.add_experimental_option('prefs', prefs)
    chrome = web.Chrome(chrome_options=options)
    chrome.get('http://online.zhihuishu.com/onlineSchool/student/index')

    # 1.登录
    chrome.find_element_by_id('lUsername').send_keys(username)
    chrome.find_element_by_id('lPassword').send_keys(password)
    chrome.find_elements_by_class_name('wall-sub-btn')[0].click()

    # 2.选择第一课
    while (chrome.find_elements_by_class_name('speedPromote_btn').__len__() == 0):
        log('正在检测幕课“继续”按钮')
        time.sleep(1)
    chrome.find_elements_by_class_name('speedPromote_btn')[0].click()

    # 3.切换到当前最新打开的窗口
    windows = chrome.window_handles
    while len(windows) != 2:
        log('检测第二个窗口打开否')
        time.sleep(1)
        windows = chrome.window_handles
    windows = chrome.window_handles
    chrome.switch_to.window(windows[-1])
    print('切换新窗口')
    input('请手动关闭弹窗后 输入任何内容继续：')
    return chrome


def jump_next_video(chrome):
    chrome.find_elements_by_class_name('hour')
    for btn in chrome.find_elements_by_class_name('time_ico1'):
        if 'exam' not in btn.get_attribute('id'):
            btn.click()
            return 



if __name__ == '__main__':
    username = input('username:')
    password = input('password:')
    chrome = init_chrome(username, password)
    old_progress = ''
    while True:
        time.sleep(5)
        # 如果视频看完啦 跳下一个
        if progress_now(chrome) == '100%':
            jump_next_video(chrome)
            log('下一个视频')
        # 否则 把进度条拖到0 避免弹出问题
        else:
            log(f'当前进度：{progress_now(chrome)}')
            if old_progress == progress_now(chrome):
                log('视频卡住啦 刷新')
                chrome.refresh()
                continue
            old_progress = progress_now(chrome)
            a = chrome.find_elements_by_class_name('videoArea')[0]
            ActionChains(chrome).move_to_element(a).perform()
            time.sleep(1)
            bar = chrome.find_elements_by_class_name("progressBall")[0]
            ActionChains(chrome).click_and_hold(bar).move_by_offset(-50,0).release().perform()
            
