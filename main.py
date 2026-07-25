import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("数学验证", callback_data="v1")],
        [InlineKeyboardButton("颜色验证", callback_data="v2")],
        [InlineKeyboardButton("逻辑判断", callback_data="v3")],
        [InlineKeyboardButton("顺序点击", callback_data="v4")],
        [InlineKeyboardButton("反向识别", callback_data="v5")]
    ]
    await update.message.reply_text(
        "请选择一种人机验证方式：",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # 1. 数学验证
    if query.data == "v1":
        kb = [[InlineKeyboardButton("4", c="m4"), InlineKeyboardButton("5", c="m5")],
              [InlineKeyboardButton("6", c="m6"), InlineKeyboardButton("7", c="m7")]]
        await query.edit_message_text("问题：2 + 3 = ？ 请选择正确结果：", reply_markup=InlineKeyboardMarkup(kb))
        context.user_data['current_v'] = 'm'

    # 2. 颜色验证
    elif query.data == "v2":
        kb = [[InlineKeyboardButton("红色", c="c_red"), InlineKeyboardButton("蓝色", c="c_blue")],
              [InlineKeyboardButton("绿色", c="c_green"), InlineKeyboardButton("黄色", c="c_yellow")]]
        await query.edit_message_text("问题：苹果是什么颜色？", reply_markup=InlineKeyboardMarkup(kb))
        context.user_data['current_v'] = 'c'

    # 3. 逻辑判断
    elif query.data == "v3":
        kb = [[InlineKeyboardButton("对", c="l_true"), InlineKeyboardButton("错", c="l_false")]]
        await query.edit_message_text("问题：1+1=3，对不对？", reply_markup=InlineKeyboardMarkup(kb))
        context.user_data['current_v'] = 'l'

    # 4. 顺序点击
    elif query.data == "v4":
        kb = [[InlineKeyboardButton("A", c="seq_a"), InlineKeyboardButton("B", c="seq_b"), InlineKeyboardButton("C", c="seq_c")]]
        await query.edit_message_text("步骤 1/2：请先点击按钮 C", reply_markup=InlineKeyboardMarkup(kb))
        context.user_data['current_v'] = 'seq'
        context.user_data['seq_step'] = 1

    # 5. 反向识别
    elif query.data == "v5":
        kb = [[InlineKeyboardButton("苹果", c="r_apple"), InlineKeyboardButton("香蕉", c="r_banana")],
              [InlineKeyboardButton("黄瓜", c="r_cucumber"), InlineKeyboardButton("橘子", c="r_orange")]]
        await query.edit_message_text("问题：以下哪一项不属于水果？", reply_markup=InlineKeyboardMarkup(kb))
        context.user_data['current_v'] = 'r'

async def verification_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    current_v = context.user_data.get('current_v')
    if not current_v:
        await query.edit_message_text("⛔ 验证已过期，请发送 /start 重新开始。")
        return

    # 结果判定
    if current_v == 'm' and query.data == "m5":
        await query.edit_message_text("✅ 验证通过！你已成功解锁。")
    elif current_v == 'c' and query.data == "c_red":
        await query.edit_message_text("✅ 验证通过！你已成功解锁。")
    elif current_v == 'l' and query.data == "l_false":
        await query.edit_message_text("✅ 验证通过！你已成功解锁。")
    elif current_v == 'r' and query.data == "r_cucumber":
        await query.edit_message_text("✅ 验证通过！你已成功解锁。")
    elif current_v == 'seq':
        step = context.user_data.get('seq_step', 1)
        if step == 1 and query.data == "seq_c":
            context.user_data['seq_step'] = 2
            kb = [[InlineKeyboardButton("A", c="seq_a"), InlineKeyboardButton("B", c="seq_b"), InlineKeyboardButton("C", c="seq_c")]]
            await query.edit_message_text("步骤 2/2：现在请点击按钮 A", reply_markup=InlineKeyboardMarkup(kb))
        elif step == 2 and query.data == "seq_a":
            await query.edit_message_text("✅ 验证通过！你已成功解锁。")
        else:
            await query.edit_message_text("❌ 顺序错误，验证失败。请发送 /start 重新尝试。")
    else:
        await query.edit_message_text("❌ 验证失败，请发送 /start 重新尝试。")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^v[1-5]$"))
    app.add_handler(CallbackQueryHandler(verification_result))
    print("Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()
