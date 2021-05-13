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
testtxt = """
    DaVinci Resolve Welcome:

      Version: 1.0.0
      Obtained from: Identified Developer
      Last Modified: 2020/12/17 2:23
      Signed by: Developer ID Application: Blackmagic Design Inc (9ZGFBWLSYP), Developer ID Certification Authority, Apple Root CA
      Location: /Library/Application Support/Blackmagic Design/DaVinci Resolve/DaVinci Resolve Welcome.app
      Kind: 64-bit

    リモート デスクトップ接続:

      Version: Windows 10 Pro
      Obtained from: Unknown
      Last Modified: 2021/01/17 15:03
      Location: /Users/n-ando/Applications (Parallels)/{7dd1123c-b1da-47a3-b088-934847232124} Applications.localized/リモート デスクトップ接続.app
      Kind: 64-bit
      Get Info String: 15.0, C:\Windows\system32\mstsc.exe
      """

csv_fname = 'applist.csv'

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

    #for line in hogetxt.split('\n'):
    for line in proc.stdout.readlines():
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
    proc.wait()
    return appinfolist

def create_csv(appinfolist):
    import csv
    with open(csv_fname, 'w', encoding="utf_8_sig") as csvf:
        # Excel's default encoding is SJIS. UFT8 csv needs BOM on Excel.
        writer = csv.writer(csvf) #, quoting=csv.QUOTE_ALL)
        writer.writerow([u"ソフトウェア名",
                         u"バージョン",
                         u"開発元"])
        for appinfo in appinfolist:
            if appinfo["Vendor"] != "Apple Inc." and \
               appinfo["Version"] != "Windows 10 Pro" and \
               appinfo["Location"].find("(Parallels)") != 0:
                appinfo["Version"] = "=\"" + appinfo["Version"] + "\""
                writer.writerow(
                    [appinfo["Application"], 
                     appinfo["Version"],
                     appinfo["Vendor"]])
    csvf.close()
    print("")
    print(csv_fname, "created.")
    print("")


import getopt

proc = run_systemprofiler()
appinfo = parse_results(proc)
create_csv(appinfo)
