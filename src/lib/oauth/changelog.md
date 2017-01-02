# 更新历史

## 实验阶段

## 0.0.30

- [fix] 修复了一个尼玛嗨尼玛嗨的代码里不知道怎么多打了一个 `+` 的 Bug =。=
- [add] `Activity/ActType` 类增加了 `PUBLISH_LIVE` 型动态，表示用户举办 Live。

## 0.0.30.beta3

- [fix] 修复了当用户参与了某 Live 时，调用此 Live 的 `tickets` 属性会报错的 Bug。此 Bug 是由于知乎的查看票价接口不允许已参与的用户调用，目前此属性在这种情况下将给出 warning 并且不返回任何值。（对于 `for in` 操作是安全的）
- [add] 增加了 `Live.role` 属性表示用户于 Live 的关系。
- [add] 增加了 `Live.cospeakers` 属性表示 Live 的协作者，只有小部分多人主讲的 Live 这个属性才有值。

## 0.0.30.beta2

- [fix] 修复了在使用 `client.people()` 获取 `People` 对象后直接获取 `activities` 属性时会无法获取的 Bug。

### 0.0.30.beta1

- [add] 增加了 `Live` 类。
- [add] 增加了 `LiveBadge` Live 徽章类。
- [add] 增加了 `LiveTag` Live 标签类。
- [add] 增加了 `LiveTicket` Live 门票类。
- [add] `ZhihuClient` 增加了 `lives_ongoing` 和 `lives_ended` 两个属性，可以获取所有正在进行（或未开始）的 Live 和已经结束的 Live。并且提供 `lives` 快捷方法，将以上两个 Generator chain 起来。
- [add] `ZhihuClient` 增加了 `live()` 方法，通过 Live ID 获取 `Live` 对象。
- [add] `ZhihuClient.from_url()` 现在支持使用 Live 的 URL 创建 `Live` 对象。
- [add] `ZhihuClient` 增加了 `live_tags` 属性，用于获取所有 Live Tag。
- [add] `People` 类增加了 `lives` 属性，获取用户举办和参加的 Live。
- [add] `People` 类增加了 `liked_lives` 属性，获取用户感兴趣的 Live。
- [add] `Me.follow()` 方法现在可以对 `Live` 对象使用，也即对 Live 感兴趣（点小红心）。
- [change] `JOIN_LIVE` 型的动态现在返回 `type` 属性为 `ActType.JOIN_LIVE` 型的 `Activity` 对象，其 `target` 属性为 `Live` 对象。

### 0.0.29.post2

- [add] `Activity` 类增加了 `action_text` 属性，表示对动态的描述。比如 `xxx 赞同了问题`， `xxx 参加了 Live` 等
- [add/fix] `Activity/ActType` 类增加了 `VOTEUP_EBOOK` 型动态，暂时使用 `StreamingJSON` 做兼容，`EBook` 类预计在 0.0.32 或 33 版本才会增加。

### 0.0.29.post1

- [fix/add] 修复/增加了用户动态中的「参加 Live」，「创建分享」，「点赞分享」三种动作，暂时使用 `StreamingJSON` 做个兼容，后期会弄成和其他动作相同的形式并且增加 `Live` 和 `Pin` 类，预计在 0.0.30 版本吧。

### 0.0.29

- [add] 增加了之前忘记写的问题创建时间 `Question.created_time` 属性。

### 0.0.28

- [add] 增加了 `Collection.contents` 属性用于获取收藏夹里的答案和文章（具体用法请看文档）。
- [add] 增加了 `Collection.article` 属性用于获取收藏夹里的文章。
- [fix] 修复了 `Collection.answer` 因为新版知乎 API 取消接口而失效的问题。

### 0.0.27

- [fix] 修复 Python 3.4 和 2.7.x 及之前版本因为 dict unpacking 之后不能有 trailing comma 造成的语法错误。

### 0.0.26

- [add] 增加用户私信的获取接口：使用 `me.whispers` 获取对话列表，再用 `whisper.messages` 获取每条消息。
- [fix] 修复用户动态之前没有「收藏文章」类型而在获取时可能出错的情况
- [add] 用户动态增加了「收藏文章 (`COLLECT_ARTICLE`)」 类型

### 0.0.25

- [fix] 紧急修复 `shield()` 函数的实现错误。

