# 山东大学健康打卡系统分析

这个脚本主要使用 Request 来模拟一次打卡，与其他版本的区别大概是不是使用 selenium 来模拟浏览器，这样更加轻量而且方便服务器运行，下面来分析整个流程。

## 登陆

登陆部分是非常有意思的一部分，首先大家都注意到了，本程序为什么会需要 JS 的运行环境，这就和登陆有密切的关系了，整个山大系统的登陆是进行了如下几步。

首先是打开登陆网址，这时候服务器会给客户端一个网页，这个网页的 HTML 中，有两个非常关键的参数隐藏其中，LT 与 execution 这两个值，也就是登陆第一步，要 get 到这个网页，之后从中提取 LT 与 execution 这两个值。

![Screen Shot 2021-01-19 at 17.51.01](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-19%20at%2017.51.01.png)

之后便开始登陆流程，也就是用户名和密码，这样构成了登陆系统所需要的必要因素。

接下来我们来观察一个登陆样例 POST 包来看看是怎么登陆的：

```
POST /cas/login HTTP/1.1
Host: pass.sdu.edu.cn
Connection: close
Content-Length: 383
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: https://pass.sdu.edu.cn
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://pass.sdu.edu.cn/cas/login
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: JSESSIONID=CDDADFE350C42BDEC44B59F94D326EE6; Language=zh_CN

rsa=***&ul=***&pl=***&lt=***&execution=***&_eventId=submit
```

其中注意内容，这里因为隐私信息，用***替代，这里 ul 代表用户名长度，这里是学号长度，之后 pl 代表密码长度，之后 lt 便是上面获取到的 lt，execution 就是上面获取带的 execution，之后后面固定_eventId=submit。

那么这个所谓的 rsa 呢？难道是非对称加密，lt 是公钥，非也非也，这里是本系统最大的一个笑话。

我们来看登陆了部分的 js 代码：

![IMAGE 2021-01-19 17:58:45](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/IMAGE%202021-01-19%2017:58:45.jpg)

这里可以看到这个的 rsa 是由 u-用户名，p-密码，lt-LT，拼接起来，之后加三个密钥，对真的三个字符串密钥`1 2 3`  那么这个 `strEnc` 是啥函数呢，这里我们只需简单搜索发现了这个脚本：

![IMAGE 2021-01-19 18:00:56](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/IMAGE%202021-01-19%2018:00:56.jpg)

DES ？这和 RSA 完全没有关系，对，到这里我想大家就明白了，这个所谓的 RSA 这里是使用了 3DES 算法加密三个部分的拼接字符串，而三个密钥是简单的 `1 2 3`  有点可笑，不过我感觉还是安全的，因为毕竟学校的服务器开了 SSL，CA 证书也是正常的，只是这样折腾来的所谓加密，感觉还不如直接 Base 64，浪费服务器资源，还起名 RSA，挂羊头卖狗肉。

~~因为不知道，也不想分析，更不想写这个 3DES，所以这里选择了一个意外简单偷懒的方式，直接调用他的 js 加密，加上见代码中生成的随机 Cookies 这样我们就得到了登陆所需要的所有部分。~~

最新版本的代码使用了原生 Python 的 DES 加密，可以不依赖 js 运行环境了。

## 打卡

打卡部分非常繁琐，因为涉及到了数据的操作，从顶倒下的来介绍本部分的实现。

首先在本项目中，model.json 便是抓包后分析的一个标准的打卡后提交的 json 内容，所以思路便是通过服务器的请求获取到前一天的打卡数据，这也就是为什么运行需要你先打一天的卡，这样服务器就有了你的过去的数据，这样就可以实现获取到前一天的数据之后填充到新一天的数据中，之后只需要对 Model 进行简单的时间修改，之后 post 出去就可以实现打卡。

但是获取前一天的数据是比较复杂的，需要好几个步骤，这部分的实现可以在 `health_checkin` 中查看，首先需要进行 `gethealth` 之后 `checkService` 之后 `serveInfo` 之后 `getServeApply` 之后 `getContinueService` 之后 `getSignData` 这一整套流程下来，其中的最后一步 `getSignData` 的到了服务器返回的包，在这个包中，会有上次打卡的数据或者是暂存的数据，之后将这个数据，传到 model 里面进行处理，之后返回处理后的数据。

相当于 model 是支架，我们将获取到的前一天的数据附加到 model 上，之后增加修补，post 到服务器上就可以完成这个打卡流程。

