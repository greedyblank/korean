#!/bin/bash
# 一键部署到 Cloudflare Pages（非泄露 · 不进 Git）
# 用法：改完本地文件后，在本项目目录跑  bash deploy.sh
# 首次需配置 CLOUDFLARE_API_TOKEN（见下方说明）。
set -e
cd "$(dirname "$0")"

: "${CLOUDFLARE_API_TOKEN:?请先设置 CLOUDFLARE_API_TOKEN 环境变量（见 README/部署说明）}"

TMP=$(mktemp -d)
trap "rm -rf '$TMP'" EXIT
cp etymology_map.html verb_phonetic_symbolism.js manifest.json sw.js \
   icon-192.png icon-512.png icon-maskable-512.png apple-touch-icon.png "$TMP/"

echo "↑ 部署 Korean → Cloudflare Pages ..."
wrangler pages deploy "$TMP" --project-name korean --branch main --commit-dirty=true
echo "✅ 完成 → https://korean-b7f.pages.dev/etymology_map"
