#!/usr/bin/env python3
# coding: utf-8
#
# macapplister: Create a list of installed apps on macOS
#
# Copyright (c) 2021, Noriaki Ando, All right reserved.
#
# This tool create a list of applications which installed on the macOS.
# The list is output into a csv file.
#
import re
import sys
import subprocess
from subprocess import Popen, PIPE
proc = Popen("system_profiler SPApplicationsDataType",
                    shell = True, text = True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("waiting")
charcode="shift_jis"
count = 0
app_name = ""
appinfo = {}
hogetxt = """
    DaVinci Resolve Welcome:

      Version: 1.0.0
      Obtained from: Identified Developer
      Last Modified: 2020/12/17 2:23
      Signed by: Developer ID Application: Blackmagic Design Inc (9ZGFBWLSYP), Developer ID Certification Authority, Apple Root CA
      Location: /Library/Application Support/Blackmagic Design/DaVinci Resolve/DaVinci Resolve Welcome.app
      Kind: 64-bit
      """

#for line in hogetxt.split('\n'):
for line in proc.stdout.readlines():
    # Application name
    appm = re.match(r'^    (\S[^:]+):(.*)$', line)
    if appm:
        app_name = appm.group(1).strip()
        appinfo[app_name] = {}
        continue
    # Application info
    tagm = re.match(r'^      (\S[^:]+):(.*)$', line)
    if tagm: 
        tag_name = tagm.group(1).strip()
        tag_value = tagm.group(2).strip()
        appinfo[app_name][tag_name] = tag_value

        vendor_name = "Unknown"
        if tag_name == "Signed by":
            # Signed vendors' app
            m0 = re.match(
                r'\s*Developer ID Application: (\S[^\(]+) \([A-Z0-9]{10}\).*$',
                tag_value)
            if m0:
                appinfo[app_name]['Vendor'] = m0.group(1).strip()
            # Apple's app 
            m1 = re.search("Apple Code Signing Certification Authority",
                            tag_value)
            if m1:
                appinfo[app_name]['Vendor'] = "Apple Inc."
        continue
    count = count + 1
#proc.wait()

#print(appinfo)
import csv
with open('applist.csv', 'w') as csvf:
    writer = csv.writer(csvf)
    writer.writerow([u"ソフトウェア名",
                     u"バージョン",
                     u"開発元"])
    for key in appinfo.keys():
        if not "Version" in appinfo[key]: appinfo[key]["Version"] = "Unknown"
        if not "Vendor"  in appinfo[key]: appinfo[key]["Vendor"]  = "Unknown"
        if appinfo[key]["Vendor"] != "Apple Inc." and \
           appinfo[key]["Version"] != "Windows 10 Pro" and \
           appinfo[key]["Location"].find("(Parallels)") != 0:
            print(key, appinfo[key]["Version"], appinfo[key]["Vendor"])
            writer.writerow(
                [key, 
                 appinfo[key]["Version"],
                 appinfo[key]["Vendor"]])
csvf.close()

#for key in appinfo.keys():
#    if not "Version" in appinfo[key]: appinfo[key]["Version"] = "Unknown"
#    if not "Vendor"  in appinfo[key]: appinfo[key]["Vendor"]  = "Unknown"
#    if appinfo[key]["Vendor"] != "Apple Inc." and \
#       appinfo[key]["Version"] != "Windows 10 Pro" and \
#       appinfo[key]["Location"].find("(Parallels)") != 0:
#        print(key, ", ", appinfo[key]["Version"], ", ", appinfo[key]["Vendor"],
#    sep='') 