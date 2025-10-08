import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# Conversation states
PHQ9_Q1, PHQ9_Q2, PHQ9_Q3, PHQ9_Q4, PHQ9_Q5, PHQ9_Q6, PHQ9_Q7, PHQ9_Q8, PHQ9_Q9 = range(1, 10)
GAD7_Q1, GAD7_Q2, GAD7_Q3, GAD7_Q4, GAD7_Q5, GAD7_Q6, GAD7_Q7 = range(10, 17)

# Crisis keywords
CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end my life', 'want to die',
    'better off dead', 'end it all', 'suicidal', 'no reason to live',
    "can't go on", 'self harm', 'hurt myself'
]

# Crisis resources
CRISIS_RESOURCES = """
🚨 **IMMEDIATE HELP AVAILABLE** 🚨

**India:**
• AASRA: 91-9820466726 (24/7)
• iCall: 9152987821 (Mon-Sat, 8am-10pm)
• Vandrevala Foundation: 1860-2662-345 (24/7)

**International:**
• Crisis Text Line: Text HOME to 741741
• Befrienders Worldwide: befrienders.org

**YOU ARE NOT ALONE. YOUR LIFE MATTERS.**
"""

# PHQ-9 & GAD-7 Questions
PHQ9_QUESTIONS = [
    "Over the last 2 weeks, how often have you been bothered by:\n\n**Little interest or pleasure in doing things?**",
    "**Feeling down, depressed, or hopeless?**",
    "**Trouble falling or staying asleep, or sleeping too much?**",
    "**Feeling tired or having little energy?**",
    "**Poor appetite or overeating?**",
    "**Feeling bad about yourself?**",
    "**Trouble concentrating?**",
    "**Moving or speaking slowly, or being restless?**",
    "**Thoughts that you would be better off dead?**",
]

GAD7_QUESTIONS = [
    "Over the last 2 weeks, how often have you been bothered by:\n\n**Feeling nervous, anxious, or on edge?**",
    "**Not being able to stop or control worrying?**",
    "**Worrying too much about different things?**",
    "**Trouble relaxing?**",
    "**Being so restless that it's hard to sit still?**",
    "**Becoming easily annoyed or irritable?**",
    "**Feeling afraid, as if something awful might happen?**",
]

def get_answer_keyboard():
    keyboard = [
        [InlineKeyboardButton("0 - Not at all", callback_data="0")],
        [InlineKeyboardButton("1 - Several days", callback_data="1")],
        [InlineKeyboardButton("2 - More than half the days", callback_data="2")],
        [InlineKeyboardButton("3 - Nearly every day", callback_data="3")],
    ]
    return InlineKeyboardMarkup(keyboard)

def detect_crisis(message: str) -> bool:
    return any(keyword in message.lower() for keyword in CRISIS_KEYWORDS)

def get_response(message: str) -> str:
    msg = message.lower()
    
    if any(word in msg for word in ['anxious', 'anxiety', 'worried', 'panic']):
        return ("Anxiety can feel overwhelming. Try this grounding:\n\n"
                "• 5 things you see\n• 4 things you touch\n• 3 things you hear\n"
                "• 2 things you smell\n• 1 thing you taste\n\n"
                "What's triggering the anxiety?")
    
    if any(word in msg for word in ['depressed', 'depression', 'sad', 'hopeless']):
        return ("I'm sorry you're feeling this way. Depression makes everything heavier.\n\n"
                "Small steps count. Have you talked to a mental health professional?")
    
    if any(word in msg for word in ['stressed', 'overwhelmed', 'too much']):
        return ("Feeling overwhelmed shows you're carrying a lot.\n\n"
                "Let's break it down: What's the ONE thing causing most stress?")
    
    if any(word in msg for word in ['sleep', 'insomnia', 'tired', 'exhausted']):
        return ("Sleep issues affect everything. Try:\n"
                "• Consistent schedule\n• No screens 1hr before bed\n"
                "• Cool, dark room\n\nHow long has sleep been difficult?")
    
    if any(word in msg for word in ['lonely', 'alone', 'isolated']):
        return ("Loneliness is painful. Connection can start small:\n"
                "• This conversation\n• Message someone\n• Online communities\n\n"
                "What connections feel meaningful to you?")
    
    if any(word in msg for word in ['happy', 'good', 'better', 'great']):
        return "That's wonderful! 😊 What contributed to feeling this way?"
    
    responses = [
        "I'm here to listen. Tell me more.",
        "That sounds important. How are you feeling about this?",
        "Thank you for sharing. What's been on your mind?",
        "I hear you. What's the hardest part?",
    ]
    import random
    return random.choice(responses)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱 **Welcome to Mental Wellbeing Support**\n\n"
        "I'm here to support you.\n\n"
        "⚠️ **Important:** I'm NOT a therapist. I'm an AI support tool.\n\n"
        "**Commands:**\n"
        "/checkdepression - PHQ-9 screening\n"
        "/checkanxiety - GAD-7 screening\n"
        "/breathe - Breathing exercise\n"
        "/ground - Grounding technique\n"
        "/resources - Crisis helplines\n"
        "/help - All commands\n\n"
        "Or just chat with me! How are you feeling?",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧭 **Available Commands:**\n\n"
        "/start - Welcome\n"
        "/checkdepression - PHQ-9 screening\n"
        "/checkanxiety - GAD-7 screening\n"
        "/breathe - Breathing exercise\n"
        "/ground - Grounding technique\n"
        "/journal - Journaling prompts\n"
        "/resources - Crisis helplines\n\n"
        "You can also just chat with me! 💬",
        parse_mode='Markdown'
    )

