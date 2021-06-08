# macapplister: macOS用アプリリスト収集コマンド

macOS上にインストールされているアプリケーションリストを取得しCSVファイルに書き出します。
取得するリストに条件を付けてフィルタリングすることもできます。

<!-- TOC -->

- [1. 動作条件](#1-動作条件)
- [2. ライセンス](#2-ライセンス)
- [3. インストール](#3-インストール)
- [4. 使い方](#4-使い方)
    - [4.1. デフォルト除外ルール](#41-デフォルト除外ルール)
    - [4.2. 実行例](#42-実行例)
- [5. ヘルプ](#5-ヘルプ)

<!-- /TOC -->

## 1. 動作条件
- macOS Catalina, Big Sur
- python3.9 (python3系なら動くと思います)

※ Big Surでも動作すると思いますが、Catalinaでしか確認していません。<br/>
※ もし動かないようならissueからお知らせください。

## 2. ライセンス
- MIT License

## 3. インストール
macapplister をパスの通ったところへインストールしてください。

```console
$ wget https://github.com/n-ando/macapplister/raw/main/macapplister
$ sudo install macapplister /usr/bin
Password:
$ macapplister -h <- ヘルプを見る
```

## 4. 使い方
オプション無しでも動作します。デフォルトでは、Apple, Microsoft 社製のアプリ (Office, Teams等) や、Google Chrome や Mozilla/Thunderbird などの一般的なアプリケーション、さらに Parallels のアプリ共有機能で共有されたアプリケーション、GlobalProtect等は除外されて csv リスト化されます。除外ルールは、実行時に表示されます。

### 4.1. デフォルト除外ルール

- ベンダ名に Apple Inc. を含むもの
- ベンダ名に Microsoft を含むもの
- Location に (Parallels) を含むもの
  - Parallelsのアプリケーション共有が有効な場合、VM上のアプリケーションがMacから起動できるが、これがアプリケーションとして認識される
- Application 名が以下のもの
  - Firefox
  - Chrome
  - Thunderbird
  - GlobalProtect
  - Acrobat

macOS上でアプリケーションとして認識されるものは多数あり、以上の除外ルールで除外したもの以外を更に除外したい場合は、-e オプションで新たな除外ルールを指定してください。
除外ルールは、-r オプションで rawlist.txt を出力し、除外したいアプリケーション名や含まれるキーワードを指定してください。指定方法の詳細は、以下のヘルプを参照してください。

### 4.2. 実行例

実行には20秒から30秒程度の時間がかかります。プログラム実行中は Waiting の文字の後ろで '-' が回転します。

```console
$ macapplister
Excludeed key-values:
        ['Vendor', 'Apple Inc.']
        ['Vendor', 'Microsoft']
        ['Location', '(Parallels)']
        ['Application', 'Firefox']
        ['Application', 'Chrome']
        ['Application', 'Thunderbird']
        ['Application', 'GlobalProtect']
        ['Application', 'Acrobat']
Retrieving installed application information.
Waiting \
applist.csv created.

$ ls
applist.csv
$

デフォルトでは、Apple, Microsoft 社製のアプリは除外
さらに、Google Chrome や Mozilla/Thunderbird なども除外される

$ macapplister -a
全てのアプリケーションをcsvファイルとして出力

$ macapplister -e "Application:Acrobat"
Acrobat という文字列を含むアプリケーションを除外

$ macapplister -e "Vendor:Google"
ベンダ名に Google という文字列を含むアプリケーションを除外
```

## 5. ヘルプ
詳しい使い方は、 '-h' オプションで表示されるヘルプをご覧ください。
'-e' または '--exclude=' オプションを指定することで、除外パターンを指定することができます。このオプションは任意に回数指定することができ、複数のパターンを指定することが可能です。

```console
使い方: macapplister [オプション]... [URL]...

長いオプションで不可欠な引数は短いオプションでも不可欠です。

スタートアップ:
  -V,  --version                   バージョン情報を表示して終了する
  -h,  --help                      このヘルプを表示する

出力形式指定:
  -a,  --all                       全てのアプリケーションをリスト化する
  -d,  --detail                    Applicationフォルダ内の複数アプリを展開する。
                                   デフォルトでは、/Application/<name>,
                                   /Library/<name> の <name> とアプリケーション名が
                                   一致する場合には、/App|Lib/<name>/以下に複数の
                                   アプリケーションがあっても<name>のみリスト化される。
  -o,  --outfile=file_name         出力csvファイル名
  -r,  --rawlist                   生データを "rawlist.txt"(ファイル名固定) に出力
                                   このデータから アプリ名, バージョン, ベンダ名
                                   を抽出してcsv形式で出力するので、-eオプションを
                                   指定する際に参考にしてください。
  -e,  --exclude="Key:Value"       除外パターン指定、複数回指定可
                                   特定のエントリを含むアプリケーションを除外する指定
                                   指定時はデフォルト除外パターンはクリアされる
  　                               デフォルト除外パターン:
                                       ['Vendor', 'Apple Inc.']
                                       ['Vendor', 'Microsoft']
                                       ['Location', '(Parallels)']
                                       ['Location', '/System']
                                       ['Application', 'Firefox']
                                       ['Application', 'Chrome']
                                       ['Application', 'Thunderbird']
                                       ['Application', 'GlobalProtect']
                                       ['Application', 'Acrobat']

利用可能な exclude "Key" の例:
  Application                      アプリケーション名
  Vendor                           ベンダ名 (Signed byから抽出)
  Version                          バージョン番号
  Obtained from                    取得元
  Last Modified                    最終更新日
  Signed by                        ベンダ名を含む署名情報
  Location                         インストール場所
  Kind                             32-bit, 64-bit等の情報

例:
  # Signed by に Amazon が含まれるアプリを除外
  macapplister -e "Signed by:Amazon"

  # Application に Acrobat が含まれるアプリを除外
  macapplister -e "Application:Acrobat"

  # デフォルト設定と同等 (システムアプリと Parallels 共有アプリ等除外、上記参照)
  macapplister -e 'Vendor:Apple Inc.' -e 'Vendor:Microsoft' \
             -e 'Location:(Parallels)' ....

生データ例:

#### Apple製 OS付属アプリケーション例 ####
    システム環境設定:

      Version: 14.0
      Obtained from: Apple
      Last Modified: 2021/04/29 10:02
      Signed by: Software Signing, Apple Code Signing Certification Authority, Apple Root CA
      Location: /System/Applications/System Preferences.app
      Kind: 64-bit

#### 通常のアプリケーション例 ####
    DaVinci Resolve Welcome:

      Version: 1.0.0
      Obtained from: Identified Developer
      Last Modified: 2020/12/17 2:23
      Signed by: Developer ID Application: Blackmagic Design Inc (9ZGFBWLSYP), Developer ID Certification Authority, Apple Root CA
      Location: /Library/Application Support/Blackmagic Design/DaVinci Resolve/DaVinci Resolve Welcome.app
      Kind: 64-bit

#### Paralles上のWindowsアプリケーション共有の例 ####
    Excel:

      Version: Windows 10 Pro
      Obtained from: Unknown
      Last Modified: 2021/04/22 16:15
      Location: /Users/myname/Applications (Parallels)/{7dd1123c-b1da-47a3-b088-934847232124} Applications.localized/Excel.app
      Kind: 64-bit
      Get Info String: 15.0, C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE
      """
```
