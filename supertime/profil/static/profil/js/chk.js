const chk = document.getElementById("checkbox");
const supp = document.getElementById("supp");

chk.addEventListener('click', () => {
  const isChecked = chk.checked;
  supp.style.display = isChecked ? "block" : "none";

//   if (isChecked) {
//     supp.classList.add("animated", "fadeIn");
//   } else {
//     supp.classList.add("animated", "fadeOut");
//   }
});
