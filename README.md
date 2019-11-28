# 概要
## 目的
気軽に使える自動化テストができる、seleniumライブラリが欲しい

## 要件
- どうせ夜中に走らせるので、処理速度は犠牲にしてもOK
- システム毎に改修すべき部分を明確にくくりだしたい
- システム毎のコードができたら、非エンジニアでも使えるようにしたい
- 結果はとりあえずスクショの目視確認でOK
    - 後々は判定も入れたい

# 使用方法
## ブラウザ
- chrome
    - headless
- firefox
    - headless
- IE
- Edge

## ディレクトリ構成例
```
main.py
  |-  setting.ini
  |-  img（証明書提出用ポジション取得用画像ファイル）
  |   |-  chrome
  |   |-  firefox
  |   |-  ms
  |- lib
  |   |-  logwrapper.py
  |   |-  pyautoguiwrapper.py
  |   |-  seleniumwrapper.py
  |   |-  systemspecific.py
  |   |-  pyautotest.py
  |- profile（firefox用ユーザプロファイル例）
  |- scenario（シナリオディレクトリ例）
  |   |-  chrome
  |   |     |-  login.json
  |   |-  firefox
  |   |-  ms
  |- result（結果ディレクトリ例）
      |-  chrome
            |-  login
                  |-  result.log
                  |-  cookie.pkl
                  |-  000.png
                  |-  001.png
```

## 内容
- シナリオディレクトリに配置されたjsonファイルを全て読み込み
- シナリオに記載されたコマンドを実行、設定値を伴う場合は同名パラメータの設定を行う
- 結果ディレクトリにjsonファイルの同名ディレクトリを作成し、結果ファイルを出力
- 各コマンド実行時にコマンド名をログに出力し、スクリーンショットを吐き出す
- ブラウザ閉じる際に「cookieファイル」を吐き出す
- 指定されたコマンドが実行できなかった場合、ログ及びスクリーンショットを取得する

## 使い方
    python main.py -s [シナリオディレクトリ] -r [結果ディレクトリ]
| オプション名 | 内容                   | 説明                         |
| ------------ | ---------------------- | ---------------------------- |
| -s           | [シナリオディレクトリ] | jsonシナリオ配置ディレクトリ|
| -r           | [結果ディレクトリ]     | テスト結果配置ディレクトリ   |

setting.ini

    [paths]
    scenario_dir = D:\dev\pyAutoTest\scenario
    result_dir = D:\dev\pyAutoTest\result

- 基本は設定ファイルに記載のディレクトリを使用
- テスト中などでディレクトリを指定したい場合のみ、上記オプションでディレクトリ変更可能

# まとめ
- システムに合わせてsystemspecific.pyを改修
- テストしたいシナリオファイルを作成
- 実行し、スクショで成否を確認

# コード解説
## main.py
引数及び設定ファイルの解析
シナリオディレクトリ及び結果ディレクトリを実行ファイルに送る

## logwrapper.py
ログ出力
出力ディレクトリはコンストラクタで指定

## pyautoguiwrapper.py
pyautoguiラッパー
マウス操作を行う
クライアント証明書の提出にのみ使用

### __search_from_image
指定された画像の表示位置を取得
描画されるまで指定秒数リトライする
指定秒数経過後も表示がなかった場合、エラーとする

### move_click
指定された画像の表示位置へマウスを移動させ、クリック
引数によって画像からの相対位置を指定可能

### click
指定された画像の表示位置をクリック
マウス移動を行わないため高速（だが、成否の判断がわかりづらい）

## seleniumwrapper.py
seleniumラッパー
使用頻度の高い処理だけ抜き出し、エラー処理を設定
基本的なDOM操作のラッパーを上部に、ブラウザ依存の処理を下部に配置

## systemspecific.py
seleniumwrapper.pyの子クラス
seleniumラッパーを利用し、調査したいコマンドを設定

## pyautotest.py
シナリオディレクトリからjsonファイルを展開
コマンド及びパラメータを取得し、systemspecificに設定されたコマンドを実行

# シナリオファイル
```
{
        "BROWSE_CONF": {　　　　　　　　　　　　　　　　　ブラウザ設定
        "browse_type": "firefox",　　　　　　　　　　　　　ブラウザの種類
        "headless": false,　　　　　　　　　　　　　　　　　ヘッドレス機能のon/off
        "profile_path": "",　                          ユーザプロファイルのディレクトリ
        "profile_user": ""　　　　　　　　　　　　　　     ユーザプロファイルのユーザ名
    },
    "CMDS": [　　　　　　　　　　　　　　　　　　　　　　　コマンド
        "access",
        "uid",
        "password",
        "submit",
        "toggle",
        "logout",
        "close"
    ],
    "PARAMETERS": {　　　　　　　　　　　　　　　　　　　パラメータ名（コマンド名と一致したものが引数）
        "access" : "",                                  URL
        "uid" : "",                                     ユーザ名
        "password": "",                                 パスワード
    }
}
```