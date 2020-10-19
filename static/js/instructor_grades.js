function clickRegrade(i) {
  if(document.getElementById("newgrade"+i).style.display == "none"||!document.getElementById("newgrade"+i).style.display){
     document.getElementById("newgrade"+i).style.display = "block";
  } else {
    document.getElementById("newgrade"+i).style.display = "none";
  }
}

function clickNewGrade() {
  if(document.getElementById("newgradeform").style.display == "none"||!document.getElementById("newgradeform").style.display){
     document.getElementById("newgradeform").style.display = "block";
  } else {
    document.getElementById("newgradeform").style.display = "none";
  }
}