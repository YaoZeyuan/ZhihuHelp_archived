知乎助手1.7.4
====

![forks](https://img.shields.io/github/forks/YaoZeyuan/ZhihuHelp.svg)
![stars](https://img.shields.io/github/stars/YaoZeyuan/ZhihuHelp.svg)
![issues](https://img.shields.io/github/issues/YaoZeyuan/ZhihuHelp.svg)


<center>
  <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>
  <br />
  <span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">知乎助手</span>
  由 <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/YaoZeyuan/ZhihuHelp__Python" property="cc:attributionName" rel="cc:attributionURL">姚泽源</a> 创作，采用 <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享 署名-非商业性使用-相同方式共享 4.0 国际 许可协议</a>进行许可。
</center>


*   知乎助手构建于python标准库之上，旨在用最简洁的方式帮助知友将知乎内容转换为便于移动平台上通用的Epub电子书
*   目前的1.7.x系列是知乎助手发布计划中的过渡版本，在该版本中，我会尽可能多的为助手添加功能，为2.0版本的图形界面做准备

##安装
0.  首先需要下载安装python软件，[适用于微软32位系统的下载地址](https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi)、[适用于微软64位系统的下载地址](https://www.python.org/ftp/python/2.7.8/python-2.7.8.amd64.msi))，安装完成后即可正常运行*知乎助手*，不清楚是多少位系统的同学直接下载适用于32位系统的程序即可

1.  随后[下载](http://yaozeyuan.sinaapp.com/zhihuhelper/upgrade.php)知乎助手并解压缩
    *   说明:Windows用户使用老旧版本的winRAR解压会导致解压后的文件名为乱码，请使用最新版的[360压缩](http://yasuo.360.cn/)或者[好压](http://haozip.2345.com/download.htm)进行解压，Mac用户和Linux用户没有这方面的问题

##使用

目前知乎助手支持收集的网址类型有



| 网址类型 | 描述 | 示例 |
| -------- | ---- | ---- |
| 问题 | 单个问题的网址，<br />程序运行时除了下载答案,<br />还会顺带把问题描述一起下下来 | `http://www.zhihu.com/question/22921426`，<br />`www.zhihu.com/question/27238186`，<br />`http://www.zhihu.com/question/22719537/`<br /> |
| 答案 | 知乎单个回答的网址,<br />也会下载问题描述 | `http://www.zhihu.com/question/21423568/answer/29751744`,<br /> `www.zhihu.com/question/20894671/answer/16526661`,<br /> `http://www.zhihu.com/question/22719537/answer/22733181`<br />|
| 话题 | 知乎话题的地址，<br />保存话题信息和话题精华中的答案 | `http://www.zhihu.com/topic/19552430`,<br /> `http://www.zhihu.com/topic/19551147/top-answers`,<br />`http://www.zhihu.com/topic/19554859` <br />|
| 指定知乎用户的全部回答 | 用户的个人主页 | `http://www.zhihu.com/people/yolfilm`,<br /> `http://www.zhihu.com/people/ying-ye-78/answers`,<br />`http://www.zhihu.com/people/bo-cai-28-7/logs` <br />|
| 公开收藏夹 | 知乎公开收藏夹的地址，<br />保存收藏夹信息和收藏夹内的答案 | `http://www.zhihu.com/collection/26489045`,<br /> `http://www.zhihu.com/collection/19633165`,<br /> `http://www.zhihu.com/collection/19641505`<br /> |
| 私人收藏夹 | 知乎私人收藏夹的地址，<br />保存收藏夹信息和收藏夹内的答案，<br />需要创建者用自己的ID登陆知乎助手 | `长得和正常收藏夹一样`,<br />`主要是我的私人收藏夹放上了你们也打不开= =` |
| 专栏 | 专栏的网址 | `http://zhuanlan.zhihu.com/yolfilm`, <br />`http://zhuanlan.zhihu.com/epiccomposer`,<br /> `http://zhuanlan.zhihu.com/Wisdom`<br /> |
| 专栏文章 | 单篇专栏文章的网址 | `http://zhuanlan.zhihu.com/Wisdom/19636626`,<br /> `http://zhuanlan.zhihu.com/zerolib/19972661`, <br />`http://zhuanlan.zhihu.com/cogito/19968816` <br />|




1.  首先打开位于知乎助手文件夹内的ReadList.txt，将待下载的网址复制粘贴至ReadList中，然后保存并关闭
    *   ![ReadList](http://pic2.zhimg.com/95cbba73c17c5ea162746fd4c3ebf649_b.jpg)

2.  然后，Windows用户双击运行zhihuHelp.py，根据提示进行简单设定后开始自动进行抓取，生成的电子书在【助手生成的电子书】文件夹中，为Epub格式，可以在多看系列软件上流畅阅读
    *   Linux/Mac用户可以按如下方式运行zhihuHelper.py
        1.  首先，将知乎助手解压到桌面上
            *  ![unzip](http://pic1.zhimg.com/6379696bebd4d2977aaefd0d06a5e034_b.jpg)
        2.  打开终端，输入对应命令，切换到知乎助手的文件夹下


            ```Shell
            cd Desktop
            或者 cd 桌面 (根据操作系统中桌面文件夹的命名方式而定)
            -----------------------
            cd 知乎助手1.7.0.2   （切换到知乎助手所在的文件夹中）
            ```


            *   ![change_dir](http://pic3.zhimg.com/fe54216ccd4e796f24944cfa504bc1ba_b.jpg)
        3.  输入


            ```Shell
            python zhihuHelper.py
            ```


            运行知乎助手
            *   ![running](http://pic1.zhimg.com/7ea404bc3b9362053737660f86d0f588_r.jpg)

3.  补充说明:
    1.  ReadList.txt文件中每一行对应一本电子书，一行中可以添加多个网址，使用$符号分开即可
    2.  网址后可添加#+注释以方便记忆，助手在分析网址时会自动忽略#后的内容
    3.  助手目前还在快速迭代期，数据库、代码结构均不固定，所以暂时不能利用数据库起到永久保存知乎答案的功能，各位见谅则个:）
    4.  制作知乎2013年度回答300问的方法请见[www.zhihu.com/question/23845802/answer/26191403](http://www.zhihu.com/question/23845802/answer/26191403)

4.  配置项说明：
    0.  知乎助手的配置内容位于运行目录下的config.json中，各项配置功能如下
    1.  article_order_by
        *   文章排序指标
        *   可选值
            *   update_date
                *   更新日期
            *   agree_count
                *   赞同数
            *   char_count
                *   字数
    2.  article_order_by_desc
        *   是否按照降序对排序指标进行排列
        *   可选值
            *   true
                *   对于设定指标按降序排列（例如，按赞同数降序排列）
            *   false
                *   对于设定指标按升序排列
    3.  answer_order_by
        *   答案排序指标，为对问题内答案进行排序的依据
        *   可选值
            *   同article_order_by
    4.  answer_order_by_desc
        *   是否按照降序对排序指标进行排列
        *   同article_order_by_desc
    5.  question_order_by
        *   问题排序指标，为对电子书内问题进行排序的依据
        *   可选值
            *   answer_count
                *   问题内的答案数
            *   char_count
                *   问题内答案总字数
            *   agree_count
                *   问题内答案总赞同数
    6.  question_order_by_desc
        *   是否按照降序对排序指标进行排列
        *   同article_order_by_desc 
    7.  account
        *   用户名，只能是知乎登陆邮箱
    8.  password
        *   密码
    9.  max_answer
        *   每本电子书中最大可容纳的答案数，超过该值电子书将自动分割为多本
        *   备注
            *   一篇文章视为一个回答
    10. max_question
        *   每本电子书中最大可容纳的问题，超过该值电子书将自动分割为多本
        *   备注
            *   本设置项未启用
    11. max_article
        *   每本电子书中最大可容纳的文章数，超过该值电子书将自动分割为多本
        *   备注
            *   本设置项未启用     
    12. picture_quality
        *   图片质量
        *   可选项
            *   0
                *   无图模式
            *   1   
                *   标清模式，下载知乎网页中所展示的图片
            *   2
                *   原图模式，下载原图
    13. show_private_answer
        *   是否抓取『禁止转载』的答案
        *   可选项
            *   true
            *   false
    14. update_time
        *   更新日期
        *   修改本项会导致无法自动检测更新
        *   如果想跳过检测的话将本项设置为与[助手最新版本号](http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt)一致即可
    15. max_thread
        *   最大线程数
        *   不建议修改，线程开的过大在抓取时会引发429错误
    16. max_try
        *   网页打开失败时的最大尝试次数
        *   默认为反复打开5次
    17. debug
        *   debug模式开关
        *   可选值
            *   true
            *   false
    18. timeout_download_html
        *   下载网页超时时间
        *   默认为5s
    19. timeout_download_picture
        *   下载图片超时时间
        *   默认为10s
    20. remember_account
        *   是否记住密码
        *   如为否，所有设置项都会被重置为默认值

##依赖

仅要求python2.7环境，不依赖任何第三方组件

##Todo

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
- [ ] 改进电子书样式
- [x] 增加输出为单张网页的功能
- [ ] 在捕获收藏夹信息时将创建者头像一并捕获进来

##License

CC
