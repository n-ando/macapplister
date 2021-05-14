#!/usr/bin/env python3
# coding: utf-8
#
# macapplister: Create a list of installed apps on macOS
#
# Copyright (c) 2021, Noriaki Ando, All right reserved.
# 
#
# This tool create a list of applications which installed on the macOS.
# The list is output into a csv file.
#
VERSION="1.0.0"

rawtext = """
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

CSV_FNAME = 'applist.csv'
RAWLIST_TXT = 'rawlist.txt'
RAWLIST_GEN = False
EXCLUDE_LIST = [
    ['Vendor', 'Apple Inc.'],
    ['Vendor', 'Microsoft'],
    ["Location", "(Parallels)"],
    ['Application', 'Firefox'],
    ['Application', 'Chrome'],
    ['Application', 'Thunderbird'],
    ['Application', 'GlobalProtect'],
    ['Application', 'Acrobat']
]


import sys
import re
import time
import subprocess

def run_systemprofiler():
    proc = subprocess.Popen("system_profiler SPApplicationsDataType",
                        shell = True, text = True,
                        stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print("Retrieving installed application information.")
    rot = ['-', '\\', '|', '/']
    for c in range(150):
        print("Waiting", rot[c%4], flush = True, end = '\r')
        time.sleep(0.1)
    return proc

def parse_results(proc):
    app_name = ""
    appinfolist = []
    appinfo = {"Version": "Unknown", "Vendor": "Unknown"}
    if RAWLIST_GEN: rawf = open(file_name, 'a')

    #for line in hogetxt.split('\n'):
    for line in proc.stdout.readlines():
        if RAWLIST_GEN: rawf.write(line)
        # Application name
        appm = re.match(r'^    (\S[^:]+):(.*)$', line)
        if appm:
            # End if "AppName" and start new entry
            if "Application" in appinfo: 
                appinfolist.append(appinfo)
            appinfo = {"Version": "Unknown", "Vendor": "Unknown"}
            app_name = appm.group(1).strip()
            appinfo['Application'] = app_name
            continue
        # Application info
        tagm = re.match(r'^      (\S[^:]+):(.*)$', line)
        if tagm: 
            tag_name = tagm.group(1).strip()
            tag_value = tagm.group(2).strip()
            appinfo[tag_name] = tag_value
            # Retrieve vendor name
            if tag_name == "Signed by":
                # Signed vendors' app
                m0 = re.match(
                    r'\s*Developer ID Application: (\S[^\(]+) \([A-Z0-9]{10}\).*$',
                    tag_value)
                if m0:
                    appinfo['Vendor'] = m0.group(1).strip()
                # Apple's app 
                m1 = re.search("Apple Code Signing Certification Authority",
                                tag_value)
                if m1:
                    appinfo['Vendor'] = "Apple Inc."
            continue
    if RAWLIST_GEN: rawf.close()
    proc.wait()
    return appinfolist

def is_exclude(appinfo):
    for ex in EXCLUDE_LIST:
        if ex[1] in appinfo[ex[0]]: return True
    return False

def create_csv(appinfolist):
    import csv
    with open(CSV_FNAME, 'w', encoding="utf_8_sig") as csvf:
        # Excel's default encoding is SJIS. UFT8 csv needs BOM on Excel.
        writer = csv.writer(csvf) #, quoting=csv.QUOTE_ALL)
        writer.writerow([u"ソフトウェア名",
                         u"バージョン",
                         u"開発元"])
        for appinfo in appinfolist:
            if is_exclude(appinfo): continue
            appinfo["Version"] = "=\"" + appinfo["Version"] + "\""
            writer.writerow(
                    [appinfo["Application"], 
                     appinfo["Version"],
                     appinfo["Vendor"]])
    csvf.close()
    print("")
    print(CSV_FNAME, "created.")
    print("")

def version():
    version_msg="""
{_cmdname} {_version}, macOS X用アプリケーションリスト収集コマンド
    """.format(_cmdname=sys.argv[0], _version=VERSION).strip()
    print(version_msg)
    print("")

def help():
    help_msg="""
{_cmdname} {_version}, macOS X用アプリケーションリスト収集コマンド

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
                                       {_exclude}
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
  {_cmdname} -e 'Vendor:Apple Inc.' -e 'Vendor:Microsoft' \\
             -e 'Location:(Parallels)' ....

生データ例:
{_rawtext}
    """.format(_cmdname=sys.argv[0],
               _version=VERSION,
               _exclude='\n                                       '.
               join([str(i) for i in EXCLUDE_LIST]),
               _rawtext=rawtext).strip()
    print(help_msg)
    print("")

def parse_opt(arglist):
    import getopt
    global CSV_FNAME
    global EXCLUDE_LIST
    global RAWLIST_GEN
    try:
        opts, args = getopt.getopt(
            arglist,
            'Vhao:re:',
            ['version', 'help', 'all', 'outfile=', 'rawlist']
        )
    except getopt.GetoptError as err:
        print("オプション指定が間違っています。")
        print(str(err))
        help()
        sys.exit(-1)

    exclude_list = []
    for o, a in opts:
        if o in ("-V", "--version"):
            version()
            sys.exit(0)
        if o in ("-h", "--help"):
            help()
            sys.exit(0)
        if o in ("-o", "--outfile"):
            CSV_FNAME = a
        if o in ("-a", "--all"):
            EXCLUDE_LIST = []
            print("#########")
        if o in ("-r", "--rawlist"):
            RAWLIST_GEN = True
        if o in ("-e", "--exclude"):
            exclude_list.append(a.split(':'))
    if len(exclude_list) != 0:
        EXCLUDE_LIST = exclude_list

def main():
    parse_opt(sys.argv[1:])
    print("Excludeed key-values:\n       ", '\n        '.
               join([str(i) for i in EXCLUDE_LIST]))
    proc = run_systemprofiler()
    appinfo = parse_results(proc)
    create_csv(appinfo)


if __name__ == "__main__":
    main()