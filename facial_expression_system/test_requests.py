import requests
import dropbox
import sys
from dropbox.files import WriteMode
from dropbox.sharing import ListSharedLinksError

# DropboxおよびInstagram APIに必要なアクセストークン
DROPBOX_ACCESS_TOKEN = 'sl.u.AFdZOkI-QXvA6pzTMxiPNfQuWRlkGM_P0JZVK-EBKvb3rrZceJQ60W6oYU5dgAw81OFEvVAA2RWCWxEeSLyInN5RGifPEeXocXb0QIXyanEwIU-3TH18Bl1ZzZlzwC_m7pMVSoEruQQGgT1EH_VRsnTfS5Y8uctAoe1Z6cGsUiiVTO_rbQDrliEFj-Z_Z255QdX7j7U9h-GFZSxNdSi34ClK4QQrzgprJGbc9ZExYdmYHB55qpzCJ2u9nSTEtODm7yNOLcNBB85uOo4oRO4CSadJn1HOFWSo9zTI4LSUj_AgRZasQ9T9QS5RkHSXIXS44ylaKrcsF4JPDeEZQRyQyBEzjSlN2_nLPqU1Zqh-bTuGUyv7Oct8EXrS99955ppWGE9-n8p9hgJcB6f37lsPO8GECaYyszOj44EYOGK-Pu_kVTCB8DmEZWovAGV8dL8eGSqh6T2F3tDMCcmvXMn9Rx5f1Br50Zo4sD7z_7HA3xh5tqD9gfo_yX_u2u-uGSvscJuC0JsBzu4vuTWsrBXZmhl8s1Eum2_wwYlcKWcCnpnG63z4n7zl2ea2GGU2CQIf0hH-Fz39Q2l6Eb8f2ajwUmCQXprpXQp-EBCmYtwsxOkPIO59oAcCpNtmE4NMl3P6ROFvcaIt5_1rCkuNeDz4DQJ07o0-3olxBPmcuwpPoCJePPf7svxMttpUpiB2xe2Nv-12RtHdKGVyr4VyboCDvZcTzZP83Res2V0l6UzMOeevwceTYj52sVbrSQsySLTFysV9EW61unCIyQaeDOmIkYB9-LjYCqApyZ-hBLB2SwduLEpxd8AgiQ9kDWYQxtVihhXbRTe9CacIa7W9pHWcg9wb0IR3lO0l7kA99WIeZducgidy0B_t6z-XfNXH3Um--qGqqHZrINfPZ8zOPvImt-FZwM1NanJsDHGU_-0EB9UcUoX_2MLsOru_55fGcZ7B7x-JAqH5w9gQjwlz_pczBvSv_wXQlGMtFxQbRb_cJvbHvLRIg0xNAiA7aGOPuFqsdoATVfeeqjdtnpJzD02zPb7WJabKlVkD6bui3KHaMpK-yxcC_mTA__Hu4P-V_NwaIqymZU18QGaBSYlaC4kG-kOymN1jlKXAAMP4iz3VrNb0MlCoN-w1u63FOQSk74MR92WKibjaXmLlL18c4GxqhRVU2MDYIsWYb74nObZCIxXphqQ4fByMb9hmI9AHCn3CivCTWQDHUQnq9wkQBy_P1swiUzdck9ccUgxiVyvzrdaRNN91SBDfiA5J8Y-OEAEAVXW_V9g7jEDaV_mtsDz9L2fb-s9PTb0XXsdzaBf_FaDPkNdvOS5dwHKFxJghSQBk-Vw9bqeNftezJG4Co9yxXbxolitBd1A2K0d51u-8EFZAZDad4kQv3S6fnhk45qM1ldjYSUq-DKX2ro6WpQFfA9ZSEVUNJDbfgIV4Xg0jJnE8qg'  # Dropboxのアクセストークン（実際には有効なものに変更してください）
INSTA_BUSINESS_ID = '17841467681337524'  # InstagramビジネスアカウントID
INSTA_ACCESS_TOKEN = 'EAARSsZCQrzCcBOyHKLrZAmJyqB8tK6RxxwmM84TQpZAeNgA6LMiftZCoQgIIgzZAonrrrnphlA4VmSnZBU1CXp7zQtHk99ssrb4KKDZBVZBHZCJZCtrXwoT3zejsBCPAXBKNKMYOrdCJXmKvJ06vss2Hx3K4pmVy9XdiJMtVsPlw8DK0tiMr36NdvWONjJypZBN2LJJ'  # Instagram API用アクセストークン

# ローカルファイルをDropboxにアップロードする関数
def upload_to_dropbox(local_path, dropbox_path):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open(local_path, 'rb') as file:
        dbx.files_upload(file.read(), dropbox_path, mode=WriteMode('overwrite'))
    return dbx  # Dropbox APIクライアントを返す

# Dropbox内のファイルに対して共有リンクを取得する関数
def get_shared_link(dbx, dropbox_path):
    try:
        links = dbx.sharing_list_shared_links(path=dropbox_path)
        if links.links:
            return links.links[0].url
        link = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        return link.url
    except ListSharedLinksError as e:
        print(f'Error retrieving shared links: {e}')
        return None

# Instagramに画像をアップロードする関数
def upload_to_instagram(image_url, caption):
    post_data = {
        'image_url': image_url,
        'caption': caption,  # キャプションを動的に設定
        'media_type': 'IMAGE'
    }

    url = f'https://graph.facebook.com/v17.0/{INSTA_BUSINESS_ID}/media'
    headers = {
        'Authorization': f'Bearer {INSTA_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=post_data, headers=headers)
        response.raise_for_status()
        creation_id = response.json().get('id')
        if creation_id:
            publish_url = f'https://graph.facebook.com/v17.0/{INSTA_BUSINESS_ID}/media_publish'
            publish_data = {'creation_id': creation_id}
            publish_response = requests.post(publish_url, json=publish_data, headers=headers)
            publish_response.raise_for_status()
            print('Publish Response:', publish_response.json())
        else:
            print('Failed to create media container')
    except requests.exceptions.RequestException as error:
        print('Instagram APIのリクエスト中にエラーが発生しました:', error.response.json() if error.response else error)

# メイン処理を行う関数
def main(file_path, caption):
    dropbox_path = '/images/image.jpg'

    dbx = upload_to_dropbox(file_path, dropbox_path)
    shared_link = get_shared_link(dbx, dropbox_path)
    if shared_link:
        print(f'変換前のDropbox URL: {shared_link}')
        shared_link_transformed = shared_link.replace('=0', '=1', 1)
        print(f'変換後のDropbox URL: {shared_link_transformed}')
        upload_to_instagram(shared_link_transformed, caption)  # キャプションを渡す
    else:
        print("Dropboxリンクの取得に失敗しました。")

# スクリプトが直接実行された場合にのみメイン処理を行う
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("画像パスとキャプションが指定されていません。")
        sys.exit(1)

    file_path = sys.argv[1]
    caption = sys.argv[2]  # キャプションを受け取る
    main(file_path, caption)
