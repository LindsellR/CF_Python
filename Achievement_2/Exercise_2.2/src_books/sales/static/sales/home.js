// sales/static/home.js
document.addEventListener("DOMContentLoaded", () => {
  // Highlight rows on hover
  const rows = document.querySelectorAll("table tr");
  rows.forEach(row => {
    row.addEventListener("mouseover", () => row.style.backgroundColor = "#eaeaea");
    row.addEventListener("mouseout", () => row.style.backgroundColor = "");
  });

  // Highlight active nav link
  const links = document.querySelectorAll(".navbar a");
  links.forEach(link => {
    if (link.href === window.location.href) {
      link.style.color = "#CBA135";
    }
  });
});
