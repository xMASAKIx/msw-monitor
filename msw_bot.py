import requests
import time
import threading
from flask import Flask
import os

# --- 網頁偽裝區域 (防止 Render 部署失敗) ---
app = Flask('')

@app.route('/')
def home():
    return "MSW Bot is Alive!"

def run_web():
    # Render 預設使用 10000 埠口
    app.run(host='0.0.0.0', port=10000)

# --- 設定區域 ---
PLAYER_MAP = {
    "20372100006053110": "黑絲維京人",
    "20372100000223997": "別時0ZOlJ",
    "20372100005338018": "小波2CPyH",
    "20372100003479787": "艾蓮作者F91FI",
    "20372100003567962": "妃姬作者w99gQ",
    "20372100008583110": "ES(夜夜發貨號)uRiUE",
    "20372100005894481": "平行jo2TC",
    "20372100003096391": "幽幽子6tG5H",
    "20372100001110251": "mimiming天使(tJL7G)",
    "20372100002790823": "mimiming天使(M1l8R)",
    "20372100004235799": "死靈作者xJGZP",
    "20372100005999546": "TJ(aSGyM)",
    "20372100005764633": "TJ(WECNP)",
    "20372100005118171": "兔仔仔XHmvQ",
    "20372000486671177": "韓國愛芮(X1I1O)",
    "20372100005311821": "照作者(iGDMQ)",
    "20372100003863084": "阿卡利作者(uMPzK)",
    "20372100000180209": "PLAT(IPvsD)",
    "20372100003462165": "奧米加獸作者(8DE8J)",
    "20372100000208070": "珊璞作者1W7aL"
}

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497592013166608484/-bQDkOKmZBbxRMXwkmgQqrFsk4cdrtKIuKfVlxk81XeXwqalZ-9VliOuSC5wI1YMcuRT"
CHECK_INTERVAL = 10  # 建議設 15-20 秒，避免太頻繁被 Nexon 擋 IP

API_URL_TEMPLATE = "https://mverse-api.nexon.com/social/v1/profile/{}"

# 紀錄狀態
last_known_status = {pid: None for pid in PLAYER_MAP.keys()}

def check_players():
    global last_known_status
    print(f"[{time.strftime('%H:%M:%S')}] 掃描 {len(PLAYER_MAP)} 位玩家中...")

    for pid, name in PLAYER_MAP.items():
        try:
            url = API_URL_TEMPLATE.format(pid)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            
            is_online = (data['data']['isOnline'] == 1)
            
            if last_known_status[pid] is None:
                last_known_status[pid] = is_online
                print(f"初始紀錄: {name} ({'上線' if is_online else '離線'})")
                continue

            if is_online != last_known_status[pid]:
                last_known_status[pid] = is_online
                status_text = "🟢 上線了！" if is_online else "🔴 下線了。"
                
                payload = {"content": f"【維京穿黑絲通知】**{name}** {status_text}"}
                requests.post(DISCORD_WEBHOOK_URL, json=payload)
                print(f"📣 通知發送: {name} {status_text}")

        except Exception as e:
            print(f"檢查 {name} 出錯: {e}")

if __name__ == "__main__":
    # 1. 在背景啟動 Flask 網頁伺服器，讓 Render 偵測到服務
    threading.Thread(target=run_web, daemon=True).start()
    
    # 2. 執行監控主迴圈
    print("🚀 MSW 極速監控模式 (免費 Web 方案) 啟動")
    while True:
        check_players()
        time.sleep(CHECK_INTERVAL)
