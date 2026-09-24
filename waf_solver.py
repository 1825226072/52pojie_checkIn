# -*- coding: utf-8 -*-
"""
吾爱破解（52pojie）网宿（WZWS）WAF 防护盾纯 Python 求解器
实现自动提取挑战参数、计算 answer、生成设备指纹校验并提交通行验证。
无需 Node.js、execjs 或第三方打码/解密服务，纯原生 Python 实现。
"""

import re
import json
import time
import logging
from typing import Optional, Tuple
import requests

logger = logging.getLogger("WafSolver")


def calc_answer(wzwsquestion: str, wzwsfactor: int) -> str:
    """根据服务器下发的挑战参数计算 answer."""
    d = 0
    s = 1
    for p, char in enumerate(wzwsquestion):
        d = 2 * (d + ord(char))
        s = 2 * (s + p + 1)
    d = d * wzwsfactor + s
    return f"WZWS_CONFIRM_PREFIX_LABEL{d}"


def encode_custom_base64(data_bytes: bytes, base64_chars: str) -> str:
    """使用服务器动态指定的 64 位字符表进行 Base64 编码."""
    p = []
    length = len(data_bytes)
    q = 0
    while q < length:
        f = data_bytes[q]
        q += 1
        if q == length:
            p.append(base64_chars[f >> 2])
            p.append(base64_chars[(f & 3) << 4])
            p.append('==')
            break
        u = data_bytes[q]
        q += 1
        if q == length:
            p.append(base64_chars[f >> 2])
            p.append(base64_chars[((f & 3) << 4) | ((u & 0xf0) >> 4)])
            p.append(base64_chars[(u & 0xf) << 2])
            p.append('=')
            break
        z = data_bytes[q]
        q += 1
        p.append(base64_chars[f >> 2])
        p.append(base64_chars[((f & 3) << 4) | ((u & 0xf0) >> 4)])
        p.append(base64_chars[((u & 0xf) << 2) | ((z & 0xc0) >> 6)])
        p.append(base64_chars[z & 0x3f])
    return ''.join(p)


def build_fp_payload(timestamp: int, answer: str, user_agent: str) -> dict:
    """构造设备指纹并动态计算 verify 校验和."""
    y = (timestamp % 10) or 10

    plugins_details = [
        {"name": "PDF Viewer", "description": "Portable Document Format", "filename": "internal-pdf-viewer", "mimetypes": [{"type": "application/pdf", "suffixes": "pdf"}, {"type": "text/pdf", "suffixes": "pdf"}]},
        {"name": "Chrome PDF Viewer", "description": "Portable Document Format", "filename": "internal-pdf-viewer", "mimetypes": [{"type": "application/pdf", "suffixes": "pdf"}, {"type": "text/pdf", "suffixes": "pdf"}]},
        {"name": "Chromium PDF Viewer", "description": "Portable Document Format", "filename": "internal-pdf-viewer", "mimetypes": [{"type": "application/pdf", "suffixes": "pdf"}, {"type": "text/pdf", "suffixes": "pdf"}]},
        {"name": "Microsoft Edge PDF Viewer", "description": "Portable Document Format", "filename": "internal-pdf-viewer", "mimetypes": [{"type": "application/pdf", "suffixes": "pdf"}, {"type": "text/pdf", "suffixes": "pdf"}]},
        {"name": "WebKit built-in PDF", "description": "Portable Document Format", "filename": "internal-pdf-viewer", "mimetypes": [{"type": "application/pdf", "suffixes": "pdf"}, {"type": "text/pdf", "suffixes": "pdf"}]}
    ]
    plugin_names = [p["name"] for p in plugins_details]

    fp_infos = {
        "errors": {},
        "plugins": {
            "details": plugins_details,
            "names": plugin_names,
            "fp": "9772d5556d57fcc8177f76029bfd92ef"
        },
        "fonts": {
            "names": ["Arial", "Arial Black", "Calibri", "Comic Sans MS", "Courier New", "Georgia", "Helvetica", "Impact", "Segoe UI", "Tahoma", "Times New Roman", "Verdana"],
            "fp": "1b16b21419cf4eed8bdae341d01ae629"
        },
        "screenObject": {
            "screenResolution": [1920, 1080],
            "availableScreenResolution": [1920, 1040],
            "colorDepth": 24,
            "availTop": 0,
            "availLeft": 0,
            "isExtended": False,
            "pixelDepth": 24,
            "orientation": {"angle": 0, "type": "landscape-primary"}
        },
        "intlObject": {
            "locale": "zh-CN",
            "calendar": "gregory",
            "numberingSystem": "latn",
            "timeZone": "Asia/Shanghai",
            "year": "numeric",
            "month": "numeric",
            "day": "numeric",
            "timezoneOffset": -480
        },
        "touchSupport": [0, False, False],
        "audio": "124.04347527516074",
        "webdriver": False,
        "webGL": {
            "webgl_version": "WebGL 1.0 (OpenGL ES 2.0 Chromium)",
            "webgl_vendor_and_renderer": "Google Inc. (NVIDIA)~ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "webgl_unmasked_renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "webgl_unmasked_vendor": "Google Inc. (NVIDIA)",
            "webgl_aliased_point_size_range": [1, 1024],
            "webgl_fragment_shader_medium_int_precision_rangeMax": 30,
            "webgl_fragment_shader_medium_int_precision_rangeMin": 31,
            "fp": "ba6faa254e58a06a3de7ed87b7f1f4e5"
        },
        "canvas": {
            "canvas_winding": True,
            "fp": "5f1789b44d2008b266b283ffa91bb040"
        },
        "deviceInfos": {
            "deviceMemory": 8,
            "hardwareConcurrency": 16
        },
        "storageObject": {
            "localStorage": True,
            "openDatabase": False,
            "indexedDb": True,
            "sessionStorage": True,
            "addBehavior": False
        },
        "navigatorObject": {
            "userAgent": user_agent,
            "platform": "Win32",
            "vendor": "Google Inc.",
            "language": "zh-CN",
            "languages": ["zh-CN", "zh", "en"],
            "productSub": "20030107"
        },
        "functions": {
            "eval_tostring_length": 33
        },
        "dateTime": {
            "timestamp": timestamp
        },
        "fp": "11f1f389f6f17388040dfca306404b31",
        "protocol": "https"
    }

    # 计算每一个 section 的加权 verify
    for section_name, section in fp_infos.items():
        if isinstance(section, dict):
            x = 0
            for k, val in section.items():
                if isinstance(val, (int, float)) and not isinstance(val, bool):
                    x += int(val)
                elif isinstance(val, str):
                    x += len(val)
                else:
                    x += y
            if x:
                section["verify"] = x * y

    return {
        "fp_infos": fp_infos,
        "answer": answer,
        "hostname": "www.52pojie.cn",
        "scheme": "https"
    }