（嗯我觉得这个版本号很好……因为我今天头痛，脑袋转了半天也没想清楚现在的实现到底对不对……不管了，反正是刚加的新功能，错就错吧，有人反馈我再改 =。= 

### 0.0.24

- [update] API 版本升级至 3.0.40，APP 版本升级至 4.11.0，更新 UA 和 UUID，跟上 Android 客户端的步伐
- [add] `People.activities` 现在能够获取「收藏答案」类型的动态，具体 `ActType` 和 `Activity.type` 取值请参见文档
- [fix] 修复获取某些用户时可能会 500 的 Bug
- [add] `shield` 现在可以防御 HTTP 请求达到最大重试次数的异常（`MaxRetryError`）
- [fix] `shield` 函数现在不能防御 `Activity` 生成器，因为它比较特殊
- [fix] 修改文档里的小 typo

注意，因为更新了 API 版本，而这个项目并没有完善的自动测试，所以某些情况下可能会造成 Bug，如果你遇到了，请暂时使用上一版本并与我联系，谢谢。

### 0.0.23

- [add] 增加 `People.over()` 和 `People.over_reason()` 函数判断用户是否被知乎反作弊系统屏蔽。
- [add] 增加 `shield()` 函数来辅助处理生成器获取数据时的异常。
- [per] 新增 `ZhihuException`， package 内所有自定义的异常均改为继承此异常，方便处理。
- [per] 新增 `ZhihuWarning`，package 内所有自定义的警告均继承此警告，方便处理。
- [del] 取消 404 错误码的自动重试。

### 0.0.22

- [fix] 修复 `ZhihuClient.people()` 方法的文档里的返回值类型错误。
- [add] 增加 `Activity.created_time` 属性表示用户动态的发生时间戳。
- [per] 完善 `Activity` 的文档。

### 0.0.21

- [fix] 修复 `Answer.save`，`Post.save()` 方法无法自定义多级目录，比如 `'data/' + answer.question.title` 的问题。
- [fix] 修复由于 Windows 不允许文件和文件夹名前后出现空格而导致的储存文件时可能出错的 Bug。

### 0.0.20

- [fix] 升级 OAuth API 到 3.0.29， APP Version 4.7.1，以支持机构帐号的基本资料获取。

### 0.0.19

- [fix] 修复了 Windows下文件名中含有换行时会出错的 Bug。
- [change] `Answer.save()` 和 `Article.save()` 方法的第三个参数现在不会重新设置非法字符列表，而是会更新它。

### 0.0.18

- [fix] 修复在使用 `BaseGenerator.add_params` 设置 `offset=100` 参数以函数跳过前面某些用户时，因为一直覆盖原始 URL 参数造成的只能循环获取 20 个数据的 Bug。
- [add] 提供了一个 `BaseGenerator.jump(n)` 函数作为 `add_params(offset=n)` 的简写。

### 0.0.17

- [add] `ZhihuClient.login_in_terminal` 增加了一个 `use_getpass` 参数用于控制在输入密码时是否使用密码模式（不回显输入），用于解决某些 Windows IDE 中无法在控制台中登录的问题。
- [change] Python 2 情况下，API requests 的 Header 从 unicode 转变成 ASCII，解决 Issue #20。

### 0.0.16

- [fix] 修复了在用户被知乎的新「悟空」系统屏蔽是，获取用户数据会发生 `MaxRetryError` 的 Bug，现在可以使用 `GetDataErrorException` 来捕获这一情况，并可用 `exception.reason` 输出原因，
- [del] 删除了 400 错误的自动重试机制。
- [fix] 修复了因 Python 2.7 版本，`getpass.win_getpass` 使用 `msvcrt.putch` 而不是 `msvcrt.putwch` 造成的使用 unicode 字符串作为输入密码时的提示字符串时出现的异常。
- [fix] 修改了一处 magic string。

### 0.0.15

- [fix] 修复了当文章不属于任何专栏时，使用 ``article.column`` 获取时会出错的 Bug。

### 0.0.14

- [fix] 修复了知乎现在的 API 添加了新验证字段 UUID 和 UA 而导致的无法使用的 Bug。
- [change] 关闭非安全请求的警告和输入密码时的警告。

### 0.0.13

- [fix] 修复了保存答案或文章时文件名的扩展名部分会多一个点的 bug。
- [fix] 修复了保存答案或文章时传递进文件名没有进行非法字符过滤引发的 bug。

