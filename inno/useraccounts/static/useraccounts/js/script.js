document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('.left').addEventListener('click', toggleFlex);
  });
  
  function toggleFlex() {
    const div1 = document.getElementsByClassName('left');
    const div2 = document.getElementsByClassName('home');
  
    if (div1.style.flex === '1') {
      div1.style.flex = '0';
      div2.style.flex = '2';
    } else {
      div1.style.flex = '1';
      div2.style.flex = '1';
    }
  }
  