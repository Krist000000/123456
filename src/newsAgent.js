const { XMLParser } = require("fast-xml-parser");

const DEFAULT_INTERVAL_MS = 2 * 60 * 60 * 1000;
const DEFAULT_KEYWORDS = ["中国房地产最新情况"];
const MAX_ITEMS = 5;
const parser = new XMLParser({ ignoreAttributes: false });

const parseKeywords = () => {
  const args = process.argv.slice(2).filter(Boolean);
  const raw = args.length > 0 ? args : [process.env.HOT_KEYWORDS || ""];

  const keywords = raw
    .flatMap((entry) => entry.split(","))
    .map((entry) => entry.trim())
    .filter(Boolean);
  return keywords.length > 0 ? keywords : DEFAULT_KEYWORDS;
};

const toArray = (value) => {
  if (!value) {
    return [];
  }
  return Array.isArray(value) ? value : [value];
};

const fetchNewsForKeyword = async (keyword) => {
  const url = `https://news.google.com/rss/search?q=${encodeURIComponent(
    keyword
  )}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans`;

  const response = await fetch(url, {
    headers: {
      "User-Agent": "news-brief-agent/1.0",
    },
  });

  if (!response.ok) {
    throw new Error(`获取“${keyword}”新闻失败，状态码：${response.status}`);
  }

  const xml = await response.text();
  const data = parser.parse(xml);
  const items = toArray(data?.rss?.channel?.item).slice(0, MAX_ITEMS);

  return items.map((item) => ({
    title: item.title || "未命名",
    link: item.link || "",
    pubDate: item.pubDate || "",
  }));
};

const formatBriefing = (keyword, items) => {
  if (items.length === 0) {
    return `- ${keyword}：暂无相关新闻。`;
  }

  const lines = items.map((item, index) => {
    const date = item.pubDate ? `（${item.pubDate}）` : "";
    return `  ${index + 1}. ${item.title}${date}\n     ${item.link}`.trimEnd();
  });

  return [`- ${keyword}：`, ...lines].join("\n");
};

const generateBriefing = async (keywords) => {
  const timestamp = new Date().toLocaleString("zh-CN", { hour12: false });
  const results = await Promise.all(
    keywords.map(async (keyword) => {
      try {
        const items = await fetchNewsForKeyword(keyword);
        return formatBriefing(keyword, items);
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return `- ${keyword}：获取失败 (${message})`;
      }
    })
  );

  return [`\n=== 热词新闻简报 (${timestamp}) ===`, ...results].join("\n");
};

let isRunning = false;
const runBriefing = async (keywords) => {
  if (isRunning) {
    return;
  }
  isRunning = true;
  try {
    const briefing = await generateBriefing(keywords);
    console.log(briefing);
  } finally {
    isRunning = false;
  }
};

const keywords = parseKeywords();

let timerId;
const scheduleNext = () => {
  timerId = setTimeout(() => {
    runBriefing(keywords)
      .catch((error) => {
        console.error("生成简报失败：", error);
      })
      .finally(scheduleNext);
  }, DEFAULT_INTERVAL_MS);
};

runBriefing(keywords)
  .catch((error) => {
    console.error("生成简报失败：", error);
  })
  .finally(scheduleNext);

const shutdown = (exitCode = 0) => {
  if (timerId) {
    clearTimeout(timerId);
  }
  process.exit(exitCode);
};

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

process.on("unhandledRejection", (error) => {
  console.error("未处理的 Promise 拒绝：", error);
  shutdown(1);
});
