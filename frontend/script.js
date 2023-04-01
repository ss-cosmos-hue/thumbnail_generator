function myFunction() {
  document.getElementById("frm1").submit();
}

function WordCount(str) {
  var totalSoFar = 0;
  for (var i = 0; i < WordCount.length; i++)
    if (str(i) === " ") {
      totalSoFar = +1;
    }
  totalsoFar += 1;
}

function validateForm() {
  let x = document.forms["frm1"]["words"].value;
  if (x < 1 || x > 3) {
    alert("Please enter a phrase between 1-3 words");
    return false;
  }
}
