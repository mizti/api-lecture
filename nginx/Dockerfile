FROM nginx:latest

# 設定ファイルテンプレートとエントリポイントスクリプトをコンテナにコピー
COPY default.conf.template /etc/nginx/conf.d/default.conf.template
COPY reflect_envs.sh /docker-entrypoint.d/reflect_envs.sh

# 実行可能にする
RUN chmod +x /docker-entrypoint.d/reflect_envs.sh

# 80番ポートを公開
EXPOSE 80

# エントリポイントの設定
#ENTRYPOINT ["/entrypoint.sh"]
