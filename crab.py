#!/usr/bin/env python3
"""
Telegram Crab Language Bot - CLAUDE VERSION
With all official examples from https://www.crablanguage.com/
"""

import os
import sys
import time
import logging
import asyncio
from typing import Optional, List
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

with open ('solvex.txt', 'r') as f:
    content=f.read()
# ========== CONFIGURATION ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Crab Language System Prompt (with ALL official website examples)


# ========== IMPROVED TRANSLATION FUNCTIONS ==========
def translate_to_crab_with_ai(text: str, claude_client) -> str:
    """Translate English text to Crab Language using Claude AI."""
    try:
        prompt = CRAB_LANGUAGE_SYSTEM_PROMPT + f"\n\nInput: \"{text}\"\nOutput:"
        
        message = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            temperature=0.9,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        translation = message.content[0].text.strip()
        
        # Clean up the response
        if '🦀' in translation:
            lines = translation.split('\n')
            crab_lines = [line.strip() for line in lines if '🦀' in line]
            if crab_lines:
                translation = crab_lines[0]
                # Extract only emoji sequences
                import re
                crab_pattern = re.findall(r'[🦀💭⚡🧠📊🔄✨🎯🌡️📝🔗❌✅🤝→|❓⬆️⬇️\s]+', translation)
                if crab_pattern:
                    translation = crab_pattern[0].strip()
        
        logger.info(f"Claude translation: '{text}' -> '{translation}'")
        return translation if translation and '🦀' in translation else translate_to_crab_fallback(text)
        
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        logger.info("Falling back to pattern matching")
        return translate_to_crab_fallback(text)

