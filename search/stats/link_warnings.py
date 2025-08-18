from enum import Enum

class NotRecommendedFilehost(Enum): # more can be added, there are just some more used ones
    DDownload = 1 # slow without premium
    RapidGator = 2 # slow without premium
    NitroFlare = 3 # slow without premium
    FikPer = 4 # slow without premium
    OneFichier = 5 # annoying limitations
    Qiwi = 6 # with their migration to ranoz.gg, qiwi links don't work 
    ZippyShare = 7 # shut down
    PixelDrain = 8 # is good in terms of speed, has a download limit though - can be bypassed

def information_filehost(items):
    
    filehost = None

    for item in items:
        if "ddownload" in item.lower():
            filehost = NotRecommendedFilehost.DDownload
        if "rapidgator" in item.lower():
            filehost = NotRecommendedFilehost.RapidGator
        if "nitroflare" in item.lower():
            filehost = NotRecommendedFilehost.NitroFlare
        if "fikper" in item.lower():
            filehost = NotRecommendedFilehost.FikPer
        if "1fichier" in item.lower():
            filehost = NotRecommendedFilehost.OneFichier
        if "qiwi" in item.lower():
            filehost = NotRecommendedFilehost.Qiwi
        if "zippyshare" in item.lower():
            filehost = NotRecommendedFilehost.ZippyShare
        if "pixeldrain" in item.lower():
            filehost = NotRecommendedFilehost.PixelDrain
    
    if filehost:
        if filehost == NotRecommendedFilehost.DDownload:
            return "Warning: A DDownload link was detected. Their downloads are extemely slow without their premium plan, you might want to choose a different link if available."
        if filehost == NotRecommendedFilehost.RapidGator:
            return "Warning: A RapidGator link was detected. Their downloads are extemely slow without their premium plan, you might want to choose a different link if available."
        if filehost == NotRecommendedFilehost.NitroFlare:
            return "Warning: A NitroFlare link was detected. Their downloads are extemely slow without their premium plan, you might want to choose a different link if available."
        if filehost == NotRecommendedFilehost.FikPer:
            return "Warning: A FikPer link was detected. Their downloads are extemely slow without their premium plan, you might want to choose a different link if available."
        if filehost == NotRecommendedFilehost.OneFichier:
            return "Warning: A 1Fichier link was detected. Their download speed isn't extremely slow, but the site has several limitations on their free plan. For example, if you try to access a file a second time, you will have to wait out a very long countdown. You might want to choose a different link if available."
        if filehost == NotRecommendedFilehost.Qiwi:
            return "Warning: A Qiwi link was detected. They used to be a good filehost, but with their migration to ranoz.gg all qiwi.gg links got invalidated. This may be subject to change in the future, but for now you might want to choose a different link if available."
        if filehost == NotRecommendedFilehost.ZippyShare:
            return "Warning: A ZippyShare link was detected. ZippyShare got taken down, you should probably choose a different link."
        if filehost == NotRecommendedFilehost.PixelDrain:
            return "Warning: A PixelDrain link was detected. Pixeldrain may be good in terms of download speed, but there is a limit on how much you can download. This can be bypassed though, for example with userscripts such as MegaLime0/pixeldrain-bypass-usercript on github."
    else: 
        return None