### 0.0.12 - 2016.05.29

- [add] 莫名其妙的好像知乎 API 限制了获取用户粉丝的数量，只允许获取前 5020 个？稍微加了个 Warning。

### 0.0.11 - 2016.05.15

- [fix] 我真是傻 QwQ，自动重试机制写错了，现在应该是对了……

### 0.0.10 - 2016.05.15

- [fix] 修复一个由于登录时服务器返回的数据和大多数情况不一致造成的无法登录的 Bug（Issue #13）
- [add] 为 `StreamingJSON` 类增加了 `raw_data` 方法，用于获取内部数据的副本

### 0.0.9 - 2016.05.15

- [change] 修改了 `ZhihuClient.login` 方法中某些失败信息，使其能更明确的说明失败原因
- [add] 尝试性的为网络请求加入了自动重试机制
- [add] 完善文档，加入了手机登录的说明

### 0.0.8 - 2016.05.04

- [fix] 修复了 `Topic.best_answerers` 因返回的 JSON 与常规返回不符造成的 Bug

### 0.0.7 - 2016.04.28

- [fix] 修复了设置代理后因为关闭了 SSL 而造成的报 Warning 的问题
- [add] `Comment` 类增加了获取父评论作者的 `reply_to` 属性

### 0.0.6 - 2016.04.21

- [fix] 修复了 `Collection` 类的 `answer_count` 属性无法使用的 bug
- [change] 由于发现知乎 API 无法获取除自己以外用户关注的收藏夹，将 `following_collections` 由 `People` 类 移动至 `Me` 类中

### 0.0.5 - 2016.04.18

- [add] `Topic` 类增加了 `followers` 属性，可获取话题关注者
- [add] `Me` 类增加了 `vote` 方法，可以给答案/文章/评论点赞同/[反对]/清除赞和反对。
- [add] `Me` 类增加了 `thanks` 方法，可以给答案点感谢/取消感谢
- [add] `Me` 类增加了 `unhelpful` 方法，可以给答案没有帮助/取消没有帮助
- [add] `Me` 类增加了 `follow` 方法，可以关注/取消关注问题/话题/用户/专栏/收藏夹
- [add] `Me` 类增加了 `block` 方法，可以屏蔽/取消屏蔽用户
- [add] `Me` 类增加了 `collect` 方法，可以将答案加入自己的收藏夹
- [add] `Me` 类增加了 `message` 方法，可以向别的用户发私信
- [add] `Me` 类增加了 `comment` 方法，可以向答案/文章/问题/收藏夹发送评论，并且支持回复特定评论
- [add] `Me` 类增加了 `delete` 方法，可以删除自己的答案/评论/收藏夹/文章

### 0.0.4 - 2016.04.16

- [change] 所有自定义异常修改为继承 `Exception` 类，遵循 Python 文档的要求。[REF](https://docs.python.org/2/library/exceptions.html#exceptions.Exception)
- [add] `ZhihuClient` 增加 `set_proxy` 方法，可设置代理
- [add] 增加了 `People` 类的 `activities` 属性，可以获取用户动态
- [fix] 修复 Python 2 下因为 `__init__.py` 文件中的 `__all__` 变量是 unicode 而造成的 `from xxx import *` 报错的 bug
- [change] 生成器不再尝试使用类内缓存的数据，而是一定会访问 API（改了一下实现，对用户接口没啥影响）
- [add] 小小的增加了一点没啥用的测试

### 0.0.3 - 2016.04.09

- [add] 增加了 `ZhihuClient.from_url` 方法，传入合法的知乎网址，就能生成对应的对象
- [add] 给 `BaseGenerator` 增加了 `add_params` 和 `set_params`  方法
- [fix] 修复了 `BaseGenerator` 在 Python 2 下有问题的情况。
- [fix] 修复了当用户的 `locations`，`educations`，`business`，`employments` 等属性值不存在强行获取会出错的 bug
- [add] 写完了文档
- [change] 改变了好多内部类名和变量名，不过对外部接口没有影响

### 0.0.2 - 2016.04.07

- [fix] 修复错误的 BASE_HTML_HEADER 值。原值会导致 html 文件在 Firefox 中打开时，由于没有编码信息显示而不正确的问题。
- [add] 完善文档，用户文档基本写完。

### 0.0.1 - 2016.04.07

首次发布，提供基础功能。
