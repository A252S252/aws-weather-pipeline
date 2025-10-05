import boto3

glue = boto3.client("glue")

def lambda_handler(event, context):
    crawler_name = "weather_raw_crawler"  # Glueで作成したクローラー名
    try:
        glue.start_crawler(Name=crawler_name)
        return {"status": "started", "crawler": crawler_name}
    except glue.exceptions.CrawlerRunningException:
        return {"status": "already_running"}
    except Exception as e:
        return {"error": str(e)}
