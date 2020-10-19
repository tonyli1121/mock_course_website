function show(i) {
  if(document.getElementById("feedback"+i).style.display == "none"||!document.getElementById("feedback"+i).style.display){
     document.getElementById("feedback"+i).style.display = "block";
     document.getElementById("button"+i).innerHTML = "hide feedback";
  } else {
    document.getElementById("feedback"+i).style.display = "none";
    document.getElementById("button"+i).innerHTML = "show feedback";
  }
}