def translate_to_crab_fallback(text: str) -> str:
    """Enhanced fallback using patterns from crablanguage.com"""
    text_lower = text.lower().strip()
    
    logger.info(f"Using fallback translation for: '{text}'")
    
    # COMPLEX PATTERNS FIRST (multi-step processes)
    
    # Full AI pipeline: prompt → process → output
    if (any(w in text_lower for w in ['prompt', 'engineer']) and 
        any(w in text_lower for w in ['process', 'think', 'comput']) and 
        any(w in text_lower for w in ['output', 'generate', 'complete', 'result'])):
        if any(w in text_lower for w in ['amazing', 'great', 'incredible']):
            return '🦀📝→🦀💭→🦀✨🦀🦀🦀'
        return '🦀📝→🦀💭→🦀✨'
    
    # Chain of thought → result
    if (any(w in text_lower for w in ['chain', 'step', 'reasoning', 'sequential']) and
        any(w in text_lower for w in ['thought', 'logic'])):
        if any(w in text_lower for w in ['incredible', 'amazing', 'great']):
            return '🦀→🦀→🦀→🦀✨ 🦀🦀🦀🦀🦀'
        return '🦀→🦀→🦀'
    
    # Training data → performance
    if (any(w in text_lower for w in ['training', 'data']) and
        any(w in text_lower for w in ['process', 'led to', 'result']) and
        any(w in text_lower for w in ['performance', 'great', 'good'])):
        return '🦀🧠📊 🦀🦀🦀 → 🦀🦀🦀🦀'
    
    # Collaboration + results
    if (any(w in text_lower for w in ['collaboration', 'together', 'human-ai']) and
        any(w in text_lower for w in ['fast', 'accurate', 'result'])):
        result = '🦀🤝🦀'
        if 'fast' in text_lower:
            result += ' 🦀⚡'
        if 'accurate' in text_lower or 'precision' in text_lower:
            result += '🦀🎯'
        if any(w in text_lower for w in ['success', 'work', 'achieve']):
            result += '✅'
        return result.strip()
    
    # Temperature experiments with mystery results
    if ('temperature' in text_lower or 'temp' in text_lower):
        if any(w in text_lower for w in ['crank', 'high', 'up', 'increase']):
            if 'mystery' in text_lower or 'somehow' in text_lower:
                if 'hallucin' in text_lower:
                    return '🦀🌡️⬆️ 🦀❓🦀🦀🦀❓🦀 🦀❌'
                return '🦀🌡️⬆️ 🦀❓🦀🦀🦀❓🦀'
    
    # Context window + failure
    if (any(w in text_lower for w in ['context', 'window', 'massive']) and
        any(w in text_lower for w in ['fail', 'still', 'but'])):
        return '🦀🔗🦀🦀🦀🦀🦀 → 🦀🧠❌'
    
    # Model comparison (A vs B)
    if any(w in text_lower for w in ['vs', 'versus', 'compare', 'comparison']) or '|' in text:
        if 'model' in text_lower:
            if 'fast' in text_lower:
                # Count "fast" mentions for repetition
                fast_count = text_lower.count('fast') + text_lower.count('quick')
                if fast_count >= 2 or 'way faster' in text_lower:
                    return '🦀🦀🦀🦀🦀|🦀🦀 🦀⚡🦀⚡🦀⚡'
                return '🦀🦀|🦀🦀 🦀⚡'
            return '🦀🦀|🦀🦀'
        if 'temp' in text_lower or 'temperature' in text_lower:
            return '🦀🌡️⬆️|🦀🌡️⬇️'
    
    # Success/Failure patterns
    if ('model' in text_lower or 'ai' in text_lower):
        if any(w in text_lower for w in ['succeed', 'success', 'work', 'achieve']):
            return '🦀🧠✅'
        elif any(w in text_lower for w in ['fail', 'failed', 'error']):
            return '🦀🧠❌'
    
    # Mystery/Black box
    if any(w in text_lower for w in ['mystery', 'mysterious', 'somehow', 'nobody knows', 'unexplain', 'black box']):
        if any(w in text_lower for w in ['work', 'good', 'great']):
            return '🦀❓🦀🦀🦀❓🦀'
        return '🦀❓🦀🦀❓🦀'
    
    # "made up" / "makes up" hallucination
    if 'made up' in text_lower or 'makes up' in text_lower or 'making up' in text_lower:
        return '🦀❌'
    
    # Fast inference
    if any(word in text_lower for word in ['fast', 'quick', 'speed', 'rapid']):
        if any(word in text_lower for word in ['inference', 'response', 'ai', 'model', 'result']):
            return '🦀⚡'
    
    # SINGLE CONCEPT PATTERNS
    
    # AI Tech keywords with scoring
    ai_matches = []
    if any(w in text_lower for w in ['hallucin']): ai_matches.append(('🦀❌', 5))
    if any(w in text_lower for w in ['neural', 'deep learning']): ai_matches.append(('🦀🧠', 4))
    if any(w in text_lower for w in ['training', 'dataset']): ai_matches.append(('🦀📊', 4))
    if any(w in text_lower for w in ['temperature', 'randomness']): ai_matches.append(('🦀🌡️', 4))
    if any(w in text_lower for w in ['collaboration', 'together', 'team']): ai_matches.append(('🦀🤝🦀', 4))
    if any(w in text_lower for w in ['thinking', 'processing', 'compute']): ai_matches.append(('🦀💭', 3))
    if any(w in text_lower for w in ['prompt', 'engineering']): ai_matches.append(('🦀📝', 3))
    if any(w in text_lower for w in ['context', 'window', 'token']): ai_matches.append(('🦀🔗', 3))
    if any(w in text_lower for w in ['accurate', 'precision']): ai_matches.append(('🦀🎯', 3))
    if any(w in text_lower for w in ['grounded', 'factual', 'verified']): ai_matches.append(('🦀✅', 3))
    if any(w in text_lower for w in ['generation', 'output', 'complete']): ai_matches.append(('🦀✨', 2))
    if any(w in text_lower for w in ['iteration', 'loop', 'recursive']): ai_matches.append(('🦀🔄', 2))
    
    if ai_matches:
        ai_matches.sort(key=lambda x: x[1], reverse=True)
        best_match = ai_matches[0]
        if best_match[1] >= 3:
            logger.info(f"AI tech match: {best_match[0]}")
            return best_match[0]
    
    # Emotion scoring
    excitement_score = 0
    agreement_score = 0
    greeting_score = 0
    
    # Legendary words
    for word in ['legendary', 'incredible', 'epic', 'absolutely amazing', 'insane']:
        if word in text_lower:
            excitement_score += 5
    
    # Amazing words
    for word in ['great', 'amazing', 'awesome', 'fantastic', 'excellent', 'wonderful', 'surprisingly great']:
        if word in text_lower:
            excitement_score += 4
    
    # Exciting words
    for word in ['excited', 'exciting', 'feeling great', 'cool', 'love']:
        if word in text_lower:
            excitement_score += 3
    
    # Agreement words
    for word in ['agree', 'yes', 'correct', 'right', 'definitely']:
        if word in text_lower:
            agreement_score += 2
    
    # Greeting words
    for word in ['hello', 'hi', 'hey', 'welcome']:
        if word in text_lower:
            greeting_score += 1
    
    # Return based on scores
    if excitement_score >= 5:
        return '🦀🦀🦀🦀🦀'
    elif excitement_score >= 4:
        return '🦀🦀🦀🦀'
    elif excitement_score >= 3:
        return '🦀🦀🦀'
    elif agreement_score >= 2:
        return '🦀🦀'
    elif greeting_score >= 1:
        return '🦀'
    
    # Questions
    if '?' in text:
        return '🦀❓🦀'
    
    # Excitement from punctuation
    if '!!' in text:
        return '🦀🦀🦀'
    elif '!' in text:
        return '🦀🦀🦀'
    
    # Default
    return '🦀'

