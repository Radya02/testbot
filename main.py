import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Initialize bot with your token
bot = telebot.TeleBot('8066332445:AAFOETRZ7-CiF6h8aK4IfdnJJMfQ0Q1F9Bc')

def get_ton_price():
    """Fetch TON price from CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'the-open-network',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'the-open-network' in data:
            ton_data = data['the-open-network']
            price = ton_data.get('usd', 'N/A')
            change_24h = ton_data.get('usd_24h_change', 'N/A')
            last_updated = ton_data.get('last_updated_at', 'N/A')
            
            return {
                'price': price,
                'change_24h': change_24h,
                'last_updated': last_updated
            }
        else:
            return None
            
    except Exception as e:
        print(f"Error fetching TON price: {e}")
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handle start and help commands"""
    welcome_text = """
🤖 *TON Price Bot*

Available commands:
/price - Get current TON price
/start - Show this help message

You can also just send "price" or "ton price" to get the current price.
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['price'])
def send_price(message):
    """Handle price command"""
    price_data = get_ton_price()
    
    if price_data:
        price = price_data['price']
        change_24h = price_data['change_24h']
        
        # Format the change with emoji
        change_emoji = "📈" if change_24h > 0 else "📉" if change_24h < 0 else "➡️"
        
        response_text = f"""
💎 *TON Price Update*

💰 Price: *${price:,.2f}*
{change_emoji} 24h Change: *{change_24h:+.2f}%*

_Data from CoinGecko_
        """
    else:
        response_text = "❌ Sorry, couldn't fetch TON price at the moment. Please try again later."
    
    bot.send_message(message.chat.id, response_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Handle all other messages"""
    text = message.text.lower()
    
    if any(keyword in text for keyword in ['price', 'ton', 'toncoin']):
        send_price(message)

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()