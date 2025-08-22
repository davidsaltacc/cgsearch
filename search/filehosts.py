from enum import Enum

class IsBad(Enum):
    No = 0
    Slightly = 1
    Yes = 2

class Filehost:

    def matches(self, linkName, linkType, linkData):
        if len(self.tags) > 0 and linkType.lower() == self.tags[0].lower():
            return True
        for part in [linkName, linkData]:
            for tag in self.tags:
                if tag in part.replace(" ", "").lower():
                    return True
        return False

    def __init__(self, name, *tags, bad = IsBad.No, warning = None, second_pass = False):
        self.name = name
        self.tags = tags
        self.bad = bad
        self.warning = warning
        self.second_pass = second_pass
    
class AllFilehosts(Enum): # 1. is for showing warnings on bad filehosts, and 2. for being able to sort through filehosts easily
    # feel free to expand the list.
    # note that all spaces are stripped from links before searching, so a tag with a space in it will never be found.
    # the links and names also get lowercased before.
    Unknown = Filehost("Unknown", bad = IsBad.Slightly) 
    Torrent = Filehost("Torrent", "torrent")
    Official = Filehost("Official", "official")
    Multiple = Filehost("Multiple Filehosts", "filecrypt", "multiup", "multiple", "bin.0xfc", second_pass = True)
    DDownload = Filehost("DDownload", "ddownload", bad = IsBad.Yes, warning = "Warning: A DDownload link was detected. Their downloads are extemely slow without their premium plan, you might want to choose a different link if available.")
    RapidGator = Filehost("RapidGator", "rapidgator", bad = IsBad.Yes, warning = "Warning: A RapidGator link was detected. Their downloads are extemely slow without their premium plan, you might want to choose a different link if available.")
    NitroFlare = Filehost("NitroFlare", "nitroflare", bad = IsBad.Yes, warning = "Warning: A NitroFlare link was detected. Their downloads are extemely slow without their premium plan, you might want to choose a different link if available.")
    FikPer = Filehost("FikPer", "fikper", bad = IsBad.Yes, warning = "Warning: A FikPer link was detected. Their downloads are extemely slow without their premium plan, you might want to choose a different link if available.")
    OneFichier = Filehost("1Fichier", "1fichier", "onefichier", "1ficher", "1fitchier", "1fitcher", bad = IsBad.Slightly, warning = "Warning: A 1Fichier link was detected. Their download speed isn't extremely slow, but the site has several limitations on their free plan. For example, if you try to access a file a second time, you will have to wait out a very long countdown. You might want to choose a different link if available.")
    Qiwi = Filehost("Qiwi", "qiwi", bad = IsBad.Yes, warning = "Warning: A Qiwi link was detected. They used to be a good filehost, but with their migration to ranoz.gg all qiwi.gg links got invalidated. This may be subject to change in the future, but for now you might want to choose a different link if available.")
    ZippyShare = Filehost("ZippyShare", "zippyshare", bad = IsBad.Yes, warning = "Warning: A ZippyShare link was detected. ZippyShare got taken down, you should probably choose a different link.")
    PixelDrain = Filehost("Pixeldrain", "pixeldrain", warning = "Warning: A PixelDrain link was detected. Pixeldrain may be good in terms of download speed, but there is a limit on how much you can download. This can be bypassed though, for example with userscripts such as MegaLime0/pixeldrain-bypass-usercript on github.")
    VikingFile = Filehost("Viking File", "viking", "vking")
    Ranoz = Filehost("Ranoz", "ranoz")
    DataNodes = Filehost("DataNodes", "datanodes")
    FuckingFast = Filehost("FuckingFast", "fuckingfast")
    OneDrive = Filehost("OneDrive", "onedrive")
    GoFile = Filehost("Gofile", "gofile")
    FileQ = Filehost("FileQ", "fileq")
    FileMirage = Filehost("FileMirage", "filemirage")
    UpToBox = Filehost("UpToBox", "uptobox")
    DataVaults = Filehost("DataVaults", "datavaults", warning = "Warning: Just a heads up, datavaults has an annoying 30 second countdown before you can download a file.")
    BuzzHeavier = Filehost("BuzzHeavier", "buzzheavier", "buzz", "buzzheavr")
    BowFile = Filehost("BowFile", "bowfile", bad = IsBad.Slightly, warning = "Warning: A BowFile link was detected. Please note that on their free plan download speeds are limited to about 1mb/s.")
    AkiraBox = Filehost("AkiraBox", "akira")
    Terabox = Filehost("TeraBox", "terabox", bad = IsBad.Slightly, warning = "Warning: A TeraBox link was detected. To download a file from terabox, you need an account, so you might want to choose a different link.")
    GoogleDrive = Filehost("Google Drive", "googledrive", "google")
    DooDrive = Filehost("DooDrive", "doodrive", bad = IsBad.Slightly, warning = "Warning: A DooDrive link was detected. To download a file from DooDrive, you need to go through an annoying process of clicking through ads, you might want to choose a different link.")

def get_filehost(linkName, linkType, linkData):
    # two passes, so links belonging to a specific filehost, but hosted on filecrypt or similar, won't get falsely marked as "Multiple Filehosts" 
    for filehost in AllFilehosts:
        if not filehost.value.second_pass and filehost.value.matches(linkName, linkType, linkData):
            return filehost.value
    for filehost in AllFilehosts:
        if filehost.value.second_pass and filehost.value.matches(linkName, linkType, linkData):
            return filehost.value
    return AllFilehosts.Unknown.value

def warning_filehost(linkName, linkType, linkData):
    filehost = get_filehost(linkName, linkType, linkData)
    if filehost.warning:
        return filehost.warning
    return None