// const chk = document.getElementById("checkbox");
// const supp = document.getElementById("supp");

// chk.addEventListener('click', () => {
//   const isChecked = chk.checked;
//   supp.style.display = isChecked ? "block" : "none";
// });

const checkboxes = document.querySelectorAll('.checkbox'); // Select all checkboxes
const supp = document.getElementById("supp"); // Get the element to show/hide

// Add click event listener to each checkbox
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('click', () => {
    const isChecked = checkbox.checked; // Check the checkbox state
    supp.style.display = isChecked ? "block" : "none"; // Show or hide the element based on checkbox state
  });
});
