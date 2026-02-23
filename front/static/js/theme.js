const toggle = document.getElementById("themeToggle")
const icon = toggle.querySelector("i")

toggle.addEventListener("click", () => {
  applyTheme(!document.documentElement.classList.contains("dark"))
})

function applyTheme(dark) {
  document.documentElement.classList.toggle("dark", dark)
  icon.className = dark ? "bi bi-moon-fill" : "bi bi-sun-fill"
  localStorage.setItem("theme", dark ? "dark" : "light")
}