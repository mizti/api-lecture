# テスト環境の使用方法

## 概要

このテスト環境は、APIをローカルでテストするためのMySQLとFastAPIの設定を提供します。Dockerを使用してMySQLを提供し、APIをローカルで実行します。

## 前提条件

以下のソフトウェアがインストールされている必要があります：

- Docker
- Docker Compose
- Python 3.x
- pip (Pythonパッケージマネージャー)

## テスト環境のセットアップと実行

### 0. Application Insights接続文字列の設定(Otional)
Application Insightsにテレメトリを連携する場合には接続文字列をAPPLICATIONINSIGHTS_CONNECTION_STRINGに設定します。
```bash
export APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx;IngestionEndpoint=https://japaneast-1.in.applicationinsights.azure.com/;LiveEndpoint=https://japaneast.livediagnostics.monitor.azure.com/;ApplicationId=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 1. テスト環境の起動

テスト環境を起動するには、以下のコマンドを実行します：

```bash
cd test
./start_test_env.sh
```

このスクリプトは以下の処理を行います：
- テスト用のDockerネットワークを作成
- MySQLコンテナを起動
- テーブルの初期化（student, lectureテーブルの作成）
- FastAPI アプリケーションをポート8003で起動

### 2. テスト環境の停止

テスト環境を停止するには、以下のコマンドを実行します：

```bash
cd test
./stop_test_env.sh
```

このスクリプトは以下の処理を行います：
- MySQLコンテナの停止と削除
- テスト用のDockerネットワークの削除

## テスト環境での動作確認

APIは以下のエンドポイントで利用可能です：

### 講義（Lectures）API

```bash
# 講義の作成
curl -X POST http://localhost:8003/lectures \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Python",
    "professor": "John Doe",
    "credits": 3,
    "description": "Learn the basics of Python programming"
  }'

# 全講義の取得
curl -X GET http://localhost:8003/lectures

# 特定の講義の取得
curl -X GET http://localhost:8003/lectures/1

# 講義の更新
curl -X PUT http://localhost:8003/lectures/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Python",
    "professor": "Jane Smith",
    "credits": 4,
    "description": "Advanced Python programming concepts"
  }'

# 講義の削除
curl -X DELETE http://localhost:8003/lectures/1
```

## 環境変数

テスト環境では以下の環境変数が設定されます：

```bash
MYSQL_HOST=localhost
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_DB=lecture_db
MYSQL_PORT=3306
```

## データベース構造

### lectureテーブル
```sql
CREATE TABLE lecture (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    professor VARCHAR(255) NOT NULL,
    credits INT NOT NULL,
    description TEXT
);
```

## トラブルシューティング

1. ポートの競合が発生した場合:
   - 既存のuvicornプロセスを停止: `pkill uvicorn`
   - 既存のMySQLコンテナを停止: `docker stop $(docker ps -q --filter name=mysql)`

2. データベース接続エラーが発生した場合:
   - MySQLコンテナが正常に起動しているか確認: `docker ps`
   - ログの確認: `docker logs test_mysql-test_1`
