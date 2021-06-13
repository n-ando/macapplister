# macapplister: macOS用アプリリスト収集コマンド

macOS上にインストールされているアプリケーションリストを取得しCSVファイルに書き出します。
取得するリストに条件を付けてフィルタリングすることもできます。

<!-- TOC -->

- [1. 動作条件](#1-動作条件)
- [2. ライセンス](#2-ライセンス)
- [3. インストール](#3-インストール)
- [4. オプション](#4-オプション)
- [5. 使い方](#5-使い方)
    - [5.1. デフォルト除外ルール](#51-デフォルト除外ルール)
    - [5.2. 除外ルール指定](#52-除外ルール指定)
        - [5.2.1. 利用可能な exclude "Key" の例](#521-利用可能な-exclude-key-の例)
    - [5.3. 実行例](#53-実行例)
- [6. ヘルプ](#6-ヘルプ)

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

## 4. オプション

以下のオプションが使用できます。

|&nbsp;&nbsp;&nbsp;&nbsp;ショート&nbsp;&nbsp;&nbsp;&nbsp;| ロング   | 意味 |
|:----:|:----:|:----| 
|  -V |  --version | バージョン情報を表示して終了する |
|  -h |  --help    | このヘルプを表示する |
|  -a |  --all     | 全てのアプリケーションをリスト化する |
|  -d |  --detail  | 
Applicationフォルダ内の複数アプリを展開する。<br/>
デフォルトでは、/Application/\<name\>, /Library/\<name\> の\<name\> とアプリケーション名が一致する場合には、/App or Lib/\<name\>/以下に複数のアプリケーションがあっても\<name\>のみリスト化される。 |
|  -o |  --outfile=file_name |     出力csvファイル名 |
|  -r |  --rawlist | 生データを "rawlist.txt"(ファイル名固定) に出力する。<br/>このデータから アプリ名, バージョン, ベンダ名を抽出してcsv形式で出力するので、-eオプションを指定する際に参考にしてください。 |
|  -e |  --exclude="Key:Value" | 除外パターン指定、複数回指定可能。特定のエントリを含むアプリケーションを除外する指定指定時はデフォルト除外パターンはクリアされる。|

## 5. 使い方
オプション無しでも動作します。デフォルトでは、Apple, Microsoft 社製のアプリ (Office, Teams等) や、Google Chrome や Mozilla/Thunderbird などの一般的なアプリケーション、さらに Parallels のアプリ共有機能で共有されたアプリケーション、GlobalProtect等は除外されて csv リスト化されます。除外ルールは、実行時に表示されます。

### 5.1. デフォルト除外ルール

- ベンダ名に Apple Inc. を含むもの
- ベンダ名に Microsoft を含むもの
- Location に /System を含むもの
  - macOSに標準で付属する多くのアプリ、ツール、コマンドがこのディレクトリ以下に存在する。(テキストエディット、カレンダー等)
- Location に (Parallels) を含むもの
  - Parallelsのアプリケーション共有が有効な場合、VM上のアプリケーションがMacから起動できるが、これがアプリケーションとして認識される

- Application 名が以下のもの
  - Firefox
  - Chrome
  - Thunderbird
  - GlobalProtect
  - Acrobat

### 5.2. 除外ルール指定

macOS上でアプリケーションとして認識されるものは多数あり、以上の除外ルールで除外したもの以外を更に除外したい場合は、-e オプションで <Key>:<Value> の形式で指定して、新たな除外ルールを指定してください。

以下の例では、アプリケーション名に Python を含むものを除外します。(Python は macOS に標準で含まれています。)

```shell
$ macapplister -e "<Key>:<Value>"

$ macapplister -e "Application:Python"
```

-e オプションは何度でも指定可能です。また、-eオプションを指定するとデフォルトの除外指定はクリアされます。使用できる Key は以下のとおりです。


#### 5.2.1. 利用可能な exclude "Key" の例

- Application                      アプリケーション名
- Vendor                           ベンダ名 (Signed byから抽出)
- Version                          バージョン番号
- Obtained from                    取得元
- Last Modified                    最終更新日
- Signed by                        ベンダ名を含む署名情報
- Location                         インストール場所
- Kind                             32-bit, 64-bit等の情報

実際、それぞれのアプリケーションがそれぞれの Key に対してどのような値を持っているかを調べるには、-r オプションで rawlist.txt を出力して出力されたテキストファイルを見て決めてください。

以下は、Parallels Desktop というアプリケーションの例です。最初の "Parallels Desktop" という名称は　Application という Key で指定する対象となります。また、Vendor というタグはありませんが、ベンダ情報は "Signed by" "Get Info String" といったタグの値からあるルールに基づいて自動で抽出されます。

また、App Store から取得されたものは、"Obtained from" に "App Store"が指定されていることが多いようです。

```
    Parallels Desktop:

      Version: 16.5.0
      Obtained from: Identified Developer
      Last Modified: 2021/04/02 18:41
      Kind: Intel
      Signed by: Developer ID Application: Parallels International GmbH (4C6364ACXT), Developer ID Certification 
Authority, Apple Root CA
      Location: /Applications/Parallels Desktop.app
      Get Info String: 16.5.0, Copyright 2005-2021 Parallels International GmbH
```

### 5.3. 実行例

実行には20秒から30秒程度の時間がかかります。プログラム実行中は Waiting の文字の後ろで '-' が回転します。

```console
$ macapplister
Excludeed key-values:
        ['Vendor', 'Apple Inc.']
        ['Vendor', 'Microsoft']
        ['Location', '/System'],
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

## 6. ヘルプ
詳しい使い方は、 '-h' オプションで表示されるヘルプをご覧ください。
'-e' または '--exclude=' オプションを指定することで、除外パターンを指定することができます。このオプションは任意に回数指定することができ、複数のパターンを指定することが可能です。

```console
使い方: macapplister [オプション]...

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
