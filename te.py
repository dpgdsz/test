from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
from ddddocr import DdddOcr
import time


# 0402 new
def watch_courses(username, password, course_numbers):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    ocr = DdddOcr()

    def login():
        driver.get('https://student.cx-online.net/#/login')
        wait = WebDriverWait(driver, 20)
        name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="请输入手机号"]')))
        name_input.send_keys(username)
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入密码"]')
        password_input.send_keys(password)
        time.sleep(6)  # 等验证码出现
        code_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入验证码"]')
        img_code = driver.find_element(By.CSS_SELECTOR, '.code-img img')
        img_text = ocr.classification(img_code.screenshot_as_png)
        code_input.send_keys(img_text)
        login_button = driver.find_element(By.CSS_SELECTOR, 'button.el-button')
        login_button.click()

    def watch_course(course_number, course_rounds=66):
        wait = WebDriverWait(driver, 10)
        my_class_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/section/main/section/aside/div/ul/div[5]/li/span')))
        my_class_button.click()  # 我的课程
        time.sleep(2)
        course_button_xpath = f'/html/body/div[1]/section/main/section/main/div/div/div[2]/div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[{course_number}]/td[6]/div/div/button'
        course_button = wait.until(EC.element_to_be_clickable((By.XPATH, course_button_xpath)))
        course_button.click()
        kechenmulu_button_xpath = f'/html/body/div[1]/section/main/section/main/div/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]'
        kechenmulu_button = wait.until(EC.element_to_be_clickable((By.XPATH, kechenmulu_button_xpath)))
        kechenmulu_button.click()
        handles = driver.window_handles
        current_handle = driver.current_window_handle
        # for i in range(course_rounds):
        for i in range(3, 60):
            # 这里是循环体，写你想要循环执行的代码
            # for i in range(20,60):从20-59
            for handle in handles:
                if handle != current_handle:
                    driver.switch_to.window(handle)
                try:
                    kechenmulu_button_xpath = f'/html/body/div[1]/section/main/section/main/div/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]'
                    kechenmulu_button = wait.until(EC.element_to_be_clickable((By.XPATH, kechenmulu_button_xpath)))
                    kechenmulu_button.click()
                    my_ketanglianxi_button = wait.until(EC.presence_of_element_located(
                        (By.XPATH,
                         f"/html/body/div[1]/section/main/section/main/div/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div[{i}]/div/div[2]/div/div/div/div[2]/div/span[1]")))
                    # 课堂练习
                    print(f"点了课堂练习")
                    my_ketanglianxi_button.click()
                    # 增加做题的代码
                    # 等待包含正确答案的div元素变得可见
                    answer_div = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "multiple_ctx--rightAns"))
                    )

                    # 获取答案文本
                    answer_text = answer_div.find_element(By.TAG_NAME, 'span').text

                    # 检查答案文本中是否包含多选分隔符（例如顿号）
                    is_multiple_choice = '、' in answer_text

                    # 如果是多选，则分割答案并依次点击选项
                    if is_multiple_choice:
                        answer_options = [option.strip() for option in answer_text.split('、')]
                        for option in answer_options:
                            option_button_selector = f'.option[data-value="{option}"]'
                            option_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, option_button_selector))
                            )
                            option_button.click()
                            # 如果是单选，则直接点击对应的选项
                    else:
                        option_button_selector = f'.option[data-value="{answer_text}"]'
                        option_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, option_button_selector))
                        )
                        option_button.click()

                    # 做完本题点下一题
                    # 点确认答案
                    my_querendaan_botton = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                      "/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div/div[7]/button")))
                    my_querendaan_botton.click()
                    print(f"点确认答案")
                    # 点下一题
                    my_xiayiti_bottom = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div/div[3]/button[2]")))
                    my_xiayiti_bottom.click()
                    print(f"点下一题")

                    my_tijaozuoye_button = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                      '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/button')))
                    my_tijaozuoye_button.click()
                    print(f"点了提交作业")
                    my_tishiweizuo_button = wait.until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[3]/button[2]')))
                    my_tishiweizuo_button.click()
                    print(f"点了提示不能修改作业")
                    my_jiaojuanfanhui_button = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, '/html/body/div[1]/div[3]/div/div/footer/span/button[3]')))
                    my_jiaojuanfanhui_button.click()
                    print(f"做完了点返回，循环下一题")
                    time.sleep(1)
                    handles = driver.window_handles
                    current_handle = driver.current_window_handle
                    # time.sleep(5)
                    # import pyautogui
                    # pyautogui.press('escape')
                    # actions.send_keys(Keys.ESCAPE)
                    # wait_loading_mask = WebDriverWait(self.driver, 1)
                    # loading_mask = wait_loading_mask.until(
                    #     EC.invisibility_of_element_located((By.XPATH,
                    #                                         '/html/body/div[1]/section/main/section/main/div/div[3]/div/div/header/button/i')))

                    my_guanbi_button = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[1]/section/main/section/main/div/div[3]/div/div/header/button/i')))
                    my_guanbi_button.click()
                    handles = driver.window_handles
                    current_handle = driver.current_window_handle
                    time.sleep(2)

                except Exception as e:
                    print(f"答题时发生错误: {e}")
            print(f"第{i + 1}节第{course_number}科课程已完成")
        print(f"所有第{course_number}科课程已完成")

    try:
        login()
        for course_number in course_numbers:
            watch_course(course_number=course_number)
    finally:
        driver.quit()


if __name__ == '__main__':
    watch_courses("511322199208097566", "a123456", [1, 2, 3, 4, 5, 6, 7, 8])