async def breathe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌬️ **Box Breathing**\n\n"
        "1️⃣ Breathe IN... 1, 2, 3, 4\n"
        "2️⃣ HOLD... 1, 2, 3, 4\n"
        "3️⃣ Breathe OUT... 1, 2, 3, 4\n"
        "4️⃣ HOLD... 1, 2, 3, 4\n\n"
        "Repeat 4 times. How do you feel?",
        parse_mode='Markdown'
    )

async def ground(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧘 **5-4-3-2-1 Grounding**\n\n"
        "Look around and notice:\n\n"
        "👁️ 5 things you SEE\n"
        "✋ 4 things you TOUCH\n"
        "👂 3 things you HEAR\n"
        "👃 2 things you SMELL\n"
        "👅 1 thing you TASTE\n\n"
        "Take your time.",
        parse_mode='Markdown'
    )

async def journal_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompts = [
        "What am I feeling right now?",
        "What triggered this feeling?",
        "What would I tell a friend feeling this way?",
        "What's one small thing I can control?",
        "What am I grateful for today?",
    ]
    import random
    await update.message.reply_text(
        f"📝 **Journaling Prompt**\n\n*{random.choice(prompts)}*\n\n"
        "Take a moment to reflect.",
        parse_mode='Markdown'
    )

async def resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{CRISIS_RESOURCES}\n\nAsking for help is strength. 💚",
        parse_mode='Markdown'
    )

# PHQ-9 handlers
async def start_phq9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 **Depression Screening (PHQ-9)**\n\n"
        "⚠️ This is NOT a diagnosis - it's a screening tool.\n\n"
        "Ready?",
        parse_mode='Markdown'
    )
    context.user_data['phq9_scores'] = []
    await update.message.reply_text(
        PHQ9_QUESTIONS[0],
        reply_markup=get_answer_keyboard(),
        parse_mode='Markdown'
    )
    return PHQ9_Q1

async def phq9_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, q_num: int):
    query = update.callback_query
    await query.answer()
    
    context.user_data['phq9_scores'].append(int(query.data))
    
    if q_num < len(PHQ9_QUESTIONS):
        await query.edit_message_text(
            PHQ9_QUESTIONS[q_num],
            reply_markup=get_answer_keyboard(),
            parse_mode='Markdown'
        )
        return q_num + PHQ9_Q1
    else:
        score = sum(context.user_data['phq9_scores'])
        
        if score <= 4:
            msg = "Minimal symptoms. Keep up self-care! ✅"
        elif score <= 9:
            msg = "Mild symptoms. Consider self-care and talking to someone."
        elif score <= 14:
            msg = "Moderate symptoms. Consider speaking with a mental health professional."
        elif score <= 19:
            msg = "Moderately severe. Please reach out to a professional soon."
        else:
            msg = f"Severe symptoms. Please seek help immediately.\n\n{CRISIS_RESOURCES}"
        
        await query.edit_message_text(
            f"📊 **PHQ-9 Results**\n\nScore: **{score}/27**\n\n{msg}\n\n"
            "💙 This is a screening, not a diagnosis.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

# GAD-7 handlers
async def start_gad7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 **Anxiety Screening (GAD-7)**\n\n"
        "⚠️ This is NOT a diagnosis.\n\nReady?",
        parse_mode='Markdown'
    )
    context.user_data['gad7_scores'] = []
    await update.message.reply_text(
        GAD7_QUESTIONS[0],
        reply_markup=get_answer_keyboard(),
        parse_mode='Markdown'
    )
    return GAD7_Q1

