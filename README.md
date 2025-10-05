# ☁️ AWS Weather Data Pipeline

## 概要
外部の天気APIから定期的に気象データを取得し、
AWS上で自動的に収集・整形できるパイプラインを構築

## アーキテクチャ
![architecture](architecture/aws_weather_pipeline.png)

### 使用サービス
- **Amazon EventBridge**：Lambdaを定期実行（1時間ごと・1日ごと）
- **AWS Lambda**：天気APIを呼び出し、S3に生データを保存
- **Amazon S3**：raw（生データ）／curated（加工データ）を格納
- **AWS Glue**：ETL処理（S3→S3）
- **Amazon Athena**：S3上のデータをSQLで分析

## フロー概要
1. EventBridgeがLambdaを定期起動
2. Lambdaが外部APIからデータを取得し、S3（raw）に保存
3. Glueがrawデータをcuratedデータに変換
4. AthenaでSQLクエリによる分析が可能に

## デプロイ（IaC）
`iac/template.yaml` をCloudFormationまたはAWS SAMでデプロイすることで、
全構成を自動で構築できます。

```bash
aws cloudformation deploy \
  --template-file iac/template.yaml \
  --stack-name weather-pipeline \
  --capabilities CAPABILITY_IAM
