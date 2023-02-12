# 東京都スポーツ施設 一括抽選申込サービス
[東京都スポーツ施設サービス](https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/homeIndex.html) で複数ユーザーの抽選申込と抽選結果確認を一括で行うためのサービスです。
サークルのメンバー全員分の抽選申込が大変で困っている人のために作りました。 [Heroku](https://jp.heroku.com/) で公開していましたが、2022年11月のHeroku有料化に伴い本サービスも終了しました。

## 画面
### ログイン
<kbd><img src="https://user-images.githubusercontent.com/11259807/218260429-113079bf-1d14-46e7-8dba-0b66ac27875e.png" width="100px"></kbd>
<kbd><img src="https://user-images.githubusercontent.com/11259807/218260729-d9a5d78f-7a59-4d75-91f4-4c66a20636fa.png" width="100px"></kbd>
<kbd><img src="https://user-images.githubusercontent.com/11259807/218260798-5ea9525b-24ce-4918-a7fc-6641d93ae1fc.png" width="100px"></kbd>

### 抽選申込
<kbd><img src="https://user-images.githubusercontent.com/11259807/218261381-83986a0e-2615-4b70-bfc0-e57e501488a0.png" width="100px"></kbd>
<kbd><img src="https://user-images.githubusercontent.com/11259807/218261668-cc9be846-cd16-4614-90d5-80403042b6fe.png" width="100px"></kbd>
<kbd><img src="https://user-images.githubusercontent.com/11259807/218261675-bd6bc4af-4937-41b9-8db5-7a48b279cbfe.png" width="100px"></kbd>
<kbd><img src="https://user-images.githubusercontent.com/11259807/218261395-1236d580-f0b9-45f7-be93-ca213840c8dd.png" width="100px"></kbd>

### メンバー
<kbd><img src="https://user-images.githubusercontent.com/11259807/218260803-9854f7b5-532f-4da5-8ad7-91e89b0f4b42.png" width="100px"></kbd>
<kbd><img src="https://user-images.githubusercontent.com/11259807/218260810-3521e697-bcf5-4a62-b973-59fdbd4bcb76.png" width="100px"></kbd>
<kbd><img src="https://user-images.githubusercontent.com/11259807/218260802-a23a52e6-0e26-4b22-9265-7c5c2d190915.png" width="100px"></kbd>

### 抽選結果
<kbd><img src="https://user-images.githubusercontent.com/11259807/218260799-d2128ad0-554a-4fd6-9730-0fbc9a947648.png" width="100px"></kbd>

## 構成
![システム構成](https://user-images.githubusercontent.com/11259807/218312767-863d4523-6861-4cc7-b6cb-e424cb4141bc.png)
* (A) ブラウザから送信された一括抽選申込のリクエストを [Django](https://www.djangoproject.com/) アプリが受け取る。
* (B) 申込数分のジョブをキュー（ [RQ](https://python-rq.org/) ）に追加する。
* (C) キューからジョブが取り出される。
* (D) ブラウザ自動操作（ [Selenium](https://www.selenium.dev/ja/) ）により東京都スポーツ施設サービスで抽選申込をする。（キューが空になるまで繰り返す）

## 工夫
* 東京都スポーツ施設サービスは特に抽選申込のためのAPI等は提供していないため、Seleniumによりブラウザを自動操作して抽選申込するようにした。
* ブラウザ自動操作では1つのジョブの実行に数十秒かかるため、RQを用いた非同期処理により画面レスポンスはすぐに返ってくるようにした。
