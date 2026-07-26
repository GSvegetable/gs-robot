import os
from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# 这里是你的黑屏网页地址。等会按我下面的步骤部署好 GitHub Pages 后，把地址填到这里。
WEB_APP_URL = "https://gsvegetable.github.io/gs-robot/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("机器人已启动！请看看左下角的紫色菜单按钮。")

async def post_init(application: Application):
    # 核心代码：把左侧菜单按钮变成一个紫色的“迷你小程序”入口
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="打开黑屏程序",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
    )

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()
