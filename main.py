import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
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

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_data = context.user_data

    # --- 菜单展示阶段 ---
    if data == "v1":
        kb = [[InlineKeyboardButton("4", c="m4"), InlineKeyboardButton("5", c="m5")],
              [InlineKeyboardButton("6", c="m6"), InlineKeyboardButton("7", c="m7")]]
        await query.edit_message_text("问题：2 + 3 = ？ 请选择正确结果：", reply_markup=InlineKeyboardMarkup(kb))
        user_data['stage'] = 'math'
    elif data == "v2":
        kb = [[InlineKeyboardButton("红色", c="c_red"), InlineKeyboardButton("蓝色", c="c_blue")],
              [InlineKeyboardButton("绿色", c="c_green"), InlineKeyboardButton("黄色", c="c_yellow")]]
        await query.edit_message_text("问题：苹果是什么颜色？", reply_markup=InlineKeyboardMarkup(kb))
        user_data['stage'] = 'color'
    elif data == "v3":
        kb = [[InlineKeyboardButton("对", c="l_true"), InlineKeyboardButton("错", c="l_false")]]
        await query.edit_message_text("问题：1+1=3，对不对？", reply_markup=InlineKeyboardMarkup(kb))
        user_data['stage'] = 'logic'
    elif data == "v4":
        kb = [[InlineKeyboardButton("A", c="seq_a"), InlineKeyboardButton("B", c="seq_b"), InlineKeyboardButton("C", c="seq_c")]]
        await query.edit_message_text("步骤 1/2：请先点击按钮 C", reply_markup=InlineKeyboardMarkup(kb))
        user_data['stage'] = 'seq'
        user_data['seq_step'] = 1
    elif data == "v5":
        kb = [[InlineKeyboardButton("苹果", c="r_apple"), InlineKeyboardButton("香蕉", c="r_banana")],
              [InlineKeyboardButton("黄瓜", c="r_cucumber"), InlineKeyboardButton("橘子", c="r_orange")]]
        await query.edit_message_text("问题：以下哪一项不属于水果？", reply_markup=InlineKeyboardMarkup(kb))
        user_data['stage'] = 'reverse'

    # --- 结果验证阶段 ---
    elif user_data.get('stage') == 'math':
        if data == "m5":
            await query.edit_message_text("✅ 验证通过！你已成功解锁。")
        else:
            await query.edit_message_text("❌ 验证失败，请发送 /start 重新尝试。")
    
    elif user_data.get('stage') == 'color':
        if data == "c_red":
            await query.edit_message_text("✅ 验证通过！你已成功解锁。")
        else:
            await query.edit_message_text("❌ 验证失败，请发送 /start 重新尝试。")
            
    elif user_data.get('stage') == 'logic':
        if data == "l_false":
            await query.edit_message_text("✅ 验证通过！你已成功解锁。")
        else:
            await query.edit_message_text("❌ 验证失败，请发送 /start 重新尝试。")
            
    elif user_data.get('stage') == 'seq':
        step = user_data.get('seq_step')
        if step == 1 and data == "seq_c":
            user_data['seq_step'] = 2
            kb = [[InlineKeyboardButton("A", c="seq_a"), InlineKeyboardButton("B", c="seq_b"), InlineKeyboardButton("C", c="seq_c")]]
            await query.edit_message_text("步骤 2/2：现在请点击按钮 A", reply_markup=InlineKeyboardMarkup(kb))
        elif step == 2 and data == "seq_a":
            await query.edit_message_text("✅ 验证通过！你已成功解锁。")
        else:
            await query.edit_message_text("❌ 顺序错误，验证失败。请发送 /start 重新尝试。")
            
    elif user_data.get('stage') == 'reverse':
        if data == "r_cucumber":
            await query.edit_message_text("✅ 验证通过！你已成功解锁。")
        else:
            await query.edit_message_text("❌ 验证失败，请发送 /start 重新尝试。")
    else:
        await query.edit_message_text("⛔ 页面已过期，请发送 /start 重新开始。")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()
