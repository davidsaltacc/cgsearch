$isPublish = ($args[0] -eq "publish") 
$isBuild = ($args[0] -eq "build") 
$isRuntimeInstallationOnly = ($args[0] -eq "onlyRuntime") 
$buildTarget = $args[1]

if ($buildTarget -and ![System.IO.Path]::IsPathRooted($buildTarget)) {
    $buildTarget = (Join-Path -Path "ui" -ChildPath $buildTarget)
}

$kvPairs = @{}

Get-Content "properties.txt" | ForEach-Object {
    $line = $_.Trim() 
    if ($line -match "^([^=]+)=(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $kvPairs[$key] = $value
    }
}

$name = $kvPairs["name"]
$exename = $kvPairs["exename"]
$version = $kvPairs["version"]
$buildpath = $buildTarget

if ($isPublish) {

    # delete unneccessary files
    $pdbFile = (Join-Path -Path ${buildpath} -ChildPath "${exename}.pdb")
    $depsFile = (Join-Path -Path ${buildpath} -ChildPath "${exename}.deps.json")
    if (Test-Path $pdbFile) { Remove-Item $pdbFile -Force }
    if (Test-Path $depsFile) { Remove-Item $depsFile -Force }

}

if (!(Test-Path "runtime/runtime_valid")) { 

    # clean up old python embeddable runtime
    
    if (Test-Path "runtime") { Remove-Item "runtime" -Recurse -Force }

    # download python embeddable runtime
    Invoke-WebRequest "https://www.python.org/ftp/python/3.13.6/python-3.13.6-embed-amd64.zip" -OutFile "python_embeddable_runtime.zip"
    Expand-Archive -Path "python_embeddable_runtime.zip" -DestinationPath "runtime" -Force

    # install pip
    Invoke-WebRequest "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
    Invoke-Expression "./runtime/python.exe get-pip.py"

    # clean up
    Remove-Item -Path "python_embeddable_runtime.zip"
    Remove-Item -Path "get-pip.py"

    # install dependencies
    # with the path file, even with "import site" added, it still can't import files in the same directory as main.py 
    # and i don't think there is harm in just removing it. 
    Remove-Item -Path "runtime/python313._pth" 
    Invoke-Expression "runtime/Scripts/pip.exe install -r search/requirements.txt --target runtime/Lib/site-packages" 2> $null
    # don't mind the stderr suppression, it makes my vs builds fail even with successful installation due to obscure reasons

    # a file so we can cache the runtime, so we don't have to re-download it each build
    New-Item -Path "runtime/runtime_valid" -ItemType File

}

if ($isRuntimeInstallationOnly) {
    exit 0
}

if ($buildTarget) {

    Copy-Item "runtime" (Join-Path -Path "$buildTarget" -ChildPath "bin/runtime") -Recurse -Force
    Copy-Item "search" (Join-Path -Path "$buildTarget" -ChildPath "search") -Recurse -Force
    Copy-Item "icon.ico" -Destination "$buildTarget"

}

if ($isPublish) {

    # remove pycache folders
    Get-ChildItem -Path "./" -Directory -Recurse -Force -Filter "__pycache__" | Remove-Item -Recurse -Force

    # make portable
    
    Compress-Archive -Path "$buildpath\*" -DestinationPath "$name Portable.zip" -CompressionLevel Optimal -Force

    # make installer
    Copy-Item -Path "make_installer.nsi" -Destination "make_installer_temp.nsi"
    (Get-Content "make_installer_temp.nsi") -replace "POWERSHELL_INSERTS_THIS-name", "$name" | Set-Content "make_installer_temp.nsi"
    (Get-Content "make_installer_temp.nsi") -replace "POWERSHELL_INSERTS_THIS-exename", "$exename" | Set-Content "make_installer_temp.nsi"
    (Get-Content "make_installer_temp.nsi") -replace "POWERSHELL_INSERTS_THIS-version", "$version" | Set-Content "make_installer_temp.nsi"
    (Get-Content "make_installer_temp.nsi") -replace "POWERSHELL_INSERTS_THIS-buildpath", "$buildpath" | Set-Content "make_installer_temp.nsi"
    (Get-Content "make_installer_temp.nsi") -replace "POWERSHELL_INSERTS_THIS-outfile", "$name Installer.exe" | Set-Content "make_installer_temp.nsi"
    (Get-Content "make_installer_temp.nsi") -replace "Quit ;REMOVED_BY_POWERSHELL", "" | Set-Content "make_installer_temp.nsi"
    Invoke-Expression "makensis make_installer_temp.nsi"
    Remove-Item "make_installer_temp.nsi"

    if (!(Test-Path "build")) { New-Item -Name "build" -ItemType "Directory" }
     
    Move-Item -Path "$name Installer.exe" -Destination "build\$name $version Installer.exe" -Force
    Move-Item -Path "$name Portable.zip" -Destination "build\$name $version Portable.zip" -Force

}