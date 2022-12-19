# Brief Writeup

Haskell sucks, but it's just about learning to read it. Luckily, I "cheated" and just had [OpenAI](https://chat.openai.com/chat) explain it to me.

Conversation Example
```yaml
ME: "{code copied and pasted}. Explain the above Haskell code"

AI: """
The code you provided is a Haskell program that checks the validity of a string called flag. The flag variable is set to the string "HTB{XXX}" but the code does not provide any way to change its value.

The extractFlag function is defined as a pattern matching function that attempts to parse a string and extract a substring that is surrounded by curly braces ({ and }). If the input string is not in the correct format, the function throws an error with the message "Invalid format".

The chunks function is defined to take a list l and a non-negative integer n and returns a list of sublists of l, each sublist containing n elements from l.

The takeLast function is defined to take a list l and a non-negative integer n and returns the last n elements of l.
...[trim]...
"""
```

Then just write it in Python. After a while, I encountered an issue where I couldn't find all of the characters, so then I started guessing and letting the Python program fill in the other characters, until I realized that the flag is just a well known quote from the creator of Haskell.