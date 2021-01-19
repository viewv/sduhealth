# SDUHealth

山东大学健康自动打卡

**注意：本程序的适用范围为一个健康的有理智的学生，暂时只实现了离校生的打卡，未来也许会实现在校生的打卡，如果你身体不适，请勿使用本程序打卡，因本程序会自动上传健康的数据。**

## 环境&运行

本程序依赖于：

- nodejs

- python3

### 本地运行

在本地安装好环境后，运行：

```bash
pip install -r requirements.txt
```

安装 python 所需依赖之后，需要把configexample.yml文件改名为config.yml，然后根据文件里面的内容指示填入账号和密码。

然后就可以运行程序进行打卡了

注意需要你使用本程序打卡前一天手动打过卡，且当天没有打过卡。

### Github Action 运行

首先复制configexample.yml文件里面的所有内容，然后在本地进行编辑，根据文件的指示填入账号和密码，之后可以去[yaml检测](https://www.bejson.com/validators/yaml_editor/)检测一下文件的正确性。

在github项目中Settings里面选择Secrets，然后点击那个New repository secret，在新建的secrets里面Name为CONFIG，Value就是把之前的yaml文件全部复制进去即可。

## 进度

✅ 登陆  
✅ 打卡  
✅ 注销
