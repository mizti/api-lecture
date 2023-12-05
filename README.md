# api-lecture
Fast APIでAPIを作成しデプロイする簡単なサンプル

# 必要パッケージのインストール

```basha
pip install -r requirements.txt
```

# 動かし方(ローカル)

## 起動
```bash
cd app
uvicorn main:app --reloa
```

## 動作確認

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
