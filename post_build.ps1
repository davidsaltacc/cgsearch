
# remove pycache folders
Get-ChildItem -Path "./" -Directory -Recurse -Force -Filter "__pycache__" | Remove-Item -Recurse -Force

# make installer
Invoke-Expression "makensis make_installer.nsi"