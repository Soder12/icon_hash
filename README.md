# icon_hash
一个计算fofa_icon_hash的python小工具
1、	获取icon_地址 例如：
http://ip:port/favicon.ico
https://ip:port/favicon.ico
 
2、	放到同目录下1.txt 或单个执行

处理单个图片
./icon_hash -i ./favicon.png

处理多个图片
./icon_hash -i ./favicon.png ./logo.png ./icon.jpg

处理单个URL
./icon_hash -u https://www.example.com

处理文件中多个 URL/图片
./icon_hash -r 1.txt

