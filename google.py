import time
from selenium import webdriver
import os
from selenium.webdriver.support.ui import WebDriverWait
import pathlib

target_path = "./storedImg"
os.chmod(target_path, 0o777)
filelist = [f for f in os.listdir(target_path)]
for f in filelist:
    os.remove(os.path.join(target_path, f))
os.rmdir(target_path)
print("\nDIRECTORY REMOVED")
os.mkdir(target_path)
print("\nDIRECTORY CREATED")
imgs = []


def start():
    desc = input("\nImage Description: ")
    url = "https://www.google.com/search?q={0}&rlz=1C5CHFA_enUS843US843&sxsrf=ALeKk03NFv7cd9jFtpZNyb5MSxhhuOtK" \
          "fQ:1617053293273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwigiYP5uNbvAhUynOAKHXGiBAUQ_AUoAXoECAEQAw&biw=14" \
          "40&bih=690".format(desc)
    num_images = int(input("How many images?: "))
    pages_loop(init_driver(), url, num_images)


def init_driver():
    driver_path = "./chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.wait = WebDriverWait(driver, 5)
    return driver


def scrape(driver, num_images):
    num_images += int(num_images / 25)
    for i in range(1, num_images + 1):
        if i % 25 == 0:
            continue
        driver.find_element_by_xpath(
            """/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[{0}]/a[1]/div[1]/img"""
                .format(i)).click()
        time.sleep(.5)
        content = driver.find_element_by_xpath(
            "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/"
            "div[1]/div/div[2]/a/img").get_attribute("src")
        imgs.append(content)
        print(content)


def download(image):
    os.system("cd " + target_path + "; " + "curl -O " + image)


def pages_loop(driver, url, num_images):
    driver.get(url)
    time.sleep(3)
    scrape(driver, num_images)
    driver.close()
    for i in range(len(imgs)):
        download(imgs[i])
        print("\n{0}/{1}".format(i + 1, len(imgs)))
    files = []
    filename = pathlib.Path(target_path)
    for file in filename.iterdir():
        files.append(file)
    time.sleep(5)
    os.system("killall Preview")
    clean()


def clean():
    x = 0
    filename = pathlib.Path(target_path)
    for file in filename.iterdir():
        file_type = str(file)
        if not (file_type.endswith("jpg")) and not (file_type.endswith("png")):
            x += 1
            os.remove(file)

    if not x == 0:
        print("\nFile type unsupported for {0} images".format(x))

    print("\n\nPICTURES DOWNLOADED: {0}".format(len(imgs) - x))


start()
