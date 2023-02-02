from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import ddddocr, base64, cv2, os
import pandas as pd

info = pd.read_excel("Res/info.xlsx", index_col="ID", dtype=str)
checkpoint = open("Res/ckpt.txt", "r+")


def ocr_captcha_ddddocr(image):
    ocr = ddddocr.DdddOcr(show_ad=False)
    img = cv2.imread(image)
    crop_img = img[380:450, 400:570]
    image_encode = str(base64.b64encode(cv2.imencode(".png", crop_img)[1]))[2:-1]
    result = ocr.classification(img=image_encode)
    os.remove(image)
    return result


def enter_IC(IC_no):
    myProxy = "103.75.196.121:80"
    proxy = Proxy(
        {
            "proxyType": ProxyType.MANUAL,
            "httpProxy": myProxy,
            "sslProxy": myProxy,
            "noProxy": "",
        }
    )

    options = Options()
    options.headless = True
    options.proxy = proxy

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    driver.get("https://api.ipify.org/")
    print(driver.find_element(By.TAG_NAME, "pre").text)

    driver.get("https://mysprsemak.spr.gov.my/semakan/daftarPemilih")
    driver.save_screenshot("ss.png")

    # input IC
    driver.find_element(By.NAME, "NoKp").send_keys(IC_no)

    # extract CAPTCHA and submit
    driver.find_element(By.NAME, "captcha").send_keys(ocr_captcha_ddddocr("ss.png"))
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Semak']").click()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    data = soup.find_all("td")

    if data:
        # data comes as a list [header1,data1,header2,data2... and so on]. Lazy so i just take every second piece of info
        info.loc[len(info.index)] = [
            data[1].text,
            data[3].text,
            data[5].text,
            data[7].text,
            data[9].text,
            data[11].text,
            data[13].text,
            data[15].text,
            data[17].text,
        ]

    info.to_excel("Res/info.xlsx")
    driver.close()
