let hrs = document.getElementById("hrs");
let min = document.getElementById("min");
let sec = document.getElementById("sec");
let jrs = document.getElementById("jrs");
let mois = document.getElementById("mois");
let ann = document.getElementById("ann");

setInterval(()=>{
    let currentTime = new Date();

    hrs.innerHTML = (currentTime.getHours()<10?"0":"") + currentTime.getHours();
    min.innerHTML = (currentTime.getMinutes()<10?"0":"") + currentTime.getMinutes();
    sec.innerHTML = (currentTime.getSeconds()<10?"0":"") + currentTime.getSeconds();
    jrs.innerHTML = (currentTime.getDay())
    mois.innerHTML = (currentTime.getMonth())
    ann.innerHTML = (currentTime.getFullYear())
},1000)

