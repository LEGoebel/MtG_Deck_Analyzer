from random import choice, randint


def get_response(user_input: str) -> str:
    lowered_input = user_input.lower()
    
    if lowered_input == '':
        return "Well, you're awfully silent... Maybe I don/'t want to talk to you either."
    elif 'hello' in lowered_input:
        return "Hello there!"
    elif "how are you" in lowered_input:
        return "Good, I hope you too!"
    elif "bye" in lowered_input:
        return "Goodbye"
    elif "roll dice" in lowered_input:
        return f"You rolled: {randint(1,6)}"
    else:
        return choice(["I do not understand...",
                       "What are you talking about?",
                       "Do you mind rephrasing that. Try with hello, bye, or roll dice in your message!"])