function printFiche(){
    var printContents = document.getElementById('container').innerHTML;
    var originalContents = document.body.innerHTML;
    document.body.innerHTML = printContents
    window.print();
    document.body.innerHTML = originalContents
}