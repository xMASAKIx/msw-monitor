import requests
import time
import threading
from flask import Flask
import os

app = Flask('')

@app.route('/')
def home():
    return "MSW Bot with Custom Images is Alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 設定區域 ---
PLAYER_MAP = {
    "20372100000223997": {"name": "別時", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/17/1745254512144.png"},
    "20372100005338018": {"name": "小波", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/322/1775991434332.png"},
    "20372100003479787": {"name": "卡提作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/321/1774855337857.png"},
    "20372100003567962": {"name": "妃姬作者","image": "https://mod-file.dn.nexoncdn.co.kr/shop/213/1776626647882.png"},
    "20372100008583110": {"name": "ES(夜夜發貨號)", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/149/1753505473494.png"},
    "20372100005894481": {"name": "平行", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/749/1762773253552.png"},
    "20372100003096391": {"name": "幽幽子", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/586/1762449873627.png"},
    "20372100001110251": {"name": "mimiming天使", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/749/1747565380029.png"},
    "20372100002790823": {"name": "mimiming天使", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/757/1732900933505.png"},
    "20372100004235799": {"name": "死靈作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/907/1748105199984.png"},
    "20372100005999546": {"name": "TJ01", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/279/1776452793102.png"},
    "20372100005764633": {"name": "TJ02", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/163/1776452831843.png"},
    "20372100005118171": {"name": "兔仔", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/956/1776228554718.png"},
    "20372000486671177": {"name": "韓國愛芮", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/58/1775909266323.png"},
    "20372100005311821": {"name": "照作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/558/1775307529921.png"},
    "20372100003863084": {"name": "阿卡利作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/368/1757691781562.png"},
    "20372100000180209": {"name": "PLAT", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/417/1776402215444.png"},
    "20372100003462165": {"name": "奧米加獸作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/988/1775817850083.png"},
    "20372100000208070": {"name": "珊璞作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/166/1777216997978.png"},
    "20372100002340154": {"name": "金武金", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/746/1777216923670.png"},
    "20372100005770592": {"name": "PAKA", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/271/1775588447819.png"},
    "20372100005385883": {"name": "白狐", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/25/1753058871388.png"},
    "20372100005694709": {"name": "小別時", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/269/1748733872754.png"},
    "20372100008443475": {"name": "paka1", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/679/1774714211779.png"},
    "20372100005802883": {"name": "paka2", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/389/1777320374327.png"},
    "20372100008359961": {"name": "沖田作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/18/1777724572613.png"},
    "20372100002553986": {"name": "殺手兔作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/610/1777201020468.png"},
    "20372100006407090": {"name": "北極熊初音作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/7/1778050053104.png"},
    "20372100009098159": {"name": "哥倫比雅作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/123/1777628265094.png"},
    "20372100005046143": {"name": "TJ", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/861/1751824550127.png"},
    "20372100007473992": {"name": "蕾米&芙蘭", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/792/1753813913624.png"},
    "20372100004981518": {"name": "AWAWA", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/706/1749651958133.png"},
    "20372100003328034": {"name": "Coya奇術", "image": "https://mod-file.dn.nexoncdn.co.kr/profile/949/1778243422289.png"},
    "20372100000224166": {"name": "別時", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/246/1739416591406.png"},
    "20372001057320745": {"name": "MIKA", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/854/1766070535501.png"},
    "20372100005833987": {"name": "菲特", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/440/1757093677010.png"},
    "20372100005779084": {"name": "簡&卡媽", "image": "https://mod-file.dn.nexoncdn.co.kr/profile/951/1770739129110.png"},
    "20372100007840052": {"name": "惡魔狐", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/982/1757623973159.png"},
    "20372100007791322": {"name": "奶鱈", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/773/1758903318897.png"},
    "20372100006053110": {"name": "智傑黑絲人", "image": "https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1696781720-51rrQkTpkdL.jpg"}
}

DEFAULT_IMAGE = "https://example.com/default.png"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497592013166608484/-bQDkOKmZBbxRMXwkmgQqrFsk4cdrtKIuKfVlxk81XeXwqalZ-9VliOuSC5wI1YMcuRT"
DISCORD_WEBHOOK_URL_PAKA = "https://discord.com/api/webhooks/1502364012128637039/o9cJHlVQ4sibt4E-YVSki-TsNlaRSwjFH2kDaiqwl5qPnek5_UR4SWDVdZpfBYWRVbS7"

# 特別名單：包含 PAKA, paka1, paka2 的 PID
SPECIAL_PLAYERS = ["20372100008443475", "20372100005802883","20372100006053110"]

CHECK_INTERVAL = 10 
API_URL_TEMPLATE = "https://mverse-api.nexon.com/social/v1/profile/{}"

# 紀錄狀態
last_known_data = {pid: {"is_online": None, "world_name": None} for pid in PLAYER_MAP.keys()}

def check_players():
    global last_known_data
    print(f"[{time.strftime('%H:%M:%S')}] 掃描中...")

    for pid, info in PLAYER_MAP.items():
        try:
            name = info["name"]
            custom_image = info.get("image", DEFAULT_IMAGE)
            
            url = API_URL_TEMPLATE.format(pid)
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            response = requests.get(url, headers=headers, timeout=10)
            data_root = response.json().get('data', {})
            
            # 獲取 API 回傳的當前狀態
            is_online = (data_root.get('isOnline') == 1)
            world_name = data_root.get('worldName') 
            p_code = data_root.get('profileCode', '未知')
            
            prev = last_known_data[pid]

            if prev["is_online"] is None:
                last_known_data[pid] = {"is_online": is_online, "world_name": world_name}
                continue

            should_notify = False
            status_msg = ""
            
            # 偵測上下線
            if is_online != prev["is_online"]:
                should_notify = True
                status_msg = "🟢 上線了！" if is_online else "🔴 下線了。"
            # 偵測切換遊戲世界
            elif is_online and world_name != prev["world_name"]:
                should_notify = True
                status_msg = "🔄 切換世界"

            if should_notify:
                last_known_data[pid] = {"is_online": is_online, "world_name": world_name}
                
                current_world = world_name if world_name else "大廳或選單中"
                color = 3066993 if is_online else 15158332 
                
                description = f"玩家：**{name}**\n代碼：`{p_code}`\n狀態：**{status_msg}**"
                if is_online:
                    description += f"\n目前位置：`{current_world}`"

                payload = {
                    "embeds": [{
                        "title": "楓之谷發貨號動態",
                        "description": description,
                        "thumbnail": {"url": custom_image}, 
                        "color": color,
                        "footer": {"text": f"PPSN: {pid}"},
                        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                    }]
                }
                
                # --- 發送邏輯 ---
                # 1. 發送至通用頻道 (所有人)
                requests.post(DISCORD_WEBHOOK_URL, json=payload)

                # 2. 如果在特別名單，額外發送至 Paka 專屬頻道
                if pid in SPECIAL_PLAYERS:
                    # 如果是 Paka，只發送到專屬頻道 (dc2)
                    requests.post(DISCORD_WEBHOOK_URL_PAKA, json=payload)
                    print(f"🚀 [dc2] 專屬通知: {name} (dc1不發送)")
                else:
                    # 如果不是 Paka，發送到原本的通用頻道 (dc1)
                    requests.post(DISCORD_WEBHOOK_URL, json=payload)
                    print(f"📣 [dc1] 一般通知: {name}")

                # 更新迴圈內的紀錄 (這行一定要在發送後執行)
                print(f"✅ 處理完成: {name}")

        except Exception as e:
            print(f"檢查 {pid} 出錯: {e}")

def main_loop():
    while True:
        check_players()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    threading.Thread(target=main_loop, daemon=True).start()
    run_web()
