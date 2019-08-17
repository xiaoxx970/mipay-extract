#!/bin/bash

export TRAVIS_TAG=`python getlink.py ver`
# http://www.miui.com/download-330.html
# Rom URLs
declare -a urls=(`python getlink.py cn`)

EU_VER=$TRAVIS_TAG
# https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/
# EU Rom URLs
declare -a eu_urls=(`python getlink.py eu`)

command -v dirname >/dev/null 2>&1 && cd "$(dirname "$0")"
if [[ "$1" == "rom" ]]; then
    set -e
    base_dir=~
    [ -z "$2" ] && VER="$EU_VER" || VER=$2
    [ -d "$base_dir" ] || base_dir=.
    aria2c_opts="--check-certificate=false --file-allocation=trunc -s10 -x10 -j10 -c"
    aria2c="aria2c $aria2c_opts -d $base_dir/$VER"
    for i in "${eu_urls[@]}"
    do
        $aria2c ${i//$EU_VER/$VER}
    done
    base_url="https://github.com/xiaoxx970/mipay-extract/releases/download/$VER"
    $aria2c $base_url/eufix-Mi6-$VER.zip
    $aria2c $base_url/mipay-MI6-$VER.zip
    $aria2c $base_url/eufix-appvault-MI6-$VER.zip
    $aria2c $base_url/eufix-force-fbe-oreo.zip
    exit 0
fi
for i in "${urls[@]}"
do
   bash extract.sh --appvault "$i" || exit 1
done
[[ "$1" == "keep"  ]] || rm -rf miui-*/ miui_*.zip
for i in "${eu_urls[@]}"
do
   bash cleaner-fix.sh "$i" || exit 1
done
exit 0
