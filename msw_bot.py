import requests
import time
import threading
from flask import Flask
import os

app = Flask('')

@app.route('/')
def home():
    return "MSW Bot with ProfileCode is Alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 設定區域 ---
PLAYER_MAP = {
    "20372100006053110": "黑絲維京人",
    "20372100000223997": "別時",
    "20372100005338018": "小波",
    "20372100003479787": "卡提作者",
    "20372100003567962": "妃姬作者",
    "20372100008583110": "ES(夜夜發貨號)",
    "20372100005894481": "平行",
    "20372100003096391": "幽幽子",
    "20372100001110251": "mimiming天使",
    "20372100002790823": "mimiming天使",
    "20372100004235799": "死靈作者",
    "20372100005999546": "TJ",
    "20372100005764633": "TJ",
    "20372100005118171": "兔仔",
    "20372000486671177": "韓國愛芮",
    "20372100005311821": "照作者",
    "20372100003863084": "阿卡利作者",
    "20372100000180209": "PLAT",
    "20372100003462165": "奧米加獸作者",
    "20372100000208070": "珊璞作者"
}

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497592013166608484/-bQDkOKmZBbxRMXwkmgQqrFsk4cdrtKIuKfVlxk81XeXwqalZ-9VliOuSC5wI1YMcuRT"
CHECK_INTERVAL = 10 

API_URL_TEMPLATE = "https://mverse-api.nexon.com/social/v1/profile/{}"

last_known_status = {pid: None for pid in PLAYER_MAP.keys()}

def check_players():
    global last_known_status
    print(f"[{time.strftime('%H:%M:%S')}] 掃描中...")

    for pid, name in PLAYER_MAP.items():
        try:
            url = API_URL_TEMPLATE.format(pid)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            
            response = requests.get(url, headers=headers, timeout=10)
            res_json = response.json()
            user_data = res_json.get('data', {})
            
            is_online = (user_data.get('isOnline') == 1)
            p_code = user_data.get('profileCode', '未知') # 抓取 5 碼 ID
            img_url = user_data.get('profileImageUrl', '') # 抓取頭像
            
            if last_known_status[pid] is None:
                last_known_status[pid] = is_online
                continue

            if is_online != last_known_status[pid]:
                last_known_status[pid] = is_online
                status_text = "🟢 上線了！" if is_online else "🔴 下線了。"
                color = 3066993 if is_online else 15158332 # 綠色或紅色
                
                # 建立 Discord Embed 通知
                payload = {
                    "embeds": [{
                        "title": f"楓之谷世界 狀態通知",
                        "description": f"玩家：**{name}**\n代碼：`{p_code}`\n狀態：**{status_text}**",
                        "thumbnail": {"url": img_url},
                        "color": color,
                        "footer": {"text": f"PPSN: {pid}"},
                        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                    }]
                }
                
                requests.post(DISCORD_WEBHOOK_URL, json=payload)
                print(f"📣 通知發送: {name} ({p_code}) {status_text}")

        except Exception as e:
            print(f"檢查 {name} 出錯: {e}")

def main_loop():
    while True:
        check_players()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    threading.Thread(target=main_loop, daemon=True).start()
    run_web()
