#   (已停止维护)知乎助手1.8  ![forks](https://img.shields.io/github/forks/YaoZeyuan/ZhihuHelp.svg) ![stars](https://img.shields.io/github/stars/YaoZeyuan/ZhihuHelp.svg) ![issues](https://img.shields.io/github/issues/YaoZeyuan/ZhihuHelp.svg)

##  项目说明

**知乎助手** 由 [姚泽源](http://www.yaozeyuan.online/) 创作，采用 [MIT](http://opensource.org/licenses/MIT) 协议进行许可。

*   项目基于Python2.7构建，旨在用最简洁的方式帮助知友将知乎内容转为Epub电子书
*   目前的1.8.x系列是知乎助手发布计划中的过渡版本，在该版本中，我会尽可能多的为助手添加功能，为2.0版本的图形界面做准备

##  使用说明

0.  (Windows用户)安装[python2.7](http://yun.baidu.com/s/1M8Bpk)运行环境

1.  下载[知乎助手](www.yaozeyuan.online/zhihuhelp/redirect.html)并解压缩
    *   ![解压缩后](https://pic4.zhimg.com/b67c696f1a324df22b5cac58481d11a3_r.png)

2.  打开ReadList.txt，将待收集的网址填进去，完成后保存并关闭该文件
    *   ![ReadList](https://pic2.zhimg.com/c7c05c8dc01bf74129ce412609b378c5_r.png)
    *   ReadList中每一行生成一本电子书，用『$』隔开不同的网址，『#』作为注释，『#』后所有内容都会被忽略
    *   知乎助手支持收集的网址类型见后

3.  运行程序
    *   Windows用户
        *   双击zhihuHelp.py，按照提示运行程序即可
        *   ![](https://pic2.zhimg.com/3858bed15dec0843a652b7518d7ffa95_r.png)
    *   Linux/Mac用户
        *   打开终端，cd到解压出的知乎助手的目录下
        *   键入命令`python zhihuHelp.py`,按照提示运行程序即可
        *   ![Linux使用界面](https://pic1.zhimg.com/47d2fea858e68847760ec05f848abcb0_r.png)
        *   ![Mac使用界面](https://pic2.zhimg.com/5454f5bc83e27a230dd2802510713a8d_r.png)

##  知乎助手支持收集的网址类型

| 网址类型 | 描述 | 示例 |
| -------- | ---- | ---- |
| 问题 | 单个问题的网址，<br />程序运行时除了下载答案,<br />还会顺带把问题描述一起下下来 | `http://www.zhihu.com/question/22921426`，<br />`www.zhihu.com/question/27238186`，<br />`http://www.zhihu.com/question/22719537/`<br /> |
| 答案 | 知乎单个回答的网址,<br />也会下载问题描述 | `http://www.zhihu.com/question/21423568/answer/29751744`,<br /> `www.zhihu.com/question/20894671/answer/16526661`,<br /> `http://www.zhihu.com/question/22719537/answer/22733181`<br />|
| 话题 | 知乎话题的地址，<br />保存话题信息和话题精华中的答案 | `http://www.zhihu.com/topic/19552430`,<br /> `http://www.zhihu.com/topic/19551147/top-answers`,<br />`http://www.zhihu.com/topic/19554859` <br />|
| 指定知乎用户的全部回答 | 用户的个人主页 | `http://www.zhihu.com/people/yolfilm`,<br /> `http://www.zhihu.com/people/ying-ye-78/answers`,<br />`http://www.zhihu.com/people/bo-cai-28-7/logs` <br />|
| 公开收藏夹 | 知乎公开收藏夹的地址，<br />保存收藏夹信息和收藏夹内的答案 | `http://www.zhihu.com/collection/26489045`,<br /> `http://www.zhihu.com/collection/19633165`,<br /> `http://www.zhihu.com/collection/19641505`<br /> |
| 私人收藏夹 | 知乎私人收藏夹的地址，<br />保存收藏夹信息和收藏夹内的答案，<br />需要创建者用自己的ID登陆知乎助手 | `和正常收藏夹地址一样` |
| 专栏 | 专栏的网址 | `http://zhuanlan.zhihu.com/yolfilm`, <br />`http://zhuanlan.zhihu.com/epiccomposer`,<br /> `http://zhuanlan.zhihu.com/Wisdom`<br /> |
| 专栏文章 | 单篇专栏文章的网址 | `http://zhuanlan.zhihu.com/Wisdom/19636626`,<br /> `http://zhuanlan.zhihu.com/zerolib/19972661`, <br />`http://zhuanlan.zhihu.com/cogito/19968816` <br />|


##  补充:

1.  ReadList.txt文件中每一行对应一本电子书，一行中可以添加多个网址以输出到同一本电子书里，使用$符号分开即可
2.  网址后可添加#+注释以方便记忆，助手在分析网址时会自动忽略#后的内容
3.  助手目前还在快速迭代期，数据库、代码结构均不固定，所以暂时不能利用数据库起到永久保存知乎答案的功能，各位见谅则个:）

##  配置项说明：

0.  知乎助手的配置内容位于运行目录下的config.json中，各项配置功能如下

1.  account
    *   用户名，只能是知乎登陆邮箱
2.  password
    *   密码
3.  max_book_size_mb
    *   单卷电子书的最大大小(mb),超过该大小的话电子书会自动分卷
4.  picture_quality
    *   图片质量
    *   可选项
        *   0
            *   无图模式
        *   1
            *   标清模式，下载知乎网页中所展示的图片
        *   2
            *   原图模式，下载原图
5.  update_time
    *   更新日期
    *   修改本项会导致无法自动检测更新
    *   如果想跳过检测的话将本项设置为与[助手最新版本号](http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt)一致即可
6.  remember_account
    *   是否记住密码
    *   如为否，所有设置项都会被重置为默认值

##  依赖

仅要求python2.7环境，不依赖任何第三方组件

##  Todo List

- [x] 支持下载专栏文章；
- [x] 支持下载单篇专栏文章；
- [ ] 提供GUI界面；
- [x] 支持分卷输出电子书；
- [ ] 撰写接口文档；
- [ ] 支持自定义编辑电子书。
- [ ] 电子书增加封面，封面图片
- [ ] 进一步的，应当为不同种类的电子书增加不同种类的封面
- [ ] 按知乎圆桌收集答案
- [ ] 按自定义规则过滤收集到的答案(目前只能通过用户手工在代码中编写SQL语句来实现)
- [ ] 收集折叠区内的答案
- [ ] 支持收集特定日期范围内指定用户点过赞的所有答案和专栏文章；
- [ ] 按用户关注的问题收集答案
- [ ] 实现真正意义上的答案混排(例如可以指定答案出现的位置、顺序等)
- [ ] 实现对答案展现的控制(例如将指定答案的用户名换为另一位用户的用户名)
- [ ] 收集更多的用户/答案信息
- [ ] 按要求直接提取数据库数据
- [x] 改进电子书样式
- [ ] 增加输出为单张网页的功能
- [ ] 在捕获收藏夹信息时将创建者头像一并捕获进来

##License

[MIT](http://opensource.org/licenses/MIT)
