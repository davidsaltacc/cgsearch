Function .onInit
    Quit ;REMOVED_BY_POWERSHELL
    ; this gets removed by powershell, the reason this exists so no one accidentally runs this using makensis(w) - leaving the powershell-inserted variables at what they are
FunctionEnd

!include "MUI.nsh"

!define MUI_ICON "icons\install.ico"
!define MUI_UNICON "icons\uninstall.ico"

!define name "POWERSHELL_INSERTS_THIS-name"
!define outfile "POWERSHELL_INSERTS_THIS-outfile"
!define exename "POWERSHELL_INSERTS_THIS-exename"
!define version "POWERSHELL_INSERTS_THIS-version"
!define buildpath "POWERSHELL_INSERTS_THIS-buildpath"

!define APP_NAME ${name}
!define MAIN_EXE "${exename}.exe"

Name ${APP_NAME}
InstallDir "C:\Program Files\${APP_NAME}"
OutFile "${outfile}"
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

; TODO MUI_PAGE_STARTMENU seems to be a thing? investigate.

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_DIRECTORY
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "CGSearch"
SectionIn RO

WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${version}"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "justacoder"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\icon.ico"
WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\unins.exe"
;TODO WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "EstimatedSize" ${INSTALLSIZE}

SetOutPath "$INSTDIR"
File "LICENSE"
WriteUninstaller "unins.exe"

File /r "${buildpath}\*"

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