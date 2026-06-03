# 学员上手：把 Homestead 变成「你的」官网（5 步）

部署完成后（见 [`deploy-new-instance.md`](deploy-new-instance.md) 或交给 agent 的
[`AGENT-DEPLOY.md`](../AGENT-DEPLOY.md)），按下面 5 步把空站变成你行业的专业官网。
**不需要任何图片生成服务**——图片先用「带提示词的占位图」，之后再换成你自己的图。

> 全程可以直接用 Telegram 对小爪说话（技能 `/oracle_site_rebrand`、`/oracle_site_media`、
> `/oracle_site_i18n` 等），也可以自己 curl。下面给 curl;先准备好 `$ORACLE_SITE_API` 和 admin token
> （见 [`api-contract.md`](api-contract.md) 或 `oracle-site-shared` 技能）。

## 1) 一键换成你的行业

```bash
curl -s -X POST "$ORACLE_SITE_API/admin/site/rebrand" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -d '{"industry":"beauty"}'   # restaurant / healthcare / legal / fitness …
```

首页+内页立刻变成该行业的**完整 9 块结构**（大图 hero·服务·作品集·流程·口碑·价格·FAQ·CTA），
每个图位是**带提示词的占位图**。换错了？`POST /admin/undo {"target":"home"}` 可撤销。

## 2) 换上你自己的图（占位图上写着该放什么）

每个空图位会显示一段提示词（该放什么照片）。拍好/选好图后上传，再填进对应 block：

```bash
URL=$(curl -s -X POST "$ORACLE_SITE_API/admin/media" -H "Authorization: Bearer $TOKEN" \
        -F "file=@your-photo.jpg" | jq -r .item.url)            # 返回绝对 URL
# 把 URL 填到 hero 的 image（用 GET /admin/surfaces 看 block id）
curl -s -X PATCH "$ORACLE_SITE_API/admin/compose/home/blocks/<blockId>" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -d "{\"content\":{\"image\":\"$URL\"}}"
```

填了真图，占位图自动消失。（有图片生成器？`oracle-site-rebrand` 技能能按提示词自动出图。）

## 3) 改文案、改店名

- 文案：`GET /admin/surfaces` 看有哪些面和 block → `PATCH /admin/compose/<target>/blocks/<id>` 改文字。
- 店名/品牌：改后端 `.env` 的 `SITE_NAME`（以及 `SITE_INDUSTRY`/`SITE_REGION`）→ 重新构建前端。

## 4) 做成中英双语（路径式 `/zh`）

在写操作加 `?locale=zh` 就是写中文版（**在相同 block id 上原地翻译，别改结构**）：

```bash
curl -s -X PATCH "$ORACLE_SITE_API/admin/compose/home/blocks/<id>?locale=zh" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -d '{"content":{"headline":"你的中文标题"}}'
```

整页翻译用 `oracle-site-i18n` 技能最省事。

## 5) 验收：一致性审计要「全绿」

```bash
curl -s "$ORACLE_SITE_API/admin/consistency" -H "Authorization: Bearer $TOKEN" | jq '.item.ok, .item.summary'
```

`ok:true` = 没有「中英错位 / 缺翻译 / 结构发散 / 旧行业残留」。修到全绿，再打开 `/en` 和 `/zh` 看一眼，就完成了。

---

**想加一个还没有的行业模板？** 在 `backend/app/services/design_service.py` 的
`_RICH_INDUSTRY_SPECS` 加一条 spec（行业文案 + 6 个配图提示词），就照 `beauty` 的样子；
即时拥有同样「图文完整 + 自带配图占位」的模板。能力总览见 [`REFERENCE.zh.md`](REFERENCE.zh.md)。
