import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '7366536132:AAHsDe9byoCDMYvcr1rQCN0zZ6EfOZEc5-4'

# Global variable to store the last known state of the file
last_known_state = ""

# Function to send the updated content of list_valid.txt
async def send_updated_content(update: Update) -> None:
    global last_known_state
    
    try:
        with open('list_valid.txt', 'r') as file:
            current_state = file.read()
        
        if current_state != last_known_state:
            new_lines = [line.strip() for line in current_state.splitlines() if line not in last_known_state.splitlines()]
            if new_lines:
                response_message = "New lines added to list_valid.txt:\n" + "\n".join(new_lines)
                await update.message.reply_text(response_message)
            last_known_state = current_state
    
    except FileNotFoundError:
        await update.message.reply_text("Error: File 'list_valid.txt' not found.")

# Define a command handler function for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with open('list_valid.txt', 'r') as file:
            contents = file.readlines()
        
        if contents:
            response_message = "List of accounts and URLs:\n"
            for line in contents:
                response_message += line.strip() + "\n"
        else:
            response_message = "The list is empty."

        await update.message.reply_text(response_message)

    except FileNotFoundError:
        await update.message.reply_text("Error: File 'list_valid.txt' not found.")

# Define a command handler function for /listing
async def listing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_updated_content(update)

# Main function

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("test done")
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('listing', listing))
    application.add_handler(CommandHandler('test', test))
    

    application.run_polling()

if __name__ == '__main__':
    main()
