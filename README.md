# SDUHealth
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

山东大学健康自动打卡

**注意：本程序的适用范围为一个健康的有理智的学生，暂时只实现了离校生的打卡，未来也许会实现在校生的打卡，如果你身体不适，请勿使用本程序打卡，因本程序会自动上传健康的数据。**

## 环境&运行

本程序依赖于：

- nodejs
- python3

推荐使用 GitHub Action 的运行方式，可以方便的实现每日自动打卡。

### Github Action 运行

首先复制 configexample.yml 文件里面的所有内容，然后在本地进行编辑，根据文件的指示填入账号和密码，之后可以去 [yaml检测](https://www.bejson.com/validators/yaml_editor/) 检测一下文件的正确性，支持多账户，当然前提是你知道别人的密码。

之后 fork 本仓库到自己的 GitHub 账号，之后打开仓库的 Settings，在仓库设置界面在打开 Secrets 选项：

![Screen Shot 2021-01-19 at 19.06.10](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-19%20at%2019.06.10.png)

之后新建一个 secrets，Name 为 CONFIG，Value 就是之前的yaml文件全部复制进去即可：

![Screen Shot 2021-01-19 at 19.08.02](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-19%20at%2019.08.02.png)

保存即可，之后转到仓库的 Action 选项卡：

![Screen Shot 2021-01-19 at 19.09.06](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-19%20at%2019.09.06.png)

Enable 本仓库已经配置好的 GitHub Action workflow，之后点击 heal_sign 打开配置选项：![Screen Shot 2021-01-19 at 19.10.46](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-19%20at%2019.10.46.png)

 Enable workflow，之后得到下面的界面：

![Screen Shot 2021-01-19 at 19.11.30](https://cdn.jsdelivr.net/gh/viewv/Pico@master/uPic/Screen%20Shot%202021-01-19%20at%2019.11.30.png)

你现在可以选择 Run workflow 手动触发运行，本仓库也配置了每天的自动运行，你可以打开 GitHub Action 的运行结果提示，这样就可以简单的实现每天的打卡任务。 

### 本地运行

在本地安装好环境后，运行：

```bash
pip install -r requirements.txt
```

安装 python 所需依赖之后，需要把configexample.yml文件改名为config.yml，然后根据文件里面的内容指示填入账号和密码。

然后就可以运行程序进行打卡了

注意需要你使用本程序打卡前一天手动打过卡，且当天没有打过卡。

## 程序分析

想知道这个程序如何工作的，出现了 bug 想修改代码？欢迎阅读 [山东大学健康打卡系统分析](https://github.com/viewv/sduhealth/blob/main/analysis.md) ！


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://tech.viewv.top"><img src="https://avatars3.githubusercontent.com/u/32566594?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Zhang XueNan</b></sub></a><br /><a href="https://github.com/viewv/sduhealth/commits?author=viewv" title="Code">💻</a> <a href="#ideas-viewv" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!