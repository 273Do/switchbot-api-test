import time
import hashlib
import hmac
import base64
import uuid
import requests

# クライアントシークレットをbytes型に変更
def make_secret(secret_key):
    secret_key = bytes(secret_key, 'utf-8')
    return secret_key

# signを作成
def make_sign(secret_key, t, nonce, token):
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    sign = base64.b64encode(hmac.new(secret_key, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign.decode('utf-8')

# tを作成
def make_t():
    t = int(round(time.time() * 1000))
    return str(t)

# nonceを作成
def make_nonce():
    nonce = str(uuid.uuid4())
    return nonce

if __name__ == "__main__": 
    # SwitchBotアプリから取得した情報
    secret_key = "YOUR_SECRET_KEY" # 文字列で入力 
    token = "YOUR_TOKEN" # 文字列で入力
    device_id = "DEVICE_ID" # 文字列で入力

    # 必要なパラメータを作成
    secret_key_bytes = make_secret(secret_key)
    t = make_t()
    nonce = make_nonce()
    sign = make_sign(secret_key_bytes, t, nonce, token)

    # URL指定 - 電源をオンにするためのURL
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/commands"

    # API header作成
    headers = {
        "Authorization": f"Bearer {token}",  # Bearerトークンで送る
        "sign": sign,
        "t": t,
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf-8"
    }

    # 電源をオンにするためのコマンド
    command_body = {
        "command": "turnOn",  # 電源をオンにするコマンド
        "parameter": "default",  # デフォルトのパラメータ
        "commandType": "command"
    }

    # POSTリクエストを送信して、電源をオンにする
    response = requests.post(url, headers=headers, json=command_body)

    # 結果を表示
    if response.status_code == 200:
        print("Power on command sent successfully.")
    else:
        print(f"Failed to send power on command: {response.status_code}")