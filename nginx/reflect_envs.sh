#!/bin/sh

# 環境変数を使用して設定ファイルを生成
envsubst '$API_ADDRESS' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
echo "This is an error message.stderr" >&2
echo $API_ADDRESS
echo `cat /etc/nginx/conf.d/default.conf`

# 接続テスト
#echo | openssl s_client -connect fastapi.internal.graypebble-68635b91.japaneast.azurecontainerapps.io:443 -quiet
