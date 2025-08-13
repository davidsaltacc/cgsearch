!include "MUI.nsh"

!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\nsis3-install-alt.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\nsis3-uninstall.ico"

!define APP_NAME "CGSearch"
!define MAIN_EXE "CGSearchUI.exe"

Name ${APP_NAME}
InstallDir "C:\Program Files\${APP_NAME}"
OutFile "CGSearch Installer.exe"
BrandingText " "
SetCompressor /SOLID lzma

!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\nsis3-metro.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\nsis3-metro.bmp"

!define MUI_INSTFILESPAGE_NOAUTOCLOSE

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_DIRECTORY
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Core Components (Required)"
SectionIn RO

WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "0.1.0.0"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "justacoder"
;UNCOMMENT AFTER WE HAVE AN ICON WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\${APP_NAME}.ico"
WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\unins.exe"
;TODO WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "EstimatedSize" ${INSTALLSIZE}


SetOutPath "$INSTDIR\bin\runtime"
File /r "runtime\*"

SetOutPath "$INSTDIR\search"
File /r "search\*"

SetOutPath "$INSTDIR"
File "LICENSE"
;TODO icon; File /oname=${APP_NAME}.ico PATHTOICONHERE 
WriteUninstaller "unins.exe"

File "ui\bin\Release\net8.0\win-x64\publish\${MAIN_EXE}"
File "ui\bin\Release\net8.0\win-x64\publish\*.dll"

SectionEnd

Section "Start Menu Shortcuts"
SectionIn 1

SetOutPath "$INSTDIR"
CreateDirectory "$SMPROGRAMS\${APP_NAME}"
CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" '$INSTDIR\${MAIN_EXE}' "" '$INSTDIR\${MAIN_EXE}' 0
CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall ${APP_NAME}.lnk" '$INSTDIR\unins.exe' "" '$INSTDIR\unins.exe' 0

SectionEnd

Section "Desktop Shortcut"
SectionIn 1

SetOutPath "$INSTDIR"
CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${MAIN_EXE}"

SectionEnd

Section "Uninstall"

RMDIR /r "$INSTDIR"
DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

RMDIR /r "$SMPROGRAMS\${APP_NAME}"
Delete "$DESKTOP\${APP_NAME}.lnk"

SectionEnd