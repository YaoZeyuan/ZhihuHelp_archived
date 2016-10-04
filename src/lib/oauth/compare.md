# 获取我的所有答案，截至测试时有 258 个答案

zhihu-py3 代码：

```python
import timeit

from zhihu import ZhihuClient


def be_tested():
    client = ZhihuClient('test.json')

    me = client.author('https://www.zhihu.com/people/7sdream')

    for answer in me.answers:
        print(answer.question.title, answer.upvote_num)

print(timeit.timeit('be_tested()', 'from __main__ import be_tested', number=1))
```

zhihu-oauth 代码：

```python
import timeit

from zhihu_oauth import ZhihuClient


def be_tested():
    client = ZhihuClient()

    client.load_token('token.pkl')

    me = client.people('7sdream')

    for answer in me.answers:
        print(answer.question.title, answer.voteup_count)

print(timeit.timeit('be_tested()', 'from __main__ import be_tested', number=1))
```

用时对比：

zhihu-py3: 14.69939255801728

zhihu-oauth: 4.271191456995439

统计图：

![chart](http://ww4.sinaimg.cn/large/88e401f0jw1f2l6yweho1j20hw06xdg4.jpg)

图表使用 live.amcharts.com 创建
