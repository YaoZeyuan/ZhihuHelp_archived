Game walkthrough - 游戏攻略
===========================

本来想的是写一篇博客的，但是果然还是不要太张扬，写在文档里算了。

..  warning:: 关于准备工作

    貌似知乎不知道怎么更改了 SSL 的加密方法，使用 Packet Capture 会影响到知乎 APP 的正常运作，现在推荐
    使用 Fiddler 代替 Packet Capture，并设置 SSL 解密方法为 `<client>,ssl3,tls1.2`。
    或者使用 Burp Suite 也可以。

Instruction  - 教学关
----------------------

你需要：

- 一台 Android 设备（我用的是 Nexus 7， 6.0.1，CM 13）
- 一台电脑，系统随意，有 Android Studio 最好，没有也行
- 支持 HTTPS 的抓包工具（我用的是 Android 上的 Packet Capture）
- APK 反编译工具（我用的是 jadx）

在 Android 设备上安装上知乎客户端，如果已经安装了的话就强行停止，
然后清除数据和缓存。

Start the game - 开始游戏
-------------------------

打开 Packet Capture，首次运行的话应该会让你安装证书（为了解密 SSL 流量）。
如果这一步遇到什么凭证问题，设置一下 Android 的锁屏密码什么的大概就可以，
不行的话就 Google 一下你的设备型号 + 问题描述，自己去解决吧。

证书安装完毕后点击 Packet Capture 的右上角绿三角开始抓包。

打开知乎客户端，按照正常的流程登录。

切回 Packet Capture，点开抓包列表，大概是这样一个情况。

..  image:: /images/explore-1.png

往下找，直到找到第一次知乎 APP 与 60 开头 IP 的有数据 SSL 通信，大概在最下面。

..  image:: /images/explore-2.png

..  _mission_one:

Mission 1 : Need Captcha? - 第一关：需要验证码么？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

点开最早的一次通信，然后点击右上角的 HTML 图标。忽略掉 recommendation，setting，
以及 topstory（估计是封面图） 等请求，找到第一个关键请求：captcha，如下：

..  image:: /images/explore-3.png

上图中重要的地方我都用红色框起来了。从上到下编号为 0-5 好了。

0 + 3 可以看出请求的地址是：https://api.zhihu.com/captcha

2 是表示当前 APP 和手机的一些信息的，是不是必须我没测试，但我是模拟了这几个
header 的。参见：:any:`ImZhihuAndroidClient`。

4 很重要，里面记录的是你的验证码会话。如果在后面登录的时候不带这些 Cookies 的话，
服务器会提示你验证码会话不正确之类的错误。当然辣，requests 的 Session 会自动处理
Cookies 的，不用太在意。

1 是最重要的验证信息。如果没有这个 header 项，
直接请求 API 的话服务器是会回给你错误信息的。

比如直接在浏览器里访问的话会是这样：

..  image:: /images/explore-4.png

正确的返回值应该是像上上图的框 5 那样，一个带有 ``show_captcha`` 键的 JSON 数据。
键值的意义是 「下次登录是否需要输入验证码」。

由于这里是 False，也为了简化登录流程的介绍，下面都以 ``show_captcha=False`` 为前提。

（如果你对验证码的处理方式很感兴趣，恭喜你，发现了 :ref:`隐藏关 <hidden_mission>`）

Mission 2 : Login - 第二关：登录
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

按照第一关的方式轻车熟路的找到第二个请求 sign_in（也许要返回到之前的通信列表界面，
点进另一个列表项）：

..  image:: /images/explore-5.png

好吧，很明显的两坨红色就是我的邮箱和密码了，不要管它们，继续看那些红框。

0：这是一个 POST 请求，地址是 https://api.zhihu.com/sign_in

1：和请求验证码的时候一致，其实没登录的情况下这个参数都一样。
由于这个验证在没登录的情况下都是存在的，所以我把它变成了一个类，
参见：:any:`BeforeLoginAuth`

2：这些就是登录参数了。

