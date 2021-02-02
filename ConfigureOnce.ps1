function Initialize {
    Get-Content -Path 'configexample.yml' -Encoding UTF8 | Out-String | Set-Variable 'config'
    Write-Host '[INFO] ' Cyan;
    Write-Host '请输入需要自动打卡的信息化门户账号:'
    Read-Host                   | Set-Variable id
    Write-Host '[INFO] ' Cyan;
    Write-Host '请输入密码:'
    Read-Host -AsSecureString   | Set-Variable pass

    $pass = [System.Net.NetworkCredential]::new('', $pass).Password # this looks stupid :(

    $config -creplace '\{STUID\}', $id -creplace '\{PSWD\}', $pass | `
        Out-File -FilePath 'config.yml' -Encoding UTF8
}

####
# Start from here:
####

Write-Host '检查Python环境...' -ForegroundColor White
Invoke-Expression 'python -V'   | Set-Variable v
if (-not ($v -match '3\.\w\.\w')) {
    Write-Error "未正确配置Python环境。"
    try {
        Write-Host "[INFO] 正在尝试安装python环境"
        Invoke-WebRequest -Uri 'http://npm.taobao.org/mirrors/python/3.7.8/python-3.7.8-amd64.exe' -OutFile 'python-installer.exe'
        .\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    }
    catch { Write-Host $error[0]; break }
}

Invoke-Expression 'pip -V'      | Set-Variable pv
if ($pv -match '^pip\s\w{2}\.\w\.\w') {
    iex 'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt'
}
else {
    @(iex 'cmd /U/C where python')[0].ToString().Replace('python.exe', 'Scripts') | set ppath
    iex "$ppath\pip.exe install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt"
}

Initialize # this performs the function defined most above.