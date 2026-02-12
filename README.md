# 123456

## 热词新闻简报 Agent

该 Agent 会联网查询热词相关新闻，并每隔两小时输出一份简报到控制台。

### 安装依赖

```bash
npm install
```

### 运行

```bash
npm start -- 人工智能 经济
```

也可以通过环境变量提供热词（逗号分隔）：

```bash
HOT_KEYWORDS=人工智能,经济 npm start
```
