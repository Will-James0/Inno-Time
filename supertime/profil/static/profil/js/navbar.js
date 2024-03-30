const menu = document.querySelector(".material-symbols-outlined")
const navLinks = document.querySelector(".nav-links")

menu.addEventListener('click', ()=>{
    navLinks.classList.toggle('mobile-menu')
})