在讲参数之前我们来看看 Cookies，你会发现它和询问是否需要验证码之后服务器返回的
Cookies 一样。注意这里一定要匹配，如果不匹配则登录操作是不会通过的。
然前面也说过了 Session 会自动处理的，所以也不用太在意。

好了来说重头戏，登录的参数。我把它用 Python 字典的形式写在下面（调整了一下参数位置）：

..  code-block:: python

    {
        'username': 'example@emxample.com',
        'password': '123456',
        'client_id': '8d5..............',
        'grant_type': 'password',
        'source': 'com.zhihu.android',
        'timestamp': '1460165233',
        'signature': '8ad..............',
    }

前面两项不用多说，用户名和密码。我只试了邮箱，但是手机号也可以。

第三项叫做 ``client_id``，你可以和框 1 对比一下，就会发现其实他俩是一样的。
这其实就是 OAuth 里需要申请的，表示一个应用的 APPID 值，
如果你开发过微博的第三方应用，或者在你建的网站上使用了第三方登录功能，
应该不会对这个概念感到陌生。所有的（这个版本的） Android
知乎客户端的这个值都是一样的。

第四项是……恩，你大概当作授权类型把。``password`` 表示我们通过提供用户账户的密码
来获取用户令牌。其他的方式大概还有 OAuth 登录（就是像微博那样弹个小网页让你登录），
第三方登录（通过微博，QQ什么的），这里我们只讲密码型登录。

第五项叫做 source，表示登录请求的来源，可以看出值其实就是 APK 的包名。

第六项 timestamp，时间戳，表示当前时间。用来使每次登录请求的基础数据都不同，
方便 signature 签名加密用的。（在下一小节会详细介绍的）

最后一项是最重要的，请求的签名。如果你在知乎 APP 上多试几次，
就会发现这个值每次都不同。它是用来保证安全性的，因为你既不知道签名的计算方法，
又不知道加密的参数，所以你没法伪造登录请求。

下一小节介绍的就是签名加密算法的探寻过程。

Mission 3: Encrypted signature - 第三关：被加密的签名
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

为了破解这个签名，我费了挺大功夫的，大概一晚上加一早上吧……
这里就省略掉我试过的错误的方法（虽然这些试错的价值才是最大的），直击正确的途径。

首先我们用 jadx 拆掉 APK（记得打开反混淆），导入 Android Studio。（没有 Android Studio
的话也可以在 jadx 里直接查看）。导入之后大概如下图：

..  image:: /images/explore-6.png

然后打开 ``/com/zhihu/android/api/module/Authorisation.java``
（别问我是怎么知道的，我当然是一点一点找的啊……我又没有文章可以看）。

翻到 ``createBaseAuthorisation`` 这个方法，代码如下：

..  raw:: html

    pre {
      white-space: pre-wrap;
    }

..  code-block:: java
    :linenos:
    :emphasize-lines: 6-12

    private static Authorisation createBaseAuthorisation(Context context, GrantType grantType) {
        String timestamp = String.valueOf(System.currentTimeMillis() / 1000);
        Authorisation authorisation = new Authorisation();
        authorisation.clientId = "8d5227e0aaaa4797a763ac64e0c3b8";
        authorisation.source = SystemUtils.m18405c(context);
        authorisation.signature = b.a(
            grantType +
            "8d5227e0aaaa4797a763ac64e0c3b8" +
            authorisation.source +
            timestamp,
            "ecbefbf6b17e47ecb9035107866380"
        );
        authorisation.timestamp = timestamp;
        return authorisation;
    }

注意被标注的 6 到 12 行，这就是签名的加密算法。

我们可以看到，有一个叫做 ``b.a`` 的函数，接受两个参数，第一个是一堆字符串的拼接，
第二个是固定的字符串（其实就是 客户端的 SECRET）。

通过上一段对参数的解释，我们可以看到，除了 ``timestamp`` 之外，其他的都是固定的，
所以一第一个参数就是：

``“password8d5227e0aaaa4797a763ac64e0c3b8com.zhihu.android”``

后面再加上 ``timestamp`` 的值，

然后，最重要的来了，加密方法是什么。

