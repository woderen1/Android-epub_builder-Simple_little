## 📜 许可证  
[](https://opensource.org/licenses/MPL-2.0)  
本项目采用 **Mozilla Public License 2.0**，意味着您：
- ✅ 可自由修改、分发、用于商业衍生品（如图形化APP）
- ❌ **不得直接转售源代码**(但是直接打包成app可以)
- 📝 修改代码文件需保留原始版权声明

# 在安卓设备上(安卓10及其以下为主要目标设备。11及其以上如果出现错误，请先尝试虚拟机，再有问题再提问)生成epub的非常简单方法，接近无脑程度
有什么看不懂的直接看这个md文件的原始文件，或者直接在Issues里提问，不用不好意思
-
要是安卓端有简单工具我愿意折磨自己做这个？云端转换？我对这种涉及上传存储文件的玩意总感觉怀疑
灵感:三个字母开头，然后是ku8。呜呜呜
-
## 对不起， iPhone和IPad不能用，因为严格的内部文件管理机制
-
## 桌面端windows和macos和linux都能用，只需要把py脚本里的路径改成正确的实际路径就行，当成一个普通的python项目用就行。但是！不建议！不建议！！！安卓用户无故改变路径！虽然这在技术上是可行的甚至简单的，但一个小错误都会让项目失效！再小的风险也是风险！！！！！
-
除了安卓以外还支持windows macos Linux
-
### 缺点:只支持简单文字和支持文中插图(两个脚本)，不支持文中插入超链接（但是你把链接地址放到里头让别人手动复制粘贴是可以的）。
-
### 可能雷点:py脚本有ai（Deepseek）内容
## 事前准备需要的软件有
- mt管理器[[下载链接](https://mt2.cn/download/)]
- termux[[github下载](https://github.com/termux/termux-app)或者在F-droid上下载]

### 纯文字epub制作方法

- 打开mt管理器
在`/storage/emulated/0/Download/eebook`创建`chapters`文件夹和`covers`文件夹
<details markdown='1'><summary>展开/收起</summary>

其实创建文件夹的路径位置是别的位置也行，就是需要改动一下你下载的 `.py` 脚本的里的路径，但是不建议，因为再小的风险也是风险。
而且这个项目是无脑生成，你都无脑了就别自己改了

</details>

你需要下载的脚本是`epub_builder.py`。
创建文件方式:在`chapters`文件夹下直接创建文件名形如`00001.txt`的文件，注意如果超过10章，那文件名就是`00010.txt`的形式，超过百章，文件名就是`00100.txt`的形式。千章就以此类推。


**数字后可加自然语言后缀哦**

__自然语言指中文、英文、日文、俄文等人类说的语言__


注意，cover.jpg或者cover.png的图片的大小至少是800×600
<details markdown='1'><summary>展开/收起</summary>
最后的文件夹总体效果就是

----


    ```
    /storage/emulated/0/Download/eebook/
    ├── chapters/
    │   ├── 00001.txt
    │   ├── 00002.txt
    │   └── ... (more txt)
    ├── covers/
    │   └── cover.jpg (or.png)
    └── epub_builder.py

    ```

</details>

----

- 现在是termux的时间了

<details markdown='1'><summary>展开/收起</summary>

换源命令: `termux-change-repo`

</details>

1. 敲命令 `termux-setup-storage`

2. 敲命令 `pkg install python`

3. 敲命令 `pkg install libxml2`

4. 敲命令 `pkg install libxslt`

5. 敲命令 `pip install ebooklib`

<details markdown='1'><summary>展开/收起</summary>

镜像源 `pip install -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com ebooklib
`
别的(按照这个格式):

清华源 `https://pypi.tuna.tsinghua.edu.cn/simple/`

阿里云 `https://mirrors.aliyun.com/pypi/simple/`

</details>

6. 敲命令 `cd /storage/emulated/0/Download/eebook`（如果你改了文件路径，就把cd 后的文件路径改成你的实际路径）

7. 准备好了，最后一个命令 `python epub_builder.py`

</details>

### 带插图功能使用方法
-
需要下载的脚本是 `v0.02epub_builderIMG.py`
----
在`/storage/emulated/0/Download/Exzbook/`下创建`OEBPS`文件夹。在`OEBPS`文件夹里创建txt文件(与原来规则不变)和`images`文件夹(与txt文件同级)
`images`文件夹内存放封面图片(与原来规则一样)和文中插图。**只支持jpg和png** 敏感大小写
最后效果大概是
<details markdown='1'><summary>展开/收起</summary>

    /storage/emulated/0/Download/Exzbook/
    ├─v0.02epub_builderIMG.py
    └─ OEBPS/
                ├── images/
                ║          ├cover.jpg(或cover.png)
                ║          └其他插图.jpg/png
                ├── 00001.txt
                ├── 00002.txt
                ├── 00003.txt
                └── (more txt)


</details>

-
引用方法，在txt文本中，单独一行，在那一行中使用 `[图片名.图格式]` 的方式来引用。
-
⚠️只用写图片名，脚本会帮你的，中文命名禁止❗
-
⚠️保留中括号
-
❗假如你的图片文件名是`filename.jpg`，那么引用时就单开一行写`[filename.jpg]`
脚本会帮助你的


Termux的时间


需要安装python

安装python `pkg install python`


打开目录的命令是 `cd /storage/emulated/0/Download/Ezbook/`

运行使用脚本文件 `python v0.02epub_builderIMG.py`

----
小提示<details markdown='1'><summary>展开/收起</summary>
两个`.py`里都可以根据代码间注释来改变你的epub电子书的部分信息哦
-

作者很难会选择更新的功能:多级目录

原因:很简单，作者用不上，作者要不选择很多epub文件打包成zip，要不选择直接目录全部平铺。这两种方法的人类可读性都可以保证

🛑 为什么不追求自动化的嵌套目录？
因为代价远大于收益，且替代方案更优！

🚫 技术不可行性： 原始 TXT/JPG 文件名本身缺乏深层结构信息。无法让脚本可靠地“猜测”出多级章节嵌套（是技术限制，更是信息论限制）。

🚫 实现复杂度爆炸： 为了实现不稳定且可能错误的“自动嵌套”，需要引入复杂的配置文件、路径解析规则、嵌套映射逻辑。这必然导致脚本失败率陡升、运行效率下降、维护难度激增，且最终效果往往不可预测（“玄学”）。我们坚决避免！

🚫 用户体验陷阱： 要求用户写配置文件来定义层级结构， 学习曲线陡峭、操作繁琐、极易出错。配置文件的调试成本远高于在图形界面（如 Sigil）中手动操作。如果用户有精力写配置，那他直接用 Sigil 会更方便、更直观、更可控！


-
# 想贡献的看这里
<details markdown='1'><summary>展开/收起</summary>

1. 翻译成别的语言
-
2. 把这个工具变成apk安装包
-
3. 或者把这个工具图形化
-
4. 让这个工具有更多功能
-
5. 帮作者解答问题
-
6. 直接Fork爆改这个项目
-
7. **点个星标**

</details>

-

## 仅限个人学习使用，只转化个人笔记或者不受版权保护的文本。不要转化受版权保护的内容！！
本开发者不为用户的个人行为承担任何责任！！！！！