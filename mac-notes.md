# mac使用笔记
### 软件安装：
* web开发框架，zencart，yii，laravel，thinkphp，ruby on rail，django，flask，oop，mvc
框架规定了开发者写哪些代码／不写哪些代码，怎么写代码——这就是框架主要解决的问题。
* 前端javascript框架，jquey，node.js，anglar.js，bootstrap

* Stackoverflow、HackerNews、Reddit、Github，freebsd，lisp machine，sublime，vim，emacs，c/c++，python，lisp
* pelican flask tornado django fabric sqlalchemy
* 最大的优势在于续航和触摸板，真的可以在触摸板上通过不同的手势完成鼠标的一切，比如最大化，最小化，浏览器刷新，窗口切换等，完爆windows笔记本。（有时候需要借助一些小巧的三方软件）
有钱买HHKB，嫌贵考虑FILCO、海盗船之类，桌子大买Cherry非平胸版，再下来可以考虑Poker、Race之类，ikbc F 104也可以,楼主其实也不是alienware脑残粉，其他品牌的产品楼主也还是很喜欢的，某蛇razer的鼠标垫呀，某樱桃cherry的键盘啊。某钛客的鼠标啊那些


###### mac软件相关网址
[macupdate](http://www.macupdate.com)
[小众软件](http://www.appinn.com/)
[osxtoy](http://www.osxtoy.com/)
[miao](http://miao.hu/2012/02/26/osx-exp-share/)
[yansu](http://yansu.org/2014/08/03/general-mac-resources.html)
[ifunmac](http://www.ifunmac.com)
[lutaf](http://lutaf.com/)
[lucifr](http://lucifr.com/)
[yanzhiping](http://www.yangzhiping.com/tech/mac1.html)
[知乎-如何优雅使用mac](http://www.zhihu.com/question/20873070)

crossover(wine商业化版本)
字体：Courier(windows coding)，Consolas，Monaco(osx默认字体),ubuntu(默认字体)
安装homebrew(cakebrew):mac包管理
brew cask基于brew的mac封装机制
#### app store
+ 安装xcode（开发必备command line tools）

#### 安装homebrew,cask
	ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	brew install caskroom/cask/brew-cask
#### 安装python(安装可能出错),pip(python管理包)
	brew install -vd python
	easy_install pip
##### 安装常用软件
	brew install git iterm2 zsh vim mou
	brew install mysql
	brew cask install Sequel-Pro lanuchrocket
	pip install cheat
	git clone https://github.com/chrisallenlane/cheat.git&&cd cheat&python setup.py installl

	brew install macports
	port install Synergy remmina/ubuntu
	brew cask install the-unarchiver


* alfred(launchy,synapse)（效率）+ iterm2（gow,Terminator）+ zsh(bash)+ vim(/usr/share/vim)(sublime,emacs) + EasyFind(everything) w3m(文字浏览器)+ReadKit(foxmail) pocket evernote nosleep burn(BurnAware Free刻录) moom(窗口管理)+MplayerX+vlc视频
lanuchrocket memcached redis mongodb nginx mysql
cheatsheet(Hotkey Explorer) [快捷键表](http://www.cheatsheetapp.com/CheatSheet/)

+ moom boom popclip clipmenu shadowsocksx dash istat menus flux appcleaner little snitch reeder pocket evernote gemini weibox mamp
ruby gem，curl -L get.rvm.io | bash -s stable   更换源，gem sources --remove https://rubygems.org/，gem sources -a http://ruby.taobao.org/，
chrome 插件，http://chrome-extension-downloader.com Any.do ,Evernote web clipper , save to pocket,firebug, lastpass, proxy swiftsharp, rss subscribtion extension, rss feed reader, seo in china, undo closetab, vimium, youdao, mac不发热,

#### vim配置，打开vim，
	安装插件:BundleInstall，更新插件:BundleUpdate
	python代码补全Youcompeleteme
	brew install node npm
	npm install jshint -g
	git clone https://github.com/wklken/k-vim.git&&cd /k-vim&&sh -x install.sh


#### flash转html5 [htm5](http://zythum.sinaapp.com/youkuhtml5playerbookmark/)

#### zsh配置,字体Monaco for Powerline.otf
	cat /etc/shells
	chsh -s /bin/zsh
	wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
	export LC_ALL=en_US.UTF-8 export LANG=en_US.UTF-8

+ sublime配置：sublime text 2, vim
1. python代码补全插件: jedi, Youcompeleteme
2. python格式化代码: pep8 autoformat
3. 语法检测: flake8 lint
4. repr: sublimerepr
5. html/css/js prettify
http://www.douban.com/group/topic/28027863/
+ 快捷键表 https://gist.github.com/lucasfais/1207002

##### 访问远程共享
在Windows中， 我们可以`Run "\\192.168.0.4"`  来访问其他机器共享的目录
在Mac中，  先打开Finder,    command +K   打开共享目录 输入： `smb://192.168.0.4/share`

#### mac 下mac adress修改
	sudo ifconfig en0 ether `openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/.$//'`
