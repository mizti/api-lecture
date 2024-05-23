# api-lecture
Fast APIでAPIを作成しデプロイする簡単なサンプル

# 必要パッケージのインストール

```basha
pip install -r app/requirements.txt
```

# 動かし方(ローカル)

## 環境変数の設定
```bash
export PYTHONPATH=app:$PYTHONPATH
```
appをPYTHONPATHに入れることでルートディレクトリからuvicornを起動してもモジュール参照が失敗しないようにします。

## 起動
（api-lecture直下で以下を実行する）
```bash
uvicorn app.main:app --reload
```

# 動かし方(ローカル/Docker)
（api-lecture直下で以下を実行する）
ビルド
```bash
 docker build -t myfastapi ./app
```
ビルド時のデバッグを要する場合には
```bash
 docker build -t myfastapi ./app --progress=plain --no-cache
```

実行
```bash
docker run -p 80:80 myfastapi
```

# 動作確認

* Hello APIの呼び出し
```bash
curl http://127.0.0.1:8000/hello
```

```
Hello!
```

* POST /students APIの呼び出し
```bash
curl http://127.0.0.1:8000/students -i -X POST -H'Content-Type: application/json' -d'{
    "name": "John Doe",
    "mail": "johndoe@example.com",
    "gender": "Male",
    "interest": ["Science", "Technology"],
    "description": "Hello Everyone!"
}'
```

```
HTTP/1.1 200 OK
date: Fri, 01 Dec 2023 07:14:02 GMT
server: uvicorn
content-length: 139
content-type: application/json

{"id":1,"name":"John Doe","mail":"johndoe@example.com","gender":"Male","interest":["Science","Technology"],"description":"Hello Everyone!"}
```

* GET /students の呼び出し

```
curl http://127.0.0.1:8000/students
```

```
[{"id":1,"name":"John Doe","mail":"johndoe@example.com","gender":"Male","interest":["Science","Technology"],"description":"Hello Everyone!"},{"id":2,"name":"John Doe","mail":"johndoe@example.com","gender":"Male","interest":["Science","Technology"],"description":"Hello Everyone!"}]
```

* GET /students/{students_id}の呼び出し

```
curl http://127.0.0.1:8000/students/2
```

```
{"id":2,"name":"John Doe","mail":"johndoe@example.com","gender":"Male","interest":["Science","Technology"],"description":"Hello Everyone!"}
```
# App Serviceへのデプロイ

## App Serviceの構築

* ログイン

```bash
az login
```

* リソースグループの作成
```bash
az group create --name myResourceGroup --location japaneast
```

* App Serviceプランを作成
```bash
az appservice plan create --name yourappname --resource-group myResourceGroup --sku B1 --is-linux
```

* Webアプリの作成
```bash
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name lecture-api --runtime "PYTHON:3.12" --deployment-local-git
```

* スタートアップコマンドの設定
設定 > 構成 > 全般設定 > スタックの設定 > スタートアップコマンドに
```bash
export PYTHONPATH=app:$PYTHONPATH
pip install -r app/requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0
```
と設定を行います。


* Webアプリのデプロイ
```bash
az webapp up --name lecture-api --runtime PYTHON:3.12 --sku B1 --location japaneast --resource-group myResourceGroup --plan myAppServicePlan
```
このコマンドはカレントディレクトリの内容をアップロードしてWebAppを作成します（既にある場合は更新します）。
（プロジェクトのルートディレクトリで実行してください。）


ログを見たい場合には
```bash
az webapp up --name lecture-api --runtime PYTHON:3.12 --sku B1 --location japaneast --resource-group myResourceGroup --plan myAppServicePlan --logs
```
とlogsオプションを指定してください。

（なお、デプロイが完了するまで2-3分程度掛かります。
https://<app-name>.azurewebsites.net/hello
にアクセスして動作状況を確認してください）

# MySQLのデプロイ


# App ServiceからMySQLへの接続

このプログラムはMYSQL_HOSTが設定されている場合にはメモリ上ではなくMySQLにデータを格納するストアクラスを用いる設計になっています。

* 接続情報の設定
.env.exampleを.envファイルにコピーし、デプロイしたMySQLへの接続内容を.envファイルに設定します。

```bash
cp .env.example .env
vi .env (.envファイルを編集します)
```

* App Serviceのスタートアップコマンドを修正

App Serviceでスタートアップコマンドを修正します
```bash
source .env
pip install -r app/requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0
```
(export PYTHONPATH=app:$PYTHONPATH は.envに含まれています)

再度デプロイを行います。（ルートディレクトリで実行してください）
```bash
az webapp up --name lecture-api --runtime PYTHON:3.12 --sku B1 --location japaneast --resource-group myResourceGroup --plan myAppServicePlan
```
