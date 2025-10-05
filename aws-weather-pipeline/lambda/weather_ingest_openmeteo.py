import json
import boto3
import urllib.request
from datetime import datetime, timezone, timedelta

s3 = boto3.client("s3")

def lambda_handler(event, context):
    # 取得対象の座標（例：東京）
    latitude = 35.6895
    longitude = 139.6917

    # Open-Meteo API URL
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    # APIコール
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())

    # 保存用のファイル名（UTC→JST）
    now = datetime.now(timezone(timedelta(hours=9)))
    file_name = f"raw/weather_{now.strftime('%Y%m%d_%H%M%S')}.json"

    # S3アップロード
    bucket_name = "weather-raw-apne1"  # ← 自分のバケット名に置き換えてOK
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(data, ensure_ascii=False).encode("utf-8")
    )

    return {
        "status": "ok",
        "key": file_name
    }
