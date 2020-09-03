from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

# 设置谷歌驱动器的环境
options = webdriver.ChromeOptions()
# 设置chrome不加载图片，提高速度
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# 创建一个谷歌驱动器
browser = webdriver.Chrome(options=options,
                           executable_path=r'C:\Users\HP\AppData\Local\Programs\Python\Python36\Scripts\chromedriver')
browser.minimize_window()  # 最小化窗口，方便输入要检索的页数和关键词
url = 'https://wap.cnki.net/touch/web/Article/SearchIndex'


def start_spider(page):
    # 请求url
    browser.get(url)
    # 显示等待输入框是否加载完成
    WebDriverWait(browser, 1000).until(EC.presence_of_all_elements_located((By.ID, 'keyword_ordinary')))
    # 找到输入框的id，并输入关键字，如这儿我们输入测绘，待会儿我们爬取的就是关于测绘文献方面的信息
    word = input("请输入要检索的关键词 ：")
    print("\n请稍等片刻！")
    browser.find_element_by_id('keyword_ordinary').send_keys(word)
    # 输入关键字之后点击搜索
    browser.find_element_by_class_name('btn-search ').click()
    # print(browser.page_source)
    # 显示等待文献是否加载完成
    WebDriverWait(browser, 1000).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'g-search-body')))
    # 声明一个标记，用来标记翻页几页
    count = 1
    while True:
        # 显示等待加载更多按钮加载完成
        WebDriverWait(browser, 1000).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'c-company__body-item-more')))
        # 获取加载更多按钮
        Btn = browser.find_element_by_class_name('c-company__body-item-more')
        # 显示等待该信息加载完成
        WebDriverWait(browser, 1000).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@id="searchlist_div"]/div[{}]/div[@class="c-company__body-item"]'.format(2 * count - 1))))
        # 获取在div标签的信息，其中format(2*count-1)是因为加载的时候有显示多少条
        # 简单的说就是这些div的信息都是奇数
        divs = browser.find_elements_by_xpath(
            '//div[@id="searchlist_div"]/div[{}]/div[@class="c-company__body-item"]'.format(2 * count - 1))
        # 遍历循环
        for div in divs:
            # 获取文献的题目
            name = div.find_element_by_class_name('c-company__body-title').text
            # 获取文献的作者
            author = div.find_element_by_class_name('c-company__body-author').text
            # 获取文献的来源和日期、文献类型等
            text = div.find_element_by_class_name('c-company__body-name').text.split()
            if (len(text) == 3 and text[-1] == '优先') or len(text) == 2:
                # 来源
                source = text[0]
                # 日期
                datetime = text[1]
                # 文献类型
                literature_type = None
            else:
                source = text[0]
                datetime = text[2]
                literature_type = text[1]

            data = (name, author, source, datetime, literature_type)
            with open(r'D:\data.csv', 'a', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)

        # 如果Btn按钮（就是加载更多这个按钮）没有找到（就是已经到底了），就退出
        if not Btn:
            break
        else:
            Btn.click()
        # 如果到了爬取的页数就退出
        if count == page:
            break
        count += 1
        # 延迟,让爬虫爬取慢点，给服务器减轻压力，以免服务器崩溃
        time.sleep(3)


if __name__ == '__main__':
    # 先写入表头信息
    with open(r'D:\data.csv', 'a', encoding='utf-8',
              newline='') as csvfile:  # 存储的路径可以自己设置,我存在了D:\Python_DATA\data.csv里
        writer = csv.writer(csvfile)
        writer.writerow(("文献名", "作者", "来源", "发表日期", "文献类型"))
    start_spider(page=eval(input('请输入要爬取的页数（如果需要全部爬取请输入0，可能需要等很长时间）：')))  # eval()是执行一个字符串表达式
    browser.close()
    print("爬取完成，请到相应文件夹查看！")
