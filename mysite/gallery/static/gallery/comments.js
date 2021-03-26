var button = document.getElementsByName("toggle-comments");

for (var i = 0; i < button.length; i++) {
  button[i].addEventListener("click", function () {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
      this.innerHTML = "Show Comments"
    } else {
      content.style.display = "block";
      this.innerHTML = "Hide Comments"
    }
  });
}