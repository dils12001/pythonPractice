$(document).ready(function(){
    // <html>的style屬性，fontsize設置為 螢幕寬度/10 (<html>的 fontsize 等於 1 rem)
    // 若螢幕寬度為 320px，則 1rem = 32px
    document.documentElement.style.fontSize = innerWidth / 10 + "px";
})

