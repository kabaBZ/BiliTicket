from BiliOrder.BiliOrder import BiliApi
import json
import time

if __name__ == "__main__":
    with open("./cookie.txt", "r") as f:
        cookie = f.read()

    with open("./token.txt", "r") as f:
        token = f.read()

    # cookie = "buvid3=A100C588-4759-DFCC-4F60-25773B1CC15A60686infoc; b_nut=1704731460; _uuid=884F16910-6217-6EAB-9B3F-5A6106356E2EF61693infoc; buvid4=FCD24F59-A348-819E-9542-6E32C0A9044A61438-024010816-pur4gGV8XVkIqfTofhg%2FbA%3D%3D; rpdid=|(Y|lJ|J~|Y0J'u~|R~JuRYu; DedeUserID=21197509; DedeUserID__ckMd5=23a6d60ac2163f40; enable_web_push=DISABLE; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1872-924; hit-dyn-v2=1; LIVE_BUVID=AUTO6917048827768866; buvid_fp_plain=undefined; CURRENT_QUALITY=80; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDk0NzM5MDMsImlhdCI6MTcwOTIxNDY0MywicGx0IjotMX0.LugJcrDHy8QgUkFXcUE3NvEh1RI43CvVCEyl4KVpFbM; bili_ticket_expires=1709473843; SESSDATA=88d31a9f%2C1724766719%2Ca880a%2A21CjAE-0Zfyp6uBOv4iOTmgYxv7VNlzF6xyImiIijEKriRAbUdRvVLEE4dNdu5-rqtINMSVnY2R1lkRXQya2ctSXYzdlU2VTctSHpUYkpyTTlHekdhaEJLTlJzdTBscGl4V1N1UmkzMjdrNndHSk13S3I2NjExY05hVUhVOGxHa2p3QVJmdC0xbm13IIEC; bili_jct=1c0390188b3536495b71347b02febac2; FEED_LIVE_VERSION=V8; CURRENT_FNVAL=4048; fingerprint=c7a99f8b210b590ec70d7279d7837c64; msource=pc_web; deviceFingerprint=eff5469d5848f860945a2f747cecdf74; Hm_lvt_909b6959dc6f6524ac44f7d42fc290db=1709363468,1709372377,1709445838; bsource=search_bing; buvid_fp=c7a99f8b210b590ec70d7279d7837c64; bp_video_offset_21197509=904558539642503173; PVID=3; canvasFp=90d7ce55109c8b3d11a121ae5e3803f1; webglFp=26410a13ea5fa2fa362af0972a19be49; screenInfo=1920*1080*24; feSign=cff5469d5848f860945a2f747cecdf74; payParams=%7B%22createIp%22%3A%22183.156.124.2%22%2C%22customerId%22%3A10001%2C%22defaultChoose%22%3A%22wechat%22%2C%22deviceType%22%3A1%2C%22extData%22%3A%22%7B%5C%22profitSharing%5C%22%3A%5C%22jzbPs%5C%22%2C%5C%22psExt%5C%22%3A%5C%22%7B%5C%5C%5C%22optType%5C%5C%5C%22%3A%5C%5C%5C%22jzbps_self%5C%5C%5C%22%7D%5C%22%7D%22%2C%22feeType%22%3A%22CNY%22%2C%22notifyUrl%22%3A%22http%3A//show.bilibili.co/api/ticket/order/payNotify%22%2C%22orderCreateTime%22%3A%221709451224000%22%2C%22orderExpire%22%3A600%2C%22orderId%22%3A%224007111915862999%22%2C%22originalAmount%22%3A23800%2C%22payAmount%22%3A23800%2C%22productId%22%3A461268%2C%22productUrl%22%3A%22https%3A//show.bilibili.com/platform/detail.html%3Fid%3D81605%22%2C%22returnUrl%22%3A%22https%3A//show.bilibili.com/platform/payResult.html%3ForderId%3D4007111915862999%22%2C%22serviceType%22%3A0%2C%22showContent%22%3A%22%u7968%u52A1_%u5317%u4EAC%B7Aw%u52A8%u6F2B%u6E38%u620F%u5609%u5E74%u534E7th%u51CC%u98DE%u4E13%u573A%u89C1%u9762%u4F1A_2024-03-03%2015%3A33%3A44_238%22%2C%22showTitle%22%3A%22bilibili%u7968%u52A1%22%2C%22signType%22%3A%22MD5%22%2C%22timestamp%22%3A%221709451224951%22%2C%22traceId%22%3A3276627767%2C%22version%22%3A%221.0%22%2C%22sign%22%3A%22f7cbfb74a6a4a947112984b07b5a2e86%22%7D; b_lsid=3BE1710B9_18E034D510C; from=pc_ticketlist; Hm_lpvt_909b6959dc6f6524ac44f7d42fc290db=1709453062"
    Order = BiliApi(cookie, token)
    project_id = input("输入演出id(按回车结束):")  # 81605
    # 获取演出场次及票务信息
    screenlist = Order.getV2(project_id)
    print(f"本演出共{len(screenlist)}场次")
    for screen in screenlist:
        print(f"场次编号：{screenlist.index(screen) + 1}  场次名称：{screen['screen_name']}")
    if len(screenlist) == 1:
        print("已选择第一场次")
        selected_screen = screenlist[0]
    else:
        selected_screen = screenlist[input("请选择场次编号：") - 1]

    screenid = selected_screen["screen_id"]

    print(f"本场次共{len(screenlist)}票种")
    sku_list = selected_screen["sku_list"]
    for sku in sku_list:
        print(f"票种编号：{sku_list.index(sku) + 1}  票种名称：{sku['skuid']}")
    if len(sku_list) == 1:
        print("已选择第一票种")
        selected_sku = sku_list[0]
    else:
        selected_sku = sku_list[input("请选择票种编号：") - 1]

    sku_id = selected_sku["skuid"]
    price = selected_sku["price"]

    input("修改buyer_info.json,保存后按回车")
    with open("./buyer_info.json", "r", encoding="utf-8") as f:
        buyer_info = json.loads(f.read().replace(" ", ""))
    buyer_id = Order.create_buyer(buyer_info)
    # # proid 81605  screenid 162526 skuid 461268
    Order.confirm_order("82605")
    for buyer in Order.buyer_list:
        if str(buyer["id"]) == buyer_id:
            Order.buyer = buyer
    # while time.time() < 1709457600:
    while time.time() < 1709459998:
        print("等待抢购")
        time.sleep(0.5)
    while True:
        try:
            result = Order.createV2(
                {
                    "projectid": project_id,
                    "screenid": str(screenid),
                    "skuid": str(sku_id),
                    "price": str(price),
                },
                Order.buyer,
            )
        except Exception as e:
            print(f"报错：{e}")
            time.sleep(0.05)
            continue
        else:
            if result:
                print(result)
                print("锁单成功！！！")
                break
            else:
                print(result)
                if time.time() > 1709460050:
                    break
                time.sleep(0.05)
                continue
