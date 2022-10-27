# Other Web Challenges
> You expect me to make solve scripts for all of them???

## Day 2: Spookifier
SSTI with the Mako engine, [link](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#direct-access-to-os-from-templatenamespace), exfiltrate to webhook

## Day 3: Horror Feeds
Apparently intended was nested SQL queries, but there's a keyword in SQL to overwrite stuff with ([PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection#insert-statement---on-duplicate-key-update))

```sql
admin", "USE_CODE_TO_MAKE_NEW_PWD_HASH") ON DUPLICATE KEY UPDATE password="USE_CODE_TO_MAKE_NEW_PWD_HASH" -- -
```

## Day 4: Juggling Facts
PHP Type Juggling. Capture the request when you request the "secrets" bit, replace the message with `true`. Ippsec has a good video on the subject [here](https://www.youtube.com/watch?v=idC5SAsKhlE). Interesting thing about this one is that the triple equals was used, but it's the switch statement that's the real killer. 