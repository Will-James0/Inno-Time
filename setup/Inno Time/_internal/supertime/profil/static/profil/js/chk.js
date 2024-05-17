// const chk = document.getElementById("checkbox");
// const supp = document.getElementById("supp");

// chk.addEventListener('click', () => {
//   const isChecked = chk.checked;
//   supp.style.display = isChecked ? "block" : "none";
// });
/*
const checkboxes = document.querySelectorAll('.checkbox'); // Select all checkboxes
const supp = document.getElementById("supp"); // Get the element to show/hide

// Add click event listener to each checkbox
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('click', () => {
    const isChecked = checkbox.checked; // Check the checkbox state
    supp.style.display = isChecked ? "block" : "none"; // Show or hide the element based on checkbox state
  });
});*/


const checkboxes = document.querySelectorAll('.checkbox'); // Select all checkboxes
const supp = document.getElementById("supp"); // Get the element to show/hide
const checkall = document.querySelector('.checkall'); // Select the check all button

// Function to toggle the state of all checkboxes
const toggleCheckboxes = () => {
  const isChecked = checkall.checked;
  checkboxes.forEach(checkbox => checkbox.checked = isChecked);
}

// Add click event listener to the "check all" button
checkall.addEventListener('click', toggleCheckboxes);

checkall.addEventListener('click', () => {
  supp.style.display = areAllUnchecked() ? "none" : "block";
});

// Function to check if all checkboxes are unchecked
const areAllUnchecked = () => {
  return Array.from(checkboxes).every(checkbox => !checkbox.checked);
}

// Add click event listener to each checkbox
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('click', () => {
    supp.style.display = areAllUnchecked() ? "none" : "block";
  });
});

// Initial check for checkbox state (optional)
const areAllInitiallyChecked = checkboxes.every(checkbox => checkbox.checked);
checkall.checked = areAllInitiallyChecked; // Set check all state based on initial checkbox states