def extract_waf_params(html: str) -> Optional[Tuple[str, int, str, str]]:
    """从 WAF 拦截页面中提取动态参数 (question, factor, base64_chars, dynamicapi)."""
    m_q = re.search(r"wzwsquestion='(\d+)'", html) or re.search(r"LZ='(\d+)'", html)
    m_f = re.search(r"wzwsfactor='(\d+)'", html) or re.search(r"LJ='(\d+)'", html)
    m_b = re.search(r"base64_chars='([^']+)'", html) or re.search(r"LE='([^']+)'", html)
    m_api = re.search(r"dynamicapi='([^']+)'", html)

    if m_q and m_f and m_b:
        question = m_q.group(1)
        factor = int(m_f.group(1))
        base64_chars = m_b.group(1)
        api = m_api.group(1) if m_api else "/waf_zw_verify"
        return question, factor, base64_chars, api
    return None


def is_waf_page(text: str) -> bool:
    """判断返回的 HTML 是否属于网宿 WAF 拦截页面."""
    return ("wzwsquestion" in text or "LZ=" in text) and "waf_zw_verify" in text


def bypass_waf(session: requests.Session, current_url: str, html_content: str, timeout: int = 15) -> bool:
    """
    针对给定的 WAF 拦截页面执行自动穿透，将验证 Cookie 写回 session。
    :return: 是否通过验证
    """
    params = extract_waf_params(html_content)
    if not params:
        logger.error("检测到 WAF 特征但提取动态参数失败！")
        return False

    question, factor, base64_chars, api = params
    logger.info(f"成功提取 WAF 参数: question={question}, factor={factor}, 码表长度={len(base64_chars)}")

    timestamp = int(time.time() * 1000)
    answer = calc_answer(question, factor)
    ua = session.headers.get("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    payload_dict = build_fp_payload(timestamp, answer, ua)

    json_str = json.dumps(payload_dict, separators=(',', ':'))
    encoded_data = encode_custom_base64(json_str.encode('utf-8'), base64_chars)

    api_url = f"https://www.52pojie.cn{api}" if api.startswith("/") else api
    verify_headers = session.headers.copy()
    verify_headers.update({
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': current_url,
        'Origin': 'https://www.52pojie.cn'
    })

    for attempt in range(1, 4):
        try:
            resp = session.post(api_url, data=encoded_data, headers=verify_headers, timeout=timeout)
            logger.info(f"WAF 验证接口响应: 状态码={resp.status_code}, 返回={resp.text}")
            if resp.status_code == 200 and ("ok" in resp.text.lower() or not is_waf_page(resp.text)):
                return True
            else:
                logger.warning(f"WAF 响应异常 (尝试 {attempt}/3): {resp.text[:100]}")
        except Exception as e:
            logger.warning(f"提交 WAF 验证时发生网络错误 (尝试 {attempt}/3): {e}")
            session.close()
        time.sleep(1.5 * attempt)

    logger.error("WAF 验证重试 3 次后均失败！")
    return False
