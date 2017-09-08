# biubiubiu
2D太空射击游戏

## OSX下运行方法
* 安装pygame依赖的库
> brew install hg sdl sdl_image sdl_ttf sdl_mixer portmidi
>
> (注：有大概率安装sdl_mixer后仍然无法使用mp3音效，原因是安装的版本与Python不兼容，需要上官网下载相应版本自行编译安装，请根据报错搜索解决）
* 安装pygame
> pip3 install --user hg+http://bitbucket.org/pygame/pygame
>
> (老版本Python有可能没有安装pip，请自行安装）
* python3.5 alien_invasion.py

## 操作方法
* 控制方向：ASDE<br>
* 射击：J <br>
* 退出游戏 ：ESC
* 每次游戏有3条生命，本机中心红点被击中或者与敌机相撞损失1条生命
* 每次复活有3秒无敌时间
* 弹匣容量为3枚，即一屏最多同时存在3枚本机子弹，子弹飞行速度会根据游戏时长增长而增长

## 运行截图
![run](https://github.com/shtiyu/biubiubiu/blob/master/images/example.gif?raw=true)
<br>
![run](https://github.com/shtiyu/biubiubiu/blob/master/images/example.png?raw=true)
