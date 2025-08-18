namespace CGSearchUI
{
    public class EngineResultLink(string repackTitle, string provider, string linkName, string linkUrl, string linkType, float score)
    {

        public string RepackTitle { get; set; } = repackTitle;
        public string Provider { get; set; } = provider;
        public string LinkName { get; set; } = linkName;
        public string LinkUrl { get; set; } = linkUrl;
        public string LinkType { get; set; } = linkType;
        public float Score { get; set; } = float.Round(score, 3);
    }
}