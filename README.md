# SDUHealth
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

山东大学学生每日健康状况填报自动打卡。

**注意：本程序的适用范围为一个健康的有理智的学生，暂时只实现了离校生的打卡，未来也许会实现在校生的打卡，如果你身体不适，请勿使用本程序打卡，因本程序会自动上传健康的数据。**

## 环境&运行

本程序依赖于：

**[Python3](https://www.python.org)**

推荐使用 GitHub Actions 的运行方式，可以方便的实现每日自动打卡。

注意需要你使用本程序打卡前一天手动打过卡，且当天没有打过卡，之后每天就可以都只使用自动打卡了。

### Github Actions 运行

首先复制 configexample.yml 文件里面的所有内容，然后在本地进行编辑，根据文件的指示填入账号和密码，之后可以去 [yaml检测](https://www.bejson.com/validators/yaml_editor/) 检测一下文件的正确性，支持多账户，当然前提是你知道别人的密码。

之后 fork 本仓库到自己的 GitHub 账号，之后打开仓库的 Settings，在仓库设置界面在打开 Secrets 选项：

![Github Repo Secrets Settings](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-19%20at%2019.06.10.png)

之后新建一个 secret，Name 为 CONFIG，Value 就是你编辑的包含你的学号密码的 yaml 文件内容全部复制进去即可：

![New Github Repo Secret](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-19%20at%2019.08.02.png)

保存即可，之后转到仓库的 Actions 选项卡：

![Enable Github Actions workflow](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-19%20at%2019.09.06.png)

Enable 本仓库已经配置好的 GitHub Actions workflow，之后点击 checkin 打开配置选项：

![Enable checkin workflow](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-21%20at%2015.11.44.png)

 Enable workflow，之后得到下面的界面：

![Checkin workflow page](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-21%20at%2015.12.33.png)

你现在可以选择 Run workflow 手动触发运行，本仓库也配置了每天的自动运行，你可以打开 GitHub Actions 的运行结果提示，这样就可以简单的实现每天的打卡任务。

> ⚠️ 注意
>
> 最近我们发现 GitHub Actions workflow 有延时问题， 有可能您的实际运行时间与设置的不同。
>
> 又由于 GitHub 可能的设计问题，您有可能需要先手动运行一次打卡 workflow 才可以激活定时运行。

<details>
<summary>关于 repo_sync.yml 的使用说明</summary>

这个文件创建了一个定时自动同步源仓库内所有代码的 Github Actions workflow。

> ⚠️ 注意
>
> 该 workflow 执行后会自动覆盖原仓库内的所有代码，并更新为源仓库的代码，所有自定义的修改将不会得到保留（一般来说，也没什么需要自定义的，实在是需要自定义，可以手动执行该 workflow 之后，将其设置为 disable ）。

在 fork 了代码之后，首先需要去申请一个 GitHub Personal Access Token，该 Token 让此 workflow 拥有了更改指定仓库代码的权限。具体操作如下：

先选择账户 Settings

![Github account Settings](https://cdn.jsdelivr.net/gh/nekomiao123/pic/img/image-20210121121329851.png)

然后选择 Developer Settings

![Github Developer Settings](https://cdn.jsdelivr.net/gh/nekomiao123/pic/img/image-20210121121525838.png)

之后再选择 Personal access tokens 点击里面的 Generate new token

![Generate new token](https://cdn.jsdelivr.net/gh/nekomiao123/pic/img/image-20210121121640260.png)

之后先随便取个好记的名字，然后勾选前两项

![New personal access token](https://cdn.jsdelivr.net/gh/nekomiao123/pic/img/image-20210121121747207.png)

最后点击下面的 Generate token 即可，这样就能获得一串类似这样的字符，赶紧复制下来，它只会显示这一次

![Personal token info](https://cdn.jsdelivr.net/gh/nekomiao123/pic/img/image-20210121121953685.png)

然后去新建一个 secret（跟上面建立 secret 的流程一样）

Name 是 PAT

Value 是刚才你复制的这一串字符

</details>

到这里，该 Github Actions workflow 就可以使用了，可以实现每日自动打卡，如果你也开启了 repo_sync workflow 那么也将定时自动同步本仓库以保持代码更新。

### 本地运行

在本地安装好环境后，下载或者 clone 本仓库后，到项目文件夹下运行如下命令安装 Python 所需依赖：

```bash
pip install -r requirements.txt
```

安装好本程序所需依赖之后，需要把 configexample.yml 文件改名为 config.yml，然后根据文件里面的内容指示填入账号和密码。

之后运行如下命令运行 sduhealth.py 便会运行程序进行打卡。

```bash
python sduhealth.py
```

## 程序分析

想知道这个程序如何工作的，出现了 bug 想修改代码？欢迎阅读 [山东大学健康打卡系统分析](https://github.com/viewv/sduhealth/blob/main/doc/analysis.md) ！

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://tech.viewv.top"><img src="https://avatars3.githubusercontent.com/u/32566594?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Zhang XueNan</b></sub></a><br /><a href="https://github.com/viewv/sduhealth/commits?author=viewv" title="Code">💻</a> <a href="#ideas-viewv" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://nekokiku.cn/"><img src="https://avatars3.githubusercontent.com/u/34064940?v=4?s=100" width="100px;" alt=""/><br /><sub><b>menma</b></sub></a><br /><a href="https://github.com/viewv/sduhealth/commits?author=nekomiao123" title="Code">💻</a></td>
    <td align="center"><a href="https://www.macrohard.cn"><img src="https://avatars.githubusercontent.com/u/44798266?v=4?s=100" width="100px;" alt=""/><br /><sub><b>2U</b></sub></a><br /><a href="https://github.com/viewv/sduhealth/commits?author=Singularity0909" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/ryuujo1573"><img src="https://avatars.githubusercontent.com/u/16525512?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ryuujo Zhang</b></sub></a><br /><a href="https://github.com/viewv/sduhealth/commits?author=ryuujo1573" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
