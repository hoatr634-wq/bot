import requests
import time
from datetime import datetime
import json

class MinhLoi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://dash.lemonhost.me/api/user/billingafk"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "vi-VN",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "origin": "https://dash.lemonhost.me",
            "referer": "https://dash.lemonhost.me/components/billingafk//billingafk/dist/afk.html",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"
        }
    
    def get_status(self):
        try:
            response = requests.get(f"{self.base_url}/status", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Lỗi khi lấy status: {e}")
            return None
    
    def send_afk(self, minutes=1):
        try:
            payload = {"minutes_afk": minutes}
            response = requests.post(f"{self.base_url}/work", headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Lỗi khi gửi AFK: {e}")
            return None
    
    def display_status(self, status_data):
        if not status_data or not status_data.get('success'):
            return
        
        data = status_data.get('data', {})
        print("\n" + "="*50)
        print("📊 THÔNG TIN TÀI KHOẢN")
        print("="*50)
        print(f"💰 Credits hiện tại: {data.get('user_credits_formatted', 'N/A')}")
        print(f"⏱️  Tổng thời gian AFK: {data.get('minutes_afk', 0)} phút")
        print(f"⚡ Credits/phút: {data.get('credits_per_minute', 0)}")
        print("="*50 + "\n")
    
    def run(self, interval=60):
        print("🚀 Bắt đầu tool treo AFK Lemon")
        print(f"⏰ Gửi request mỗi {interval} giây\n")
        
        status = self.get_status()
        if status:
            self.display_status(status)
        
        afk_count = 0
        while True:
            try:
                result = self.send_afk(minutes=1)
                if result and result.get('success'):
                    afk_count += 1
                    data = result.get('data', {})
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] ✅ AFK #{afk_count} | +{data.get('credits_awarded', 0)} Credits")
                else:
                    print(f"⚠️  Lỗi: {result.get('error_message', 'Unknown error')}")
                
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n⛔ Đã dừng tool!")
                break
            except Exception as e:
                print(f"❌ Lỗi hệ thống: {e}")
                time.sleep(interval)

if __name__ == "__main__":
    # CHỖ NÀY CẦN CHÚ Ý:
    # Thay 'TOKEN_CUA_BAN' bằng mã Bearer Token lấy từ Network tab trên trình duyệt
    API_KEY = "fp_680a166d5dc4b21a79f694f6c10a09630092fcbcb5cca0a5801fa4d178fe5727" 
    
    afk = MinhLoi(API_KEY)
    afk.run(interval=61) # Để 61s cho chắc chắn không bị rate limit