#dropbox認証のためのURL表示
APP_KEY = 's9rphtvwfdhbu0v'  # DropboxアプリのApp key

# 認証URLを生成
auth_url = f"https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&response_type=code&redirect_uri=https://www.dropbox.com/1/oauth2/redirect_receiver"
print(f"認証URL: {auth_url}")