async def gad7_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, q_num: int):
    query = update.callback_query
    await query.answer()
    
    context.user_data['gad7_scores'].append(int(query.data))
    
    if q_num < len(GAD7_QUESTIONS):
        await query.edit_message_text(
            GAD7_QUESTIONS[q_num],
            reply_markup=get_answer_keyboard(),
            parse_mode='Markdown'
        )
        return q_num + GAD7_Q1
    else:
        score = sum(context.user_data['gad7_scores'])
        
        if score <= 4:
            msg = "Minimal anxiety. Great! ✅"
        elif score <= 9:
            msg = "Mild anxiety. Consider stress management."
        elif score <= 14:
            msg = "Moderate anxiety. Consider professional support."
        else:
            msg = "Severe anxiety. Please reach out to a professional."
        
        await query.edit_message_text(
            f"📊 **GAD-7 Results**\n\nScore: **{score}/21**\n\n{msg}\n\n"
            "💙 This is a screening, not a diagnosis.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    
    if detect_crisis(msg):
        await update.message.reply_text(
            f"🚨 **I'm very concerned.**\n\n{CRISIS_RESOURCES}\n\n"
            "Please reach out for help. Your life matters.",
            parse_mode='Markdown'
        )
        return
    
    await update.message.reply_text(get_response(msg))

def main():
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN found!")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    # PHQ-9
    phq9 = ConversationHandler(
        entry_points=[CommandHandler('checkdepression', start_phq9)],
        states={
            PHQ9_Q1: [CallbackQueryHandler(lambda u, c: phq9_answer(u, c, 0))],
            PHQ9_Q2: [CallbackQueryHandler(lambda u, c: phq9_answer(u, c, 1))],
            PHQ9_Q3: [CallbackQueryHandler(lambda u, c: phq9_answer(u, c, 2))],
            PHQ9_Q4: [CallbackQueryHandler(lambda u, c: phq9_answer(u, c, 3))],
            PHQ9_Q5: [CallbackQueryHandler(lambda u, c: phq9_answer(u, c, 4))],
            PHQ9_Q6: [CallbackQueryHandler(lambda u, c: phq9_answer(u, c, 5))],
            PHQ9_Q7: [CallbackQueryHandler(lambda u, c: phq9_answer(u, c, 6))],
            PHQ9_Q8: [CallbackQueryHandler(lambda u, c: phq9_answer(u, c, 7))],
            PHQ9_Q9: [CallbackQueryHandler(lambda u, c: phq9_answer(u, c, 8))],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    
    # GAD-7
    gad7 = ConversationHandler(
        entry_points=[CommandHandler('checkanxiety', start_gad7)],
        states={
            GAD7_Q1: [CallbackQueryHandler(lambda u, c: gad7_answer(u, c, 0))],
            GAD7_Q2: [CallbackQueryHandler(lambda u, c: gad7_answer(u, c, 1))],
            GAD7_Q3: [CallbackQueryHandler(lambda u, c: gad7_answer(u, c, 2))],
            GAD7_Q4: [CallbackQueryHandler(lambda u, c: gad7_answer(u, c, 3))],
            GAD7_Q5: [CallbackQueryHandler(lambda u, c: gad7_answer(u, c, 4))],
            GAD7_Q6: [CallbackQueryHandler(lambda u, c: gad7_answer(u, c, 5))],
            GAD7_Q7: [CallbackQueryHandler(lambda u, c: gad7_answer(u, c, 6))],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("breathe", breathe))
    app.add_handler(CommandHandler("ground", ground))
    app.add_handler(CommandHandler("journal", journal_prompts))
    app.add_handler(CommandHandler("resources", resources))
    app.add_handler(phq9)
    app.add_handler(gad7)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🤖 Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
