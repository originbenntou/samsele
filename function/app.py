import os
import time
import json
from selenium import webdriver
from boto3.session import Session
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

endpoint_url = "http://s3local:4566"
session = Session(
    region_name = "ap-northeast-1"
)
s3 = session.resource(
    service_name = "s3",
    endpoint_url = endpoint_url
)

BUCKET_NAME = "samsele-bucket-local"

CHROME_DRIVER_PATH = "/opt/bin/chromedriver"
HEADLESS_CHROMIUM_PATH = "/opt/bin/headless-chromium"

TARGET_URL = ""
FILENAME = os.path.join("/tmp", "screen.png")

def lambda_handler(_event, _context):

    options = webdriver.ChromeOptions()

    options.binary_location = HEADLESS_CHROMIUM_PATH
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")

    driver = webdriver.Chrome(
        executable_path = CHROME_DRIVER_PATH,
        chrome_options = options
    )

    driver.get(TARGET_URL)

    user = driver.find_element_by_xpath("//input[@type='email']")
    user.send_keys("")
    word = driver.find_element_by_xpath("//input[@type='password']")
    word.send_keys("")
    submit = driver.find_element_by_xpath("//input[@type='submit']")
    submit.click()

    # Get width and height of the page
    w = driver.execute_script("return document.body.scrollWidth;")
    h = driver.execute_script("return document.body.scrollHeight;")

    # Set window size
    driver.set_window_size(w, h)

    # Get Screen Shot
    driver.save_screenshot(FILENAME)
    logger.info("ScreenShot OK")

    driver.close()
    driver.quit()

    upload_s3_result(BUCKET_NAME)
    logger.info("Upload Result OK")

    time.sleep(180)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "OK",
        }),
    }

def upload_s3_result(bucket_name):
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(
        "/tmp/screen.png",
        "screen.png",
        ExtraArgs={"ContentType": "image/png"}
    )
