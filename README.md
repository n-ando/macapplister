# macapplister: macOS X用アプリケーションリスト収集コマンド

macOS X上にインストールされているアプリケーションリストを取得しCSVファイルに書き出します。
取得するリストに条件を付けてフィルタリングすることもできます。

## 動作条件
- macOS X
- python3.8

## 使い方

```shell
$ macapplister
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

## ヘルプ

```shell
使い方: {_cmdname} [オプション]... [URL]...

長いオプションで不可欠な引数は短いオプションでも不可欠です。

スタートアップ:
  -V,  --version                   バージョン情報を表示して終了する
  -h,  --help                      このヘルプを表示する

出力形式指定:
  -a,  --all                       全てのアプリケーションをリスト化する
  -o,  --outfile=file_name         出力csvファイル名
  -r,  --rawlist                   生データを "rawlist.txt"(ファイル名固定) に出力
                                   このデータから アプリ名, バージョン, ベンダ名
                                   を抽出してcsv形式で出力するので、-eオプションを
                                   指定する際に参考にしてください。
  -e,  --exclude=Key:Value         除外パターン指定、複数回指定可
                                   特定のエントリを含むアプリケーションを除外する指定
                                   指定時はデフォルト除外パターンはクリアされる
  　                               デフォルト除外パターン:
                                       ['Vendor', 'Apple Inc.']
                                       ['Vendor', 'Microsoft']
                                       ['Location', '(Parallels)']
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
  {_cmdname} -e "Signed by:Amazon"

  # Application に Acrobat が含まれるアプリを除外
  {_cmdname} -e "Application:Acrobat"

  # デフォルト設定と同等 (システムアプリと Parallels 共有アプリ等除外、上記参照)
  {_cmdname} -e 'Vendor:Apple Inc.' -e 'Vendor:Microsoft' \
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