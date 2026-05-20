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
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# --- 設定區域 ---
PLAYER_MAP = {
    "20372100000223997": {"name": "別時", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/17/1745254512144.png"},
    "20372100005338018": {"name": "小波", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/322/1775991434332.png"},
    "20372100003479787": {"name": "卡提作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/321/1774855337857.png"},
    "20372100003567962": {"name": "妃姬作者","image": "https://mod-file.dn.nexoncdn.co.kr/shop/213/1776626647882.png"},
    "20372100005894481": {"name": "平行", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/749/1762773253552.png"},
    "20372100003096391": {"name": "幽幽子", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/586/1762449873627.png"},
    "20372100001110251": {"name": "mimiming天使", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/749/1747565380029.png"},
    "20372100002790823": {"name": "mimiming天使", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/757/1732900933505.png"},
    "20372100004235799": {"name": "死靈", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/907/1748105199984.png"},
    "20372100003186784": {"name": "死靈妹01", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/858/1731945991995.png"},
    "20372100002734060": {"name": "死靈妹02", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/412/1731771573322.png"},
    "20372100005999546": {"name": "TJ01", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/279/1776452793102.png"},
    "20372100005764633": {"name": "TJ02", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/163/1776452831843.png"},
    "20372100002340154": {"name": "金武金", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/746/1777216923670.png"},
    "20372100005770592": {"name": "PAKA", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/271/1775588447819.png"},
    "20372100006407090": {"name": "北極熊初音作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/233/1749625499529.png"},
    "20372100005694709": {"name": "小別時", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/269/1748733872754.png"},
    "20372100008443475": {"name": "paka1", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/679/1774714211779.png"},
    "20372100005802883": {"name": "paka2", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/389/1777320374327.png"},
    "20372100005046143": {"name": "TJ", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/861/1751824550127.png"},
    "20372100000224166": {"name": "別時", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/246/1739416591406.png"},
    "20372100002684295": {"name": "ES作者", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/139/1778405604185.png"},
    "20372100000590354": {"name": "照&露西", "image": "https://mod-file.dn.nexoncdn.co.kr/profile/114/1771410723884.png"},
    "20372100005311821": {"name": "照&露西2", "image": "https://mod-file.dn.nexoncdn.co.kr/shop/949/1774672479562.png"}
}

DEFAULT_IMAGE = "https://example.com/default.png"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497592013166608484/-bQDkOKmZBbxRMXwkmgQqrFsk4cdrtKIuKfVlxk81XeXwqalZ-9VliOuSC5wI1YMcuRT"
DISCORD_WEBHOOK_URL_PAKA = "https://discord.com/api/webhooks/1502364012128637039/o9cJHlVQ4sibt4E-YVSki-TsNlaRSwjFH2kDaiqwl5qPnek5_UR4SWDVdZpfBYWRVbS7"

SPECIAL_PLAYERS = [
    "20372100008443475", # paka1
    "20372100005802883", # paka2
    "20372100004235799", # 死靈
    "20372100003186784", # 死靈妹01
    "20372100002734060", # 死靈妹02
]

# 💡 建議至少調到 30 ~ 60，避免過度頻繁觸發 Cloudflare 鎖 IP
CHECK_INTERVAL = 15 
API_URL_TEMPLATE = "https://mverse-api.nexon.com/social/v1/profile/{}"

last_known_data = {pid: {"is_online": None, "world_name": None} for pid in PLAYER_MAP.keys()}

def send_ip_blocked_warning(status_code):
    """當發現被鎖 IP 時，發送警告到 Discord"""
    print(f"⚠️ [警告] 你黑絲已造成妨礙風化: {status_code}。正在發送通知...")
    payload = {
        "embeds": [{
            "title": "⚠️ 黑絲維京人遭受官方妨礙風化制裁 (Error 1015)",
            "description": f"黑絲維京人目前被羈押禁見。\n**原因**：色色頻率過高，黑絲照已被 rate limit。\n**HTTP 狀態碼**：`{status_code}`\n\n倒數機制已啟動：**黑絲將被脫掉 10 分鐘**，隨後嘗試更換黑絲。",
            "color": 16744192,  # 橘色
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }]
    }
    # 同步通知兩個頻道
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"發送 IP 被鎖警告至 DC 失敗: {e}")

def check_players():
    global last_known_data
    print(f"[{time.strftime('%H:%M:%S')}] 啟動掃描...")

    for pid, info in PLAYER_MAP.items():
        time.sleep(0.4) 
        try:
            name = info["name"]
            custom_image = info.get("image", DEFAULT_IMAGE)
            url = API_URL_TEMPLATE.format(pid)
            
            # 偽裝稍微完整一點的瀏覽器頭
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            # 💡 核心新增：如果狀態碼不是 200 (例如 429 或 403)，判定為被鎖 IP
            if response.status_code != 200:
                print(f"❌ 擷取 {name} 失敗，狀態碼: {response.status_code}")
                if response.status_code in [429, 403, 1015]:
                    send_ip_blocked_warning(response.status_code)
                    print("😴 進入冷卻模式，暫停打擾 Nexon 10 分鐘...")
                    time.sleep(600)  # 暫停 600 秒 (10分鐘)
                    return           # 直接跳出這一輪的掃描，重新等待
                continue

            data_root = response.json().get('data', {})
            
            is_online = (data_root.get('isOnline') == 1)
            world_name = data_root.get('worldName') 
            p_code = data_root.get('profileCode', '未知')
            
            prev = last_known_data[pid]

            if prev["is_online"] is None:
                last_known_data[pid] = {"is_online": is_online, "world_name": world_name}
                continue

            should_notify = False
            status_msg = ""
            
            if is_online != prev["is_online"]:
                should_notify = True
                status_msg = "🟢 上線了！" if is_online else "🔴 下線了。"
            elif is_online and world_name != prev["world_name"]:
                should_notify = True
                status_msg = "🔄 切換世界"

            if should_notify:
                last_known_data[pid] = {"is_online": is_online, "world_name": world_name}
                current_world = world_name if world_name else "大廳或選單中"
                
                if is_online:
                    if "切換世界" in status_msg:
                        color = 16776960  
                        title_icon = "🔄"
                    else:
                        color = 65280     
                        title_icon = "🟢"
                else:
                    color = 16711680      
                    title_icon = "🔴"
                
                description = f"代碼：`{p_code}`\n狀態：**{status_msg}**"
                if is_online:
                    description += f"\n目前位置：`{current_world}`"

                payload = {
                    "embeds": [{
                        "title": f"{title_icon} 【{name}】{status_msg}",  
                        "description": description,
                        "thumbnail": {"url": custom_image}, 
                        "color": color,                                  
                        "footer": {"text": f"PPSN: {pid}"},
                        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                    }]
                }
                
                if pid in SPECIAL_PLAYERS:
                    requests.post(DISCORD_WEBHOOK_URL_PAKA, json=payload, timeout=10)
                    print(f"🚀 [dc2] 專屬通知: {name}")
                else:
                    requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
                    print(f"📣 [dc1] 一般通知: {name}")

        except Exception as e:
            print(f"檢查 {pid} ({info['name']}) 出錯: {e}")

def main_loop():
    while True:
        check_players()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("--- 正在嘗試發送啟動訊號到 Discord ---")
    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL, 
            json={"content": "🤖 維京已穿上黑絲待命！"},
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=10
        )
        if response.status_code in [200, 204]:
            print(f"✅ Discord 啟動訊號發送成功！(狀態碼: {response.status_code})")
        else:
            print(f"❌ Discord 拒絕請求，錯誤代碼: {response.status_code}")
            
    except Exception as e:
        print(f"💥 啟動訊號發送過程中發生異常: {e}")

    monitor_thread = threading.Thread(target=main_loop, daemon=True)
    monitor_thread.start()
    print("📡 後台監控線程已啟動，開始循環掃描。")

    print("🌐 正在啟動 Flask Web 服務...")
    run_web()
