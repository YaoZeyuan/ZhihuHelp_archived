#!/bin/bash

grepCheck='grep -Rn .|grep -v .svn|grep -v .js|grep -v Co,LTD|grep -v .css'

echo 检测『\(』后多余的空格
eval "$grepCheck|grep \([\ ]"
echo ===============

echo 检测『，』后直接跟进的字符
eval "$grepCheck|grep -v \'[a-zA-Z,]*,[,a-zA-Z]*\'|grep -v \"[a-zA-Z,]*,[,a-zA-Z]*\"|grep ,\[^\ \]"
echo ===============

echo 检测『，』前多加的空格
eval "$grepCheck|grep -v \'[a-zA-Z,]*,[,a-zA-Z]*\'|grep -v \"[a-zA-Z,]*,[,a-zA-Z]*\"|grep \[^\ \],"
echo ===============

echo 检测网页标签间的多余空格『\> \<』
eval "$grepCheck|grep -v \</i\>\ \<|grep \>\ \<"
echo ===============

echo 检测endif，endforach里遗漏掉的分号
eval "$grepCheck|grep endif|grep -v endif;"
eval "$grepCheck|grep endforeach|grep -v endforeach;"
eval "$grepCheck|grep endfor|grep -v endfor;"
echo ===============

echo 检测操作符前遗漏的空格
echo =\>
eval "$grepCheck|grep =\>|grep -v \[\ \]=\>\[\ \]"
echo ==
eval "$grepCheck|grep ==|grep -v ===|grep -v !==|grep -v \[\ \]==\[\ \]"
echo +=
eval "$grepCheck|grep \[+\]=|grep -v \[\ \]\[+\]=\[\ \]"
echo -=
eval "$grepCheck|grep \[-\]=|grep -v \[\ \]\[-\]=\[\ \]"
echo !=
eval "$grepCheck|grep !=|grep -v !==|grep -v \[\ \]!=\[\ \]"
echo !==
eval "$grepCheck|grep !==|grep -v \[\ \]!==\[\ \]"
echo ===============

echo 检测遗留的a函数
eval "$grepCheck|grep [^a-zA-Z:]a\("
echo ===============
#echo 检测等号左右的对齐，该功能需肉眼完成，找到不对齐处之后使用grep查找
#grep \ -Rn ./|grep -v .svn|egrep [a-zA-Z]\ +=\ +[a-zA-Z]
#echo ===============
