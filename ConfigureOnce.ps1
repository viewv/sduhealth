function Initialize {
    Get-Content -Path 'configexample.yml' -Encoding UTF8 | Out-String | Set-Variable 'config'
    Write-Host '[Info] ' -ForegroundColor Cyan -NoNewline
    Write-Host '请输入需要自动打卡的信息化门户账号:'
    Read-Host | Set-Variable id
    Write-Host '[Info] ' -ForegroundColor Cyan -NoNewline
    Write-Host '请输入密码:'
    Read-Host -AsSecureString | Set-Variable pass

    $pass = [System.Net.NetworkCredential]::new('', $pass).Password # this looks stupid :(

    $config -creplace '"\{STUID\}"', "`"$id`"" -creplace '"\{PSWD\}"', "`"$pass`"" | `
        Out-File -FilePath 'config.yml' -Encoding UTF8 -Force

    Write-Host '[Info] ' -ForegroundColor Cyan -NoNewline
    Write-Host '已将配置写入config.yml文件.'
    Pause
}

####
# Start from here:
####
$step = 1

Write-Host "[Step $step] " -ForegroundColor Red -NoNewLine
Write-Host "检查Python环境..." -ForegroundColor White
$step++
$justInstalled=0
Invoke-Expression 'python -V'   | Set-Variable v
if (-not ($v -match '3\.\w\.\w')) {
    Write-Error "未正确配置Python环境."
    try {
        Write-Host "[Step $step] " -ForegroundColor Red -NoNewLine
        Write-Host "正在尝试安装Python环境, 这取决于目前网络环境速度. (Source: npm.taobao.org 淘宝镜像源)"
        $step++
        if(!(Test-Path 'python-installer.exe')) {
            Invoke-WebRequest -Uri 'http://npm.taobao.org/mirrors/python/3.7.8/python-3.7.8-amd64.exe' -OutFile 'python-installer.exe'
        }
        pwd | set "cwd"
        .\python-installer.exe /quiet PrependPath=1 Include_test=0 `
            TargetDir="$cwd\python3" Shortcuts=0 Include_doc=0 Include_dev=0 Include_launcher=0

        $justInstalled = 1
        while (!(Test-Path "$cwd\python3\Scripts\pip.exe")) {
            Start-Sleep -Seconds 1
        }
        Start-Sleep -Seconds 3
    }
    catch { Write-Host $error[0]; break }
}

Write-Host "[Step $step] " -ForegroundColor Red -NoNewLine
Write-Host "正在检查pip指令是否可用."
$step++
Invoke-Expression 'pip -V'      | Set-Variable pv
if ($pv -match '^pip\s\w{2}\.\w\.\w') {
    Write-Host "[Step $step] " -ForegroundColor Red -NoNewLine
    Write-Host "正在安装运行所需的Python Package."
    $step++
    iex 'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt'
}
elseif($justInstalled -eq 1) {
    iex "$cwd\python3\Scripts\pip.exe install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt"
}
else {
    Write-Host "[Step $step] " -ForegroundColor Red -NoNewLine
    Write-Host "正在安装运行所需的Python Package."
    $step++
    @(iex 'cmd /U/C where python')[0].ToString().Replace('python.exe', 'Scripts') | set ppath
    iex "$ppath\pip.exe install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt"
}
Write-Host "[Step $step] " -ForegroundColor Red -NoNewLine
Write-Host "记录账号信息（信息仅在本地存储）"
Initialize # this performs the function defined most above.