# `uecli`

電通大のCLIツールです。コマンドラインからシラバス検索、成績参照、図書館の貸出リストなどを見ることができます

## インストール

```sh
pip install uecli
```

## 使い方

- シラバスを検索

```sh
python3 -m uecli syllabus search -s 'コンピュータサイエンス'
```

- シラバスを取得し、Markdown形式で表示

```sh
python3 -m uecli --markdown syllabus get --year 2021 -t 31 -c 21124255
```

- 2021年度前期の成績を取得

```sh
python3 -m uecli grades --year 2021 --semester 1 get
```

## 認証

認証には以下の方法があります

- ターミナルでユーザ名・パスワード、二段階認証コードを入力
- 環境変数に設定

> 認証情報の保存に以下のファイルが作成されます
> 
> - `~/.uecli.cookies.lwp`
> - `~/.uecli.campussquare.json`

### 環境変数に設定する場合

|||
|---|---|
|`UEC_USERNAME`|UECアカウントのユーザー名（shibboleth）|
|`UEC_PASSWORD`|UECアカウントのパスワード|
|`UEC_MFA_SECRET`|二段階認証の秘密鍵*|

### 二段階認証の秘密鍵の取得方法

**以下の方法では二段階認証コードが変わるため、認証アプリ等で再設定が必要になります**

1. [二段階認証設定ページ](https://axiole.cc.uec.ac.jp/)へログイン
2. ２段階認証設定状況:の「２段階認証設定」ボタンを押す
3. トークンアプリを使用するにチェックを入れます
4. 次のようなURIがあるので`secret=`の後の部分をコピーします

    ```
    otpauth://totp/axiole:z2510999?secret=ABCDEFGHIJKLMNOPQRSTUVWXYZ&issuer=axiole
    ```

    上記のURIの場合`ABCDEFGHIJKLMNOPQRSTUVWXYZ`です
5. QRコードを読み取りスマホなどの認証アプリへも登録します
6. 次へを押し、画面に従い設定を完了します
7. 環境変数を設定します

    - Linux, macOS

        ```sh
        # ~/.bashrc
        # UECアカウント
        export UEC_USERNAME="z2510999"
        export UEC_PASSWORD="hogehogehoge"
        # 二段階認証の秘密鍵
        export UEC_MFA_SECRET="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ```

    - WindowsはGUIから行います

8. **環境変数の値を書いたファイルは他人が読めないようにしてください**

    - Linux, macOS

        ```sh
        # bashの場合（※solはデフォルトでtcshです）
        chmod 600 ~/.bashrc
        ```

9. 必要に応じ環境変数を再読込してください

    - Linux, macOS

        ```sh
        . ~/.bashrc
        ```