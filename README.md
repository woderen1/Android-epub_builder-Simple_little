# 在安卓设备上(安卓10及其以下为主要目标设备。11及其以上如果出现错误，请先尝试虚拟机，再有问题再提问)生成epub的非常简单方法，接近无脑程度
有什么看不懂的直接看这个md文件的原始文件，或者直接在Issues里提问，不用不好意思
-
##对不起， iPhone和IPad不能用，因为严格的内部文件管理机制
-
##桌面端windows和macos和linux都能用，只需要把py脚本里的路径改成正确的实际路径就行，当成一个普通的python项目用就行。但是！不建议！不建议！！！安卓用户无故改变路径！虽然这在技术上是可行的甚至简单的，但一个小错误都会让项目失效！再小的风险也是风险！！！！！
-
###缺点:只支持简单文字，不支持文中插图和文中插入超链接（但是你把链接地址放到里头让别人手动复制粘贴是可以的）。
-
###可能雷点:py脚本有ai（Deepseek）内容
## 事前准备需要的软件有
- mt管理器[[下载链接](https://mt2.cn/download/)]
- termux[[github下载](https://github.com/termux/termux-app)或者在F-droid上下载]
## 准备好后，第一步
- 打开mt管理器
在`/storage/emulated/0/Download/eebook`创建`chapters`文件夹和`covers`文件夹
<details markdown='1'><summary>展开/收起</summary>
其实创建文件夹的路径位置是别的位置也行，就是需要改动一下你下载的`.py`脚本的里的路径，但是不建议，因为再小的风险也是风险。
而且这个项目是无脑生成，你都无脑了就别自己改了

</details>
`chapters`的文件创建方式
你需要下载的脚本是`epub_builder.py`。
创建文件方式:在`chapters`文件夹下直接创建文件名形如`00001.txt`的文件，注意如果超过10章，那文件名就是`00010.txt`的形式，超过百章，文件名就是`00100.txt`的形式。千章就以此类推。
注意，cover.jpg或者cover.png的图片的大小至少是800×600
<details markdown='1'><summary>展开/收起</summary>
最后的文件夹总体效果就是
----
    
    ```
    /storage/emulated/0/Download/eebook/
    ├── chapters/
    │   ├── 00001.txt
    │   ├── 00002.txt
    │   └── ... (more chapters)
    ├── covers/
    │   └── cover.jpg (or.png)
    └── epub_builder.py
    
    ```

</details>
- 现在是termux的时间了
1. 敲命令`pkg install python`
2. 敲命令`pip install ebooklib`
3. 敲命令`cd /storage/emulated/0/Download/eebook`（如果你改了文件路径，就把cd 后的文件路径改成你的实际路径）
4. 准备好了，最后一个命令
`python epub_builder.py`

小提示<details markdown='1'><summary>展开/收起</summary>
`epub_builder.py`里可以根据代码间注释来改变你的epub电子书的部分信息哦

</details>

# 想贡献的看这里
<details markdown='1'><summary>展开/收起</summary>
1. 翻译成别的语言
2. 把这个工具变成apk安装包
3. 或者把这个工具图形化
4. 让这个工具有更多功能
5. 帮作者解答问题
6. 直接Fork爆改这个项目
7. **点个星标**

</details>
