
# clean up old python embeddable runtime
Remove-Item "runtime" -Recurse -Force

# download python embeddable runtime
Invoke-WebRequest "https://www.python.org/ftp/python/3.13.6/python-3.13.6-embed-win32.zip" -OutFile "python_embeddable_runtime.zip"
Expand-Archive -Path "python_embeddable_runtime.zip" -DestinationPath "runtime" -Force

# install pip
Invoke-WebRequest "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
Invoke-Expression "./runtime/python.exe get-pip.py"

# clean up
Remove-Item -Path "python_embeddable_runtime.zip"
Remove-Item -Path "get-pip.py"

# install dependencies
Add-Content -Path "runtime/python313._pth" -Value "import site"
Invoke-Expression "runtime/Scripts/pip.exe install -r search/requirements.txt --target runtime/Lib/site-packages"
