#!/bin/bash
#
# nvu validatorの起動を行い出力ファイルのFileringと編集を行う
# 大枠のFilterについてはvnuの機能を利用して、細かいFilterをここで行う。
# $1 概要HTMLファイルのフルパス
# Validatorの入力はファイルおよびURLで可能
# 課題点：URL指定の場合VNUでの取得と、wgetでの取得でずれが出る場合がある
#         機能を利用する形ではwgetで先に取って来る形式が有効
#
# Path info
pgm_path=/release/tools/validator/batch/bin
vnu_path=/release/tools/validator/engine/dist
filter_path=/release/tools/validator/filter
wk_path=/tmp/validator
tmp_no=$$           #  random number for not conflict
touch $wk_path/$tmp_no.log
echo "" > $wk_path/$tmp_no.log
mkdir -p $wk_path/$tmp_no
http_flg=false


# Run vnu validator
java -jar $vnu_path/vnu.jar --filterfile $filter_path/filterfile.txt --skip-non-html $1 2> $wk_path/$tmp_no.log

#!!BP>]$,Web%5!<%P!<$+%U%!%$%kD>$+$NH=CG
#  Web%5!<%P!<$N>l9g$Owget$G%3%T!<$r9T$&
if echo "$1" | grep -q http ; then
   http_flg=true
   html=`echo "$1" | awk -F'[/]' '{print $NF}'`
   http_path=$wk_path/$tmp_no/$html
   cd $wk_path/$tmp_no
   wget $1
#   echo "wget :  $1"
#   echo "file path : $http_path"
fi

# Validatorの出力をカスタムFilterする
#
# 基本Validator全般にわたる設定はvnu側のFilterで行う
# 個別条件での設定を行うもの（たとえばあるPathのみでは外すとか、youtubeとか）
#
ofile01=$wk_path/$tmp_no.ofile01
tfile01=$wk_path/$tmp_no.tfile01

echo -n > $ofile01
echo -n > $tfile01
# ディフォルト設定
def_filterfile=$filter_path/filter_parameter.txt
def_infile=$wk_path/$tmp_no.log
def_outfile=$wk_path/$tmp_no.out_logs

#if [ ! $1 = "" ]; then
#    def_infile=$1
#fi

#if [ ! $2 = "" ]; then
#    def_filterfile=$2
#fi

while IFS= read -r line01
do
    # Log上の対象箇所の行数を抜き出す編集処理（簡易なものがあれば要変更）
    # Colomn Low
    cl1=${line01#*:}
    cl2=${cl1#*:}
    cl3=${cl2%%:*}
    st1=${cl3%%.*}
    scc=${cl3#*.}
    cl4=${cl3#*-}
    ed1=${cl4%.*}
    sc2=${cl4#*.}
    sc1=${scc%-*}

#    echo "st= $st1 ed= $ed1 sc1= $sc1  Sc2= $sc2  "

    # Path & URL
    wk1=${line01#*:}
    wk2=${wk1%%:*}
    i=${#wk2}
    j=i-1
    wk3=${wk2:0:j}
#    echo "wk3 : $wk3"
    if $http_flg = true ; then
        htmlpath=$http_path
    else
        htmlpath=$wk3
    fi

#    echo "htmlPath : $htmlpath"
#    echo "st1 : $st1    ed1 : $ed1"


    cat $htmlpath | awk -v "stt=$st1" -v "edd=$ed1" 'NR==stt,NR==edd' > $tfile01
    # 出力された行を１行にまとめる

    str=""
    while IFS= read -r line02
    do
      str=$str$line02
    done < $tfile01

    # HTMLソースの連結時に該当箇所の頭の不要部分をとる
    # 後ろの部部分については別途検討（複数ライン処理との兼ね合いもあるので）
    if [ ${st1} = ${ed1} ] ; then
        if [ ${sc1} = ${sc2} ] ; then
            echo ${str:0}$line01 >> $ofile01
        else
            echo ${str:$sc1 - 1:$sc2 - $sc1 + 1}$line01 >> $ofile01
        fi
    else
        echo ${str:$sc1 - 1}$line01 >> $ofile01
    fi
done < $def_infile



#
# ここからは、Filterのロジック
# 基本２つの条件で分類を行う。HTML内<>の文字列とErrorメッセージ内の文字列
# Filterのパラメータの書き方は、一行に書いて、後者は省略可
# ErrorメッセージのFilter用正規化文字列、（AND HTML内のFilter用正規化文字列）
# 基本サーチ用のアプリ上で条件をバッファした方が高速処理可能、プロトでは
# マッチングの部分はShell上で実現
rm -f $def_outfile
# 入力編集後のログ読み込み
while IFS= read -r line01
do
   output_flg=true
    # Filterパラメータの読み込み
    while IFS= read -r line02
    do
      # OneパラメータかTwoパラメータかのチェック
      if  echo $line02 | grep -q AND  ; then
        para1=${line02%AND*}
        para2=${line02#*AND}
 #       echo $para1 "-" $para2
      else
        para1=${line02%AND*}
        para2=""
      fi
      #
      # Filerパラメータとの突合せ、パラメータが一つの場合は、
      # 残りは全一致ということで２個セットで評価
      # Filterマッチは基本出力しない
      if echo $line01 | grep -q -E "$para1" ; then
        if echo $line01 | grep -q -E "$para2" ; then
          output_flg=false
          break
        fi
      fi
    done < $def_filterfile
    if $output_flg = true ; then
      echo $line01 >> $def_outfile
#    else
#      echo "Filter Matched No output."
    fi
done < $ofile01

#echo "Finish !!!!"
# cat  $def_outfile
rm -r $wk_path/$tmp_no

python $pgm_path/edit.py $def_outfile

rm $wk_path/$tmp_no.*
