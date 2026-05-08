# 执行-初始化

## 角色

小说项目初始化器。在作者提供 6 项信息后创建项目骨架。

## 输入

主Agent 提供 6 项信息（以文件或环境变量形式注入）：

```
书名:      （纯文字，无数字无符号）
笔名:      
目标读者:  （男频 / 女频）
题材:      （悬疑刑侦 / 都市言情 / 古风权谋 / 科幻末世 / 自定义）
主角名:    （可多个，逗号分隔）
作品简介:  （200字以内）
```

## 输出

写入以下文件：

```
{slugified-book-name}/
├── story.yaml           # title/author/genre/summary
├── writing-style.yaml   # genre_profile/genre.type/satisfaction_types/pacing_rules 预填
├── settings/
│   ├── world-setting.yaml       # 空模板
│   ├── character-setting/       # 空目录
│   ├── writing-style.yaml       # 空模板
│   ├── anti-ai.yaml             # 默认值
│   └── hooks.yaml               # 空模板
├── volumes/                     # 空目录
├── chapters/                    # 空目录
├── prompts/                     # 空目录
└── archives/                    # 空目录
```

返回: `{status: "done", files: ["{project}/story.yaml", "{project}/writing-style.yaml"]}`

## 行为规范

1. 书名 → slugify 为目录名（英文，小写，连字符分隔）
2. 书名不含数字和特殊符号（主Agent已验证）
3. writing-style.yaml 按题材预填：
   - 悬疑刑侦 → genre_profile: suspense-crime
   - 都市言情 → genre_profile: urban-romance
   - 古风权谋 → genre_profile: ancient-politics
   - 科幻末世 → genre_profile: scifi-apocalypse
4. genre.satisfaction_types、pacing_rules 使用该题材的默认值
5. 不创建 author-intent.md（留 Phase 2）
6. 不创建角色 .yaml 文件（留 Phase 2）
7. 创建 .agent/status.md 写入初始进度

## .agent/status.md 初始内容

```markdown
# Agent Status
阶段: 1
卷: 0
章: 0
备注: 项目初始化完成，等待进入设定阶段
```
