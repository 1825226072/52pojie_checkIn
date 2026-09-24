# -*- coding: utf-8 -*-
"""
推送通知模块（精简版）
仅保留：
1. 企业微信群机器人 (WECOM_WEBHOOK)
2. PushPlus (PUSHPLUS_TOKEN)
3. GitHub Actions Job Summary 渲染
"""

import os
import requests
import logging

logger = logging.getLogger("Notify")

DEFAULT_WECOM_WEBHOOK = ""


def send_wecom(webhook: str, title: str, content: str):
    """企业微信群机器人推送 (严格遵循 msgtype: text 纯文本格式)."""
    if content.strip().startswith("🔔") or content.strip().startswith("【"):
        text_content = content.strip()
    else:
        text_content = (
            f"【{title}】\n"
            f"--------------------------------\n"
            f"{content}\n"
            f"--------------------------------"
        )
    payload = {
        "msgtype": "text",
        "text": {
            "content": text_content
        }
    }

    try:
        r = requests.post(webhook, json=payload, timeout=10)
        logger.info(f"企业微信 推送响应: {r.text}")
    except Exception as e:
        logger.error(f"企业微信 推送异常: {e}")


def send_pushplus(token: str, title: str, content: str):
    """PushPlus 微信模板消息推送."""
    url = "http://www.pushplus.plus/send"
    data = {
        "token": token,
        "title": title,
        "content": content.replace("\n", "<br>"),
        "template": "html"
    }
    try:
        r = requests.post(url, json=data, timeout=10)
        logger.info(f"PushPlus 推送响应: {r.text}")
    except Exception as e:
        logger.error(f"PushPlus 推送异常: {e}")


def write_github_summary(title: str, content: str):
    """在 GitHub Actions 环境中生成 Job Summary 报告."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file and os.path.exists(os.path.dirname(summary_file)):
        try:
            markdown = f"## {title}\n\n```text\n{content}\n```\n"
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write(markdown)
        except Exception as e:
            logger.debug(f"写入 GITHUB_STEP_SUMMARY 失败: {e}")


def send(title: str, content: str):
    """统一通知分发入口."""
    logger.info(f"--- 准备推送通知 ---\n标题: {title}\n内容:\n{content}\n----------------")

    # 1. 写入 Actions Summary
    write_github_summary(title, content)

    pushed = False

    # 2. 企业微信机器人 (优先环境变量，回退到默认机器人)
    wecom_webhook = os.environ.get("WECOM_WEBHOOK") or DEFAULT_WECOM_WEBHOOK
    if wecom_webhook:
        send_wecom(wecom_webhook, title, content)
        pushed = True

    # 3. PushPlus 推送
    pushplus_token = os.environ.get("PUSHPLUS_TOKEN")
    if pushplus_token:
        send_pushplus(pushplus_token, title, content)
        pushed = True

    if not pushed:
        logger.info("未配置任何外部推送 Token，跳过发送。")
