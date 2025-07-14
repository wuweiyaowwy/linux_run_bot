# -*- coding: utf-8 -*- 
import logging
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# 你的 Bot Token（从 BotFather 获取） 
BOT_TOKEN = 'XXX'

# 你的 Telegram 用户 ID（从 @userinfobot 获取） 
AUTHORIZED_USER_ID = XXXX

# 设置日志记录，用于调试
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# /start 命令：验证身份 + 显示用户 ID 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    user_id = update.effective_user.id 
    if user_id == AUTHORIZED_USER_ID: 
        await update.message.reply_text(f"✅ Bot 已启动。\n你的 Telegram ID 是：{user_id}") 
    else: 
        await update.message.reply_text(f"❌ 未授权用户，无法执行该命令！") 
    logger.info(f"用户连接：{user_id}")  # 使用日志记录用户 ID

# 执行用户发送的命令
async def execute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ 你没有权限执行此操作。")
        return

    command = update.message.text.strip()  # 获取用户发送的文本
    if command.startswith("/start"):  # 忽略 /start 命令
        return

    if not command:
        await update.message.reply_text("⚠️ 请输入要执行的命令")
        return

    logger.info(f"正在执行命令：{command}")  # 使用日志记录正在执行的命令
    try:
        # 执行命令并获取输出
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=60)
        
        # 处理编码问题，使用 'ignore' 忽略无法解码的字符，或者用 'replace' 替代
        decoded_output = output.decode(errors='ignore')  # 你也可以用 'replace' 替代
        await update.message.reply_text(f"✅ 执行成功:\n{decoded_output[:4000]}")
    except subprocess.CalledProcessError as e:
        # 捕捉到命令执行错误
        logger.error(f"执行命令失败: {e}")
        await update.message.reply_text(f"❌ 命令出错:\n{e.output.decode(errors='ignore')[:4000]}")
    except Exception as e:
        # 捕捉到其他异常
        logger.error(f"执行异常: {str(e)}")
        await update.message.reply_text(f"❌ 执行异常: {str(e)}")

# 启动 Bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# 添加命令处理器
app.add_handler(CommandHandler("start", start))  # 添加 start 命令处理

# 监听所有文本消息并执行命令
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, execute_command))  # 监听所有文本消息并执行命令

if __name__ == '__main__':
    logger.info("🚀 Bot 正在监听中...")
    app.run_polling(timeout=60, allowed_updates=["message"])  # 启动轮询
