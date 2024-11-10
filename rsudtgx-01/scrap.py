from dotenv import load_dotenv
import instaloader
import json
import re
import os

load_dotenv()

USER = os.getenv('USER')
shortcodes = json.loads(os.getenv('SHORTCODES'))

L = instaloader.Instaloader()
L.load_session_from_file(USER)

# Load bot check results from storage
bot_check_file = 'bot_check_results.json'
if os.path.exists(bot_check_file):
    with open(bot_check_file, 'r') as f:
        bot_check_results = json.load(f)
else:
    bot_check_results = {}

def is_bot(username):
    if username in bot_check_results and bot_check_results[username] != 'indicated':
        return bot_check_results[username]
    
    indicated_bot = False
    bot_patterns = [
        r'\d{4,}', # 4 digits or more
        r'(.)\1{2,}', # 3 or more repeating characters
        r'bot', # 'bot' in username
        r'test', # 'test' in username
        r'private', # 'private' in username
    ]
    for pattern in bot_patterns:
        if re.search(pattern, username.lower()):
            indicated_bot = True
            break
    
    if indicated_bot:
        # profile = instaloader.Profile.from_username(L.context, username)
        # if profile.followers < 10:
        #     bot_check_results[username] = True
        #     with open(bot_check_file, 'w') as f:
        #         json.dump(bot_check_results, f, indent=4)
        #     return True

        bot_check_results[username] = 'indicated'
        with open(bot_check_file, 'w') as f:
            json.dump(bot_check_results, f, indent=4)
        return True

    return False

for shortcode, label in shortcodes.items():
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    comments = post.get_comments()
    comments_list = []
    for comment in comments:
        timestamp_utc = comment.created_at_utc
        bot = is_bot(comment.owner.username)
        bot_text = 'BOT' if bot else ''
        print(f"{comment.owner.username} {bot_text}: {comment.text} - {timestamp_utc}")
        comments_list.append({
            'username': f'{comment.owner.username}',
            'text': f'{comment.text}',
            'timestamp': f'{timestamp_utc}',
            # 'is_bot': bot,
        })

    output_file = f'{label}.json'
    with open(output_file, 'w') as f:
        json.dump(comments_list, f, indent=4)

    print(f"Comments have been saved to {output_file}")
    
