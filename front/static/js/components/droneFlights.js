import { getFlights, createFlight } from "../api.js"
import { getTemplate } from "../templateLoader.js"

export async function fillDroneFlights(parentBody, droneId) {
  const content = getTemplate("droneFlights")
  parentBody.appendChild(content)

  const counter = content.querySelector(".flights-count")
  const tbody   = content.querySelector(".flights-body")

  const flights = await getFlights(droneId)
  renderRows(counter, tbody, flights)

  content.querySelector(".btn-add-flight").addEventListener("click", () => addFlight(content, counter, tbody, droneId))
}

function formatDate(ts) {
  return new Date(ts * 1000).toLocaleDateString("fr-FR")
}

function formatDuration(seconds) {
  const h = String(Math.floor(seconds / 3600)).padStart(2, "0")
  const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, "0")
  const s = String(seconds % 60).padStart(2, "0")
  return `${h}:${m}:${s}`
}

function renderRows(counter, tbody, flights) {
  counter.textContent = `${flights.length} vol(s)`
  let cumul = 0
  tbody.innerHTML = flights.map(f => {
    cumul += f.duration ?? 0
    return `
      <tr>
        <td>${formatDate(f.date)}</td>
        <td>${f.pilot ?? "-"}</td>
        <td>${formatDuration(f.duration ?? 0)}</td>
        <td>${formatDuration(cumul)}</td>
        <td title="${f.purpose ?? ""}">${f.purpose ?? "-"}</td>
        <td title="${f.comments ?? ""}">${f.comments ?? "-"}</td>
      </tr>`
  }).join("")
}

async function addFlight(content, counter, tbody, droneId) {
  const pilot    = content.querySelector(".flight-pilot").value
  const duration = content.querySelector(".flight-duration").value
  const purpose  = content.querySelector(".flight-purpose").value
  const comments = content.querySelector(".flight-comments").value

  const parts   = duration.split(":").map(Number)
  const seconds = (parts[0] * 3600) + (parts[1] * 60) + (parts[2] ?? 0)

  await createFlight(droneId, { pilot, duration: seconds, purpose, comments })

  const updated = await getFlights(droneId)
  renderRows(counter, tbody, updated)
}