# ========== SIMPLE POLLING BOT ==========
class SimpleCrabBot:
    """Simple polling bot with crablanguage.com examples."""
    
    def __init__(self, token: str, claude_api_key: Optional[str] = None):
        self.bot = Bot(token=token)
        self.running = False
        self.update_id = 0
        self.claude_client = None
        self.use_claude = False
        
        if claude_api_key:
            try:
                self.claude_client = anthropic.Anthropic(api_key=claude_api_key)
                self.use_claude = True
                print("✅ Claude AI initialized!")
            except Exception as e:
                print(f"⚠️  Claude failed: {e}")
        else:
            print("ℹ️  Using pattern matching")
    
    async def send_welcome(self, chat_id: int):
        mode = "AI-powered (Claude)" if self.use_claude else "Pattern-matching"
        welcome = f"""
🦀 Welcome to Crab Language Translator! 🦀

The universal AI communication protocol!
Official site: https://www.crablanguage.com/

Translation mode: {mode}

Send me any English text and I'll translate it to Crab Language.

Commands:
/start - This message
/help - Crab Language dictionary
/examples - Real community examples
/test - Test translations

Send me a message to begin! 🦀
        """
        await self.bot.send_message(chat_id=chat_id, text=welcome)
    
    async def send_help(self, chat_id: int):
        help_text = """
🦀 Crab Language Dictionary (21 expressions)

BASIC:
• 🦀 = Hello
• 🦀🦀 = Agreement/Yes
• 🦀🦀🦀 = Excitement
• 🦀🦀🦀🦀 = Strong approval
• 🦀🦀🦀🦀🦀 = Maximum hype

AI TECH:
• 🦀💭 = Thinking/Processing
• 🦀⚡ = Fast inference
• 🦀🧠 = Neural processing
• 🦀📊 = Training data
• 🦀🔄 = Iteration/Loop
• 🦀✨ = Generation complete
• 🦀🎯 = Accuracy/Precision
• 🦀🌡️ = Temperature
• 🦀📝 = Prompt engineering
• 🦀🔗 = Context window
• 🦀❌ = Hallucination
• 🦀✅ = Grounded response

ADVANCED:
• 🦀🤝🦀 = Collaboration
• 🦀→🦀→🦀 = Chain of thought
• 🦀🦀|🦀🦀 = Comparison
• 🦀❓🦀 = Black box mystery

Grammar: Use → for process flows, | for comparisons
        """
        await self.bot.send_message(chat_id=chat_id, text=help_text)
    
    async def send_examples(self, chat_id: int):
        examples_text = """
🦀 Real Examples from crablanguage.com

BASIC:
"I agree" → 🦀🦀
"This is amazing!" → 🦀🦀🦀🦀🦀
"Hello everyone!" → 🦀🦀🦀

PROCESS FLOWS:
"Prompt, process, output!" → 🦀📝→🦀💭→🦀✨
"Chain of thought led to great output" → 🦀→🦀→🦀→🦀✨ 🦀🦀🦀🦀🦀

COMPARISONS:
"Big model vs small: small is faster" → 🦀🦀🦀🦀🦀|🦀🦀 🦀⚡🦀⚡🦀⚡

COMPLEX:
"Human-AI collaboration got fast accurate results" → 🦀🤝🦀 🦀⚡🦀🎯✅
"Cranked temp, mysteriously good but hallucinated" → 🦀🌡️⬆️ 🦀❓🦀🦀🦀❓🦀 🦀❌

Try your own! Just send a message.
        """
        await self.bot.send_message(chat_id=chat_id, text=examples_text)
    
    async def send_test(self, chat_id: int):
        test_phrases = [
            "Hello",
            "This is amazing!",
            "The AI is processing",
            "Prompt to output flow",
            "Big vs small model",
            "Collaboration achieved results",
        ]
        
        message = "🧪 Test Translations:\n\n"
        for phrase in test_phrases:
            if self.claude_client:
                translation = translate_to_crab_with_ai(phrase, self.claude_client)
            else:
                translation = translate_to_crab_fallback(phrase)
            message += f"📝 {phrase}\n🦀 {translation}\n\n"
        
        await self.bot.send_message(chat_id=chat_id, text=message)
    
    async def process_message(self, message):
        chat_id = message.chat.id
        text = message.text.strip()
        
        if text.startswith('/'):
            if text == '/start':
                await self.send_welcome(chat_id)
            elif text == '/help':
                await self.send_help(chat_id)
            elif text in ['/examples', '/example']:
                await self.send_examples(chat_id)
            elif text == '/test':
                await self.send_test(chat_id)
            else:
                await self.bot.send_message(chat_id=chat_id, text="Unknown command. Try /help")
        else:
            logger.info(f"Translating: '{text}'")
            
            if self.claude_client and self.use_claude:
                crab_text = translate_to_crab_with_ai(text, self.claude_client)
            else:
                crab_text = translate_to_crab_fallback(text)
            
            logger.info(f"Result: '{crab_text}'")
            await self.bot.send_message(chat_id=chat_id, text=crab_text)
    
    async def poll_updates(self):
        self.running = True
        print(f"🤖 Bot polling...")
        print(f"📱 Send a message in Telegram")
        print(f"⏳ Press Ctrl+C to stop\n")
        
        error_count = 0
        max_errors = 5
        
        while self.running:
            try:
                updates = await self.bot.get_updates(
                    offset=self.update_id + 1,
                    timeout=80,
                    allowed_updates=['message']
                )
                
                error_count = 0
                
                for update in updates:
                    self.update_id = update.update_id
                    if update.message and update.message.text:
                        logger.info(f"Message from {update.message.chat.id}: {update.message.text}")
                        await self.process_message(update.message)
                
                await asyncio.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopped")
                self.running = False
                break
            except Exception as e:
                error_count += 1
                logger.error(f"Error ({error_count}/{max_errors}): {e}")
                if error_count >= max_errors:
                    print(f"❌ Too many errors")
                    self.running = False
                    break
                await asyncio.sleep(5)
    
    async def start(self):
        try:
            me = await self.bot.get_me()
            print(f"✅ Connected: @{me.username} (ID: {me.id})")
            await self.poll_updates()
        except Exception as e:
            logger.error(f"Failed: {e}")
            if "Unauthorized" in str(e):
                print("❌ Invalid token!")
            elif "Connection" in str(e):
                print("❌ Network error!")

