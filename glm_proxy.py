#!/usr/bin/env python3
"""
本地 CORS 代理 — 解决浏览器无法直接调用 GLM/DeepSeek/Moonshot 等 API 的跨域问题。

【用法】
  1. 终端运行：  python3 glm_proxy.py
  2. 在 etymology_map.html 的 ⚙ 设置中勾选「使用本地代理」
  3. 端点保持原样（如 https://open.bigmodel.cn/api/paas/v4/chat/completions）
  4. 重新点 ✨ AI 补全 → 🔗 测试连接

【停止】Ctrl+C
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json
import sys

PORT = 8787
TARGET_PREFIX = ''  # URL path after / is the real target


class CORSProxy(BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
        self.send_header('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, x-api-key, anthropic-version, '
                         'anthropic-dangerous-direct-browser-access, Accept')
        self.send_header('Access-Control-Max-Age', '86400')

    def do_OPTIONS(self):
        """Preflight request"""
        self.send_response(204)
        self._send_cors()
        self.end_headers()

    def do_POST(self):
        # The path after the leading / should be the full target URL
        target = self.path.lstrip('/')
        if not target.startswith('http'):
            target = 'https://' + target

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length > 0 else b''

        # Forward only the relevant headers
        fwd_headers = {'Content-Type': self.headers.get('Content-Type', 'application/json')}
        for h in ('Authorization', 'x-api-key', 'anthropic-version',
                  'anthropic-dangerous-direct-browser-access', 'Accept'):
            v = self.headers.get(h)
            if v:
                fwd_headers[h] = v

        req = urllib.request.Request(target, data=body, headers=fwd_headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()
                self.send_response(resp.status)
                ct = resp.headers.get('Content-Type', 'application/json')
                self.send_header('Content-Type', ct)
                self._send_cors()
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self._send_cors()
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self._send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'proxy_error',
                'message': str(e),
                'hint': '检查目标 URL 是否正确、API Key 是否有效',
            }, ensure_ascii=False).encode())

    def log_message(self, fmt, *args):
        # color + timestamp
        msg = fmt % args
        if '404' in msg or '502' in msg or '500' in msg:
            sys.stderr.write(f"\033[91m[{self.log_date_time_string()}] {msg}\033[0m\n")
        else:
            sys.stderr.write(f"\033[92m[{self.log_date_time_string()}] {msg}\033[0m\n")


if __name__ == '__main__':
    banner = f"""
\033[95m╔══════════════════════════════════════════════════════════╗
║  🚀 LLM CORS Proxy 已启动                                ║
║  监听: http://localhost:{PORT}                              ║
╚══════════════════════════════════════════════════════════╝\033[0m

\033[97m【下一步】\033[0m
  1. 在 etymology_map.html 中点右上角 \033[93m⚙\033[0m
  2. 勾选「\033[93m使用本地代理（解决 CORS）\033[0m」
  3. 端点保持 GLM 默认：\033[37mopen.bigmodel.cn/api/paas/v4/chat/completions\033[0m
  4. 填 API Key → \033[93m🔗 测试连接\033[0m → 应该显示 ✓ 连接成功

\033[90m按 Ctrl+C 停止代理\033[0m
"""
    print(banner)
    try:
        HTTPServer(('127.0.0.1', PORT), CORSProxy).serve_forever()
    except KeyboardInterrupt:
        print('\n\033[93m代理已停止\033[0m')
        sys.exit(0)
