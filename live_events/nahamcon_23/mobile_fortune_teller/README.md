# Short Writeup

- Use `apktool` to unzip the archive to dig into the files
- Use `mobsf` to decompile and analyze the code
- Note `res/raw/encrypted` exists
- Don't even bother running the app, just look at Decrypt.java and how it's pulling a specific string for the key
- Follow R.java and find the `correct_guess` string in `res/values/strings.xml` to find the key `you win this ctf`
- Decrypt using pycryptodome or CyberChef