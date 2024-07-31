import telebot
from telebot import types

# Replace with your bot token and target channel ID
bot = telebot.TeleBot('7454404106:AAFBYCcYqQT5oyZ0pbpKGly6W_xoQzt3S00')
target_channel = '@RobinhoodxD_Reviews'

def extract_rating(text):
    """Extracts the rating from the user's review, handling potential errors gracefully.

    Args:
        text (str): The user's review message.

    Returns:
        int: The extracted rating (1-5) or None if invalid.
    """
    try:
        # Split the text by spaces, taking the last word as the potential rating
        potential_rating = text.split()[-1]
        rating = int(potential_rating)

        if 1 <= rating <= 5:
            return rating
        else:
            return None  # Invalid rating range

    except ValueError:
        # Not a valid number, consider more sophisticated extraction if needed
        return None

def format_review(text, rating, name):
    """Formats the review message with the extracted rating (or placeholder if not found).

    Args:
        text (str): The user's review message.
        rating (int or None): The extracted rating or None if not valid.
        name (str): The name of the customer.

    Returns:
        str: The formatted review message with rating stars.
    """
    # Create a colored rating representation
    star_full = '⭐'
    star_empty = '☆'
    stars = star_full * rating + star_empty * (5 - rating)
    
    # Escape special characters for Markdown
    escaped_name = name.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]')
    escaped_text = text.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]')
    
    # Format the review message
    return (
        f"*REVIEWS:*\n"
        f"Customer: {escaped_name}\n"
        f"Feedback: {escaped_text}\n"
        f"RATING: {stars}"
    )

@bot.message_handler(commands=['start'])
def start(message):
    """Handles the /start command, prompting the user to submit a review."""
    print("Start command received")
    bot.send_message(message.chat.id, "Welcome! Please use /review to submit your review and rating.")

@bot.message_handler(commands=['review'])
def review(message):
    print("Review command received")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton("Submit Review")
    markup.add(itembtn1)
    bot.send_message(message.chat.id, "Please submit your review and rating (e.g., 'Product is great 5'):", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_review(message):
    print(f"Received message: {message.text}")
    # Extract rating from message
    rating = extract_rating(message.text)
    # Remove rating from the message for clean formatting
    review_text = ' '.join(message.text.split()[:-1])
    customer_name = message.from_user.first_name or message.from_user.username or "Anonymous"
    formatted_review = format_review(review_text, rating, customer_name)
    print(f"Formatted review: {formatted_review}")

    try:
        bot.send_message(target_channel, formatted_review, parse_mode='Markdown')
        print(f"Review sent to channel: {target_channel}")
        bot.send_message(message.chat.id, "Thank you for your review!")
    except Exception as e:
        print(f"Error sending review: {e}")
        bot.send_message(message.chat.id, "An error occurred. Please try again later.")

bot.polling()
