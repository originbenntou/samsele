import os
import time
import json
import logging
from boto3.session import Session
from selenium import webdriver
from selenium.webdriver.support.select import Select

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

TARGET_URL = "https://www.fit-portal.go.jp/mypage/UserLogin"
FILENAME = os.path.join("/tmp", "screen.png")

# 日本語対応
os.environ['HOME'] = '/opt/'

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
    driver.maximize_window()
    driver.implicitly_wait(10)

    ##################################
    # アクセス
    ##################################
    driver.get(TARGET_URL)
    logger.info("Access OK")

    ##################################
    # ログイン
    ##################################
    driver.find_element_by_xpath("//input[@type='text']").send_keys("") # FIXME
    driver.find_element_by_xpath("//input[@type='password']").send_keys("") # FIXME
    driver.find_element_by_xpath("//input[@type='submit']").click()
    logger.info("Login OK")

    ##################################
    # マイページ
    ##################################
    time.sleep(5)
    # 申請開始
    driver.find_element_by_xpath("//*[@class='btn_cell']").find_element_by_tag_name("a").click()
    logger.info("FIT申請 Start")

    ##################################
    # 設備区分選択
    ##################################
    time.sleep(5)
    # 発電設備の区分
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:j_id80']")).select_by_value("太陽光")

    # 出力区分
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:j_id86']")).select_by_value("10kW以上50kW未満")

    # 設備利用者区分
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:j_id101']")).select_by_value("自ら太陽光発電設備を設置される方")

    # 離島等供給エリアか
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:j_id105']")).select_by_value("該当無し")

    # 情報入力ボタン
    driver.find_element_by_xpath("//*[@class='rollover']").click()
    logger.info("区分 OK")

    ##################################
    # 情報入力
    ##################################
    time.sleep(5)
    # 事業者自身が入力されていますか？
    Select(driver.find_element_by_xpath("//*[@id='j_id0:form:instPrincipal']")).select_by_value("本人")

    # 地方税法第七十二条の四に規定する法人
    driver.find_element_by_xpath("//input[@id='j_id0:form:chkCorp']").click()

    # 発電設備の出力（kW）
    driver.find_element_by_xpath("//input[@id='j_id0:form:StandardOutput']").send_keys("29.9")

    # パワーコンディショナーの自立運転機能の有無
    driver.find_element_by_xpath("//input[@name='pCSIndOp']").click()
    time.sleep(5)

    # パワーコンディショナーの出力（kW）
    driver.find_element_by_xpath("//input[@id='j_id0:form:pCSOutput']").send_keys("30.0")

    # パワーコンディショナーの自立運転機能の出力（kW）
    driver.find_element_by_xpath("//input[@id='j_id0:form:pCSIndOpOutput']").send_keys("20.0")

    # 給電用コンセントの有無
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id682']").click()

    # 発電設備の名称
    driver.find_element_by_xpath("//input[@id='j_id0:form:NmPowerplant']").send_keys("サンプルソーラー発電")
    logger.info("事業者情報 OK")

    # 代表地番_0
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id723:0:mainCityCheck']").click()
    # 郵便番号_0
    driver.find_element_by_xpath("//input[@id='j_id0:form:j_id723:0:pos1']").send_keys("") # FIXME
    driver.find_element_by_xpath("//input[@id='j_id0:form:j_id723:0:pos2']").send_keys("") # FIXME
    # 住所反映_0
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id723:0:j_id731']").click()
    time.sleep(5)
    # 住所選択_0
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id2281:j_id2282:j_id2300:0:j_id2302']").click()
    time.sleep(5)
    # 町名・番地_0
    driver.find_element_by_xpath("//input[@id='j_id0:form:j_id723:0:AddrDetailIn']").send_keys("サンプルハウス２－１０００") # FIXME

    # 住所追加
    driver.find_element_by_xpath("//input[@id='j_id0:form:j_id723:0:j_id777']").click()
    time.sleep(5)

    # 郵便番号_1
    driver.find_element_by_xpath("//input[@id='j_id0:form:j_id723:1:pos1']").send_keys("") # FIXME
    driver.find_element_by_xpath("//input[@id='j_id0:form:j_id723:1:pos2']").send_keys("") # FIXME
    # 住所反映_1
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id723:1:j_id731']").click()
    time.sleep(5)
    # 住所選択_1
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id2281:j_id2282:j_id2300:0:j_id2302']").click()
    time.sleep(5)
    # 町名・番地_1
    driver.find_element_by_xpath("//input[@id='j_id0:form:j_id723:1:AddrDetailIn']").send_keys("サンプルハウス１－１－１") # FIXME

    # 事業区域の面積(㎡)
    driver.find_element_by_xpath("//input[@id='j_id0:form:OutlineArea']").send_keys("1000")

    # 太陽光発電設備の設置形態 屋根設置
    driver.find_element_by_xpath("//label[@for='j_id0:form:papRoofLoc']").click()
    time.sleep(5)

    # 太陽光発電設備の設置形態 建設中・予定の建物等
    driver.find_element_by_xpath("//label[@for='j_id0:form:roofBldRadio:1']").click()
    time.sleep(5)

    # 太陽光発電設備の設置形態 事業者が所有
    driver.find_element_by_xpath("//label[@for='j_id0:form:roofSecStatusRadio:0']").click()

    # 太陽光発電設備の設置形態 建物の種類
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:roofBldSelect']")).select_by_value("一戸建ての住宅")
    time.sleep(5)

    # 太陽光発電設備の設置形態 地上設置
    driver.find_element_by_xpath("//label[@for='j_id0:form:papLandLoc']").click()
    time.sleep(5)

    # 太陽光発電設備の設置形態 野立て
    driver.find_element_by_xpath("//label[@for='j_id0:form:landTypeRadio:0']").click()
    time.sleep(5)

    # 太陽光発電設備の設置形態 事業者が所有
    driver.find_element_by_xpath("//label[@for='j_id0:form:landSecStatusRadio:0']").click()
    time.sleep(5)

    # 農地一時転用許可申請予定の有無 無し
    driver.find_element_by_xpath("//input[@name='farmlandTempDiversion' and @value='無']").click()
    time.sleep(5)

    logger.info("発電設備の設置場所に係る事項 OK")

    # 太陽電池 型式リスト_0
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id936:0:srch']").click()
    time.sleep(5)

    # 型式リスト_0
    iframe = driver.find_element_by_xpath("//iframe")
    driver.switch_to.frame(iframe)
    ## 入力_0
    driver.find_element_by_xpath("//input[@name='j_id0:j_id5:j_id8']").send_keys("ＣＳ３ＬＡ")
    ## 検索_0
    driver.find_element_by_xpath("//input[@name='j_id0:j_id5:j_id16']").click()
    time.sleep(5)
    ## 選択_0
    for tr in driver.find_elements_by_xpath("//table[@id='search_result_table']/tbody/tr"):
        if tr.find_element_by_xpath("td[1]").text == "ＣＳ３ＬＡ－３００ＭＳ":
            driver.execute_script(tr.find_element_by_xpath("td[6]/input[@value='選択']").get_attribute("onclick"))
            break
    time.sleep(5)
    driver.switch_to.default_content()

    ## 枚数_0
    driver.find_element_by_xpath("//input[@id='j_id0:form:j_id936:0:NmPanel']").send_keys("100")

    # 構造図
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:CdStructualdrawing']")).select_by_value("標準構造図と同じ")
    time.sleep(5)

    # 配線図
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:CdWiringdiagram']")).select_by_value("標準配線図と同じ")
    time.sleep(5)

    # 配線方法
    driver.find_element_by_xpath("//label[@for='j_id0:form:wiringRadio:1']").click()

    # 自家発電設備等の設置の有無 無し
    driver.find_element_by_xpath("//input[@name='pvtGenInstall']").click()
    time.sleep(5)

    # 自家発電設備の種類
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:privateGeneratorTypeSelect']")).select_by_value("蓄電池")
    time.sleep(5)

    # 自家発電設備の種類
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:j_id1111']")).select_by_value("PCSより発電設備側")
    time.sleep(5)

    # 区分計量の可否 可
    driver.find_element_by_xpath("//input[@id='j_id0:form:j_id1122:0']").click()
    time.sleep(5)

    # 電気事業者への電気供給量の計測方法
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:CdElecSupply']")).select_by_value("単独計測")
    time.sleep(5)

    # 接続契約締結日
    driver.find_element_by_xpath("//input[@id='j_id0:form:DtConcludeContract']").send_keys("2022/07/01")

    # 接続契約締結先
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:j_id1184']")).select_by_value("東京電力パワーグリッド")
    time.sleep(5)

    # 工事費負担金（円）（税抜き）
    driver.find_element_by_xpath("//input[@id='j_id0:form:ContributionConstruct']").send_keys("1000000")

    # 設置工事開始予定日
    driver.find_element_by_xpath("//input[@id='j_id0:form:DtConstructStart']").send_keys("2022/11/01")

    # 系統連系予定日
    driver.find_element_by_xpath("//input[@id='j_id0:form:DtInterconnection']").send_keys("2022/12/31")

    # 運転開始日（又は予定日）
    driver.find_element_by_xpath("//input[@id='j_id0:form:DtInstall']").send_keys("2022/12/31")

    # 設備廃止予定日
    driver.find_element_by_xpath("//input[@id='j_id0:form:DtRemovePlan']").send_keys("2050/07/05")

    # 法人個人区分
    Select(driver.find_element_by_xpath("//*[@name='j_id0:form:MainteHoujinKojin']")).select_by_value("個人")
    time.sleep(5)

    # 事業者情報反映
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id1289']").click()
    time.sleep(5)

    # 保守点検及び維持管理計画
    driver.find_element_by_xpath("//input[@id='j_id0:form:MaintePlan']").send_keys("半年に1度、工事店によるメンテナンスを契約")

    # 保守点検及び維持管理費用総額（円）（税抜き）
    driver.find_element_by_xpath("//input[@id='j_id0:form:MainteCost']").send_keys("100000")

    # 当該発電設備における年間発電量の見込み（kWh/年）
    driver.find_element_by_xpath("//input[@id='j_id0:form:yearlyPwrGen']").send_keys("100.0")

    # 自家消費等の量の見込み（kWh/年）
    self = driver.find_element_by_xpath("//input[@id='j_id0:form:yearlySelfConsumption']")
    self.send_keys("")
    time.sleep(5)
    self.send_keys("50.0")

    # 自家消費等の用途
    self_purpose = driver.find_element_by_xpath("//input[@name='j_id0:form:j_id1549']")
    self_purpose.send_keys("")
    time.sleep(5)
    self_purpose.send_keys("自家消費")

    # 前年の電力消費量（kWh/年）
    driver.find_element_by_xpath("//input[@id='j_id0:form:prevYearPwrConsumption']").send_keys("0")
    time.sleep(5)

    # 特定供給の有無
    driver.find_element_by_xpath("//input[@id='j_id0:form:specifiedSupply:1']").click()
    time.sleep(5)

    logger.info("太陽電池に係る事項 OK")

    # 解体等に要する費用
    driver.find_element_by_xpath("//input[@name='j_id0:form:externalReserveChk']").click()
    time.sleep(5)

    logger.info("廃棄費用積立事項 OK")

    # 遵守事項
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchk1']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchk9']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchkC']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchk8']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchk5']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchk2']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchk3']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchk4']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchk6']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchkB']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:bchk7']").click()

    logger.info("遵守事項 OK")

    # 確認事項
    driver.find_element_by_xpath("//input[@name='j_id0:form:chk2']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:chk5']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:chk6']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:chk3']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:chk1']").click()
    driver.find_element_by_xpath("//input[@name='j_id0:form:chk4']").click()

    logger.info("確認事項 OK")

    # 内容確認
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id2272']").click()
    time.sleep(5)

    # 保存して次に進む
    driver.find_element_by_xpath("//input[@name='j_id0:form:j_id676']").click()
    time.sleep(5)

    logger.info("内容確認 OK")

    ##################################
    # 関係法令
    ##################################
    # 国土利用計画法に基づく土地売買等届出
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance0' and @value='無']").click()
    time.sleep(5)
    # 都市計画法に基づく開発許可
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance1' and @value='無']").click()
    time.sleep(5)
    # 河川法に基づく工作物の新築等の許可、河川区域内の土地占用・掘削許可
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance2' and @value='無']").click()
    time.sleep(5)
    # 港湾法に基づく港湾区域内の水域又は港湾隣接地域における専用の許可、臨港地区内における行為の届出
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance3' and @value='無']").click()
    time.sleep(5)
    # 海岸法に基づく海岸保全区域等の占用許可
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance4' and @value='無']").click()
    time.sleep(5)
    # 急傾斜地の崩壊による災害の防止に関する法律に基づく急傾斜地崩壊危険区域内の行為許可
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance5' and @value='無']").click()
    time.sleep(5)
    # 砂防法に基づく砂防指定地における行為の許可、砂防設備の占用許可
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance6' and @value='無']").click()
    time.sleep(5)
    # 地すべり等防止法に基づく地すべり防止区域又はぼた山崩壊防止区域内の行為許可
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance7' and @value='無']").click()
    time.sleep(5)
    # 景観法に基づく届出
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance8' and @value='無']").click()
    time.sleep(5)
    # 農業振興地域整備に関する法律に基づく市町村の農業振興地域整備計画の変更手続
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance9' and @value='無']").click()
    time.sleep(5)
    # 農地法に基づく農地転用許可
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance10' and @value='無']").click()
    time.sleep(5)
    # 森林法に基づく林地開発許可等手続、伐採及び伐採後の造林の届出手続
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance11' and @value='無']").click()
    time.sleep(5)
    # 文化財保護法に基づく埋蔵文化財包蔵地土木工事等届出、史跡・名勝・天然記念物指定地の現状変更許可
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance12' and @value='無']").click()
    time.sleep(5)
    # 土壌汚染対策法に基づく土地の形質変更届出
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance13' and @value='無']").click()
    time.sleep(5)
    # 自然公園法に基づく工作物新築許可等
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance14' and @value='無']").click()
    time.sleep(5)
    # 自然環境保全法に基づく工作物新築許可等
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance15' and @value='無']").click()
    time.sleep(5)
    # 絶滅のおそれがある野生動植物の種の保存に関する法律に基づく生息地等保護区の管理地区の行為許可等
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance16' and @value='無']").click()
    time.sleep(5)
    # 鳥獣の保護及び管理並びに狩猟の適正化に関する法律に基づく鳥獣保護区の特別保護地区の行為許可
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance17' and @value='無']").click()
    time.sleep(5)
    # 環境影響評価法・条例に係る環境影響評価手続
    driver.find_element_by_xpath("//input[@name='btnRadioRelevance18' and @value='無']").click()
    time.sleep(5)

    # 保存して次に進む
    driver.find_element_by_xpath("//input[@name='page:form:j_id255']").click()
    time.sleep(5)

    logger.info("関係法令 OK")

    ##################################
    # 書類添付
    ##################################
    # 住民票の写し
    driver.find_element_by_xpath("//input[@id='page:form:myRepeater:0:fileInput']").send_keys("")
    time.sleep(5)

    ##################################
    # スクリーンショット
    ##################################
    driver.set_window_size(
        driver.execute_script("return document.body.scrollWidth;"),
        driver.execute_script("return document.body.scrollHeight;")
    )
    driver.save_screenshot(FILENAME)
    logger.info("ScreenShot OK")

    driver.close()
    driver.quit()

    ##################################
    # スクショアップロード
    ##################################
    upload_s3_result(BUCKET_NAME)
    logger.info("Upload Result OK")

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