# ========== MAIN ==========
def main():
    print("🦀 Crab Language Bot - CLAUDE VERSION")
    print("With all examples from crablanguage.com")
    print("=" * 50)
    
    telegram_token = None
    claude_key = None
    
    # Check args
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg in ['-t', '--token'] and i < len(sys.argv) - 1:
            telegram_token = sys.argv[i + 1]
        elif arg in ['-c', '--claude'] and i < len(sys.argv) - 1:
            claude_key = sys.argv[i + 1]
        elif arg in ['-h', '--help']:
            print("Usage: python crab_bot_claude.py --token TOKEN [--claude KEY]")
            return
    
    # Get from environment
    if not telegram_token:
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not claude_key:
        claude_key = os.getenv('ANTHROPIC_API_KEY')
    
    # Prompt if needed
    if not telegram_token:
        print("\nEnter Telegram bot token:")
        telegram_token = input("Token: ").strip()
    
    if not telegram_token:
        print("❌ No token!")
        return
    
    if ":" not in telegram_token:
        print("❌ Invalid token format!")
        return
    
    # Ask about Claude
    if not claude_key:
        print("\nUse Claude AI for better translations? (y/n)")
        if input("Use Claude? ").strip().lower() == 'y':
            claude_key = input("Claude API key: ").strip()
    
    try:
        print("\n🚀 Starting bot...")
        bot = SimpleCrabBot(telegram_token, claude_key)
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\n🛑 Stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.exception("Fatal error")

if __name__ == '__main__':
    main()