我尝试了把第二个参数拼接到第一个参数的末尾和开头，然后再分别用 md5，sha1，先 md5
再 sha1，先 sha1 再 md5，以第二个参数为盐的 md5 和 sha1。反正都不对……

然后我就陷入了深深的迷茫中。洗把脸冷静了一会之后我想……知乎还算个比较跟潮流的公司，
去查查 Google 的 OAuth 文档说不定能有收获。（别问我当时怎么想的！
我也不知道为啥就觉的知乎应该会跟着 Google 的流程走……）

然后我找到了 Google OAuth 的签名文档（对 Google 的文档感兴趣的话点\ `这里 <https://developers.google.com/maps/documentation/static-maps/get-api-key#url->`_）

于是我就猜想是不是知乎也是用的 hmac.sha1 叻……然后就成功了，嗯，说起来就是这么简单……

签名代码参见：:any:`login_signature`。

Last hint: Get token - 最后一击：获取令牌
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在了解了签名加密算法之后，剩下的工作就很简单了，模拟成客户端把登录请求发过去就行。

以下是客户端返回的结果。

..  image:: /images/explore-7.png

由于返回结果涉及到账户安全信息，所以马赛克比较多，凑合着看哈。

最重要的是那个 ``access_token`` 项，登录后的每个请求都需要这个令牌进行验证。

阿，对了，那个 cookies 里的东西貌似并不是很重要，我没有手动添加进 Session，
所有的功能也能成功完成。

有关令牌的保存和使用，请看 :any:`ZhihuToken` 类 和 :any:`ZhihuOAuth` 类。

下面是一次登录传成功后的一次 API 请求头：

..  image:: /images/explore-8.png


注意红框部分的 ``Bearer``，这是 OAuth2 的一种 token type 方式，
如果你想了解它的定义，可以看看 `RFC 6750 <https://tools.ietf.org/html/rfc6750>`_。

后面那被我打了马赛克的地方就是上上图中的 ``access_token`` 值。
你用有效的 ``access_token`` 进行验证，服务器才会允许你获取数据。

服务器的回复我就不贴了。

至此，知乎 APP 的 OAuth 过程就解析完毕辣！下面的附加关卡是给兴趣浓厚的同学们准备的。

..  _hidden_mission:

Hidden mission: Process captcha - 隐藏关卡：验证码处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`mission_one` 里说到了验证码的问题。

知乎 OAuth 的验证码策略是这样的。

1. 每次登录前必须使用 ``GET``  方式调用 ``captcha`` API 获取自己此次登录需不需要验证码。
   知乎的服务器根据你最近的登录频繁程度，上次登录结果等来决定是否需要你输入验证码。
   不管最后结果是需要还是不需要，服务器会在数据库里存你的验证码 Session 然后用
   ``Set-Cookies HTTP header`` 的方式给你 ``Session ID``。
2. 如果需要验证码则继续往下执行，不需要则转 6。
3. 请求使用 ``PUT`` 方式调用 ``captcha`` API，（记得带上上一步发给你的 Cookies）
   获取到的是 base64 编码的一张 gif 图片。
4. 使用 ``POST`` 方式调用 ``captcha`` API，``data`` 设置为 ``{'captcha'='abcd'}``
   （当然也得记得带上 Cookies）
5. 如果验证码输入正确，服务器会在你的验证码 Session 里写上验证成功。如果输入失败
   你就得重新转到步骤 3，成功的话继续往下。
6. 用正常方式使用 ``sign_up`` API 登录即可（带上 Cookies）。

知乎所有关于验证码的操作都使用同一个 API，用不同的 HTTP Verb 把功能区分开，我觉得挺有意思的。

我代码里有关登录和注册码相关逻辑处理，请看下面几个函数：

- :any:`ZhihuClient.login`
- :any:`ZhihuClient.need_captcha`
- :any:`ZhihuClient.get_captcha`
- :any:`ZhihuClient.login_in_terminal`

Finale - 大结局
---------------

好啦，游戏攻略就写到这里……快去自己玩玩呗？

（完）

2016.04.09 初稿。
2016.08.30 修改一些格式和用词小问题。
