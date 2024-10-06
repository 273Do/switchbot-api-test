import time
import hashlib
import hmac
import base64
import uuid
import requests
import pprint

# クライアントシークレットをbytes方式に変更
def make_secret(secret_key):
    secret_key = bytes(secret_key, 'utf-8')
    return secret_key

# signを作成
def make_sign(secret_key, t, nonce):
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    sign = base64.b64encode(hmac.new(secret_key, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign

# tを作成
def make_t():
    t = int(round(time.time() * 1000))
    return str(t)

# nonceを作成
def make_nonce():
    nonce = str(uuid.uuid4())
    return nonce

if __name__ == "__main__": 

    # SwitchBotアプリから取得
    secret_key = "YOUR_SECRET_KEY" # 文字列で入力 
    token = "YOUR_TOKEN" # 文字列で入力

    # デバイスID
    device_id = "DEVICE_ID" # 文字列で入力

    # 認証パラメータを作成する
    secret_key = make_secret(secret_key)
    t = make_t()
    nonce = make_nonce()
    sign = make_sign(secret_key, t, nonce)

    # URL指定
    url = "https://api.switch-bot.com/v1.1/devices/{}/status".format(device_id)

    # APIHeader作成
    headers = {
        "Authorization": token,
        "sign": sign,
        "t": t,
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf-8"
    }

    # requests処理
    response = requests.get(url, headers=headers)

    # レスポンス処理とデータ型変更
    pprint.pprint(response.json())