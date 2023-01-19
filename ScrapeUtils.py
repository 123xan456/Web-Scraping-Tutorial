from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import ddddocr, base64, cv2, os
import pandas as pd

info = pd.read_excel("info.xlsx", index_col="ID", dtype=str)
options = Options()
options.headless = True
checkpoint = open("ckpt.txt", "r+")


def ocr_captcha_ddddocr(image):
    ocr = ddddocr.DdddOcr(show_ad=False)
    img = cv2.imread(image)
    crop_img = img[380:450, 400:570]
    image_encode = str(base64.b64encode(cv2.imencode(".png", crop_img)[1]))[2:-1]
    result = ocr.classification(img=image_encode)
    os.remove(image)
    return result


def enter_IC(IC_no):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get("https://mysprsemak.spr.gov.my/semakan/daftarPemilih")
    driver.save_screenshot("ss.png")

    # input IC
    driver.find_element(By.NAME, "NoKp").send_keys(IC_no)

    # extract CAPTCHA
    driver.find_element(By.NAME, "captcha").send_keys(ocr_captcha_ddddocr("ss.png"))
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Semak']").click()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    data = soup.find_all("td")

    if data:
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

    info.to_excel("info.xlsx")
    driver.close()
