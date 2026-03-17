import { getFlights, createFlight, updateFlight } from "../api.js"
import { getTemplate } from "../templateLoader.js"

let _counter, _tbody, _droneId, _flights

export async function fillDroneFlights(parentBody, droneId) {
    const content = getTemplate("droneFlights")
    parentBody.appendChild(content)

    _counter = content.querySelector(".flights-count")
    _tbody = content.querySelector(".flights-body")
    _droneId = droneId

    _flights = await getFlights(droneId)
    renderRows(false)

    content.querySelector(".btn-add-flight").addEventListener("click", () => addFlight(content))
}

export function setFlightsEditMode(editable) {
    renderRows(editable)
}

function renderRows(isEditMode) {
    _counter.textContent = `${_flights.length} vol(s)`
    let cumul = 0
    _tbody.innerHTML = _flights.map(f => {
        cumul += f.duration ?? 0
        if (isEditMode) {
            return `
        <tr data-id="${f.id}">
          <td>${formatDate(f.date)}</td>
          <td><input class="detail-input edit-pilot" value="${f.pilot ?? ""}" /></td>
          <td><input class="detail-input edit-duration" value="${formatDuration(f.duration ?? 0)}" /></td>
          <td>${formatDuration(cumul)}</td>
          <td><textarea class="detail-input edit-purpose">${f.purpose ?? ""}</textarea></td>
          <td><textarea class="detail-input edit-comments">${f.comments ?? ""}</textarea></td>
        </tr>`
        }
        return `
      <tr>
        <td>${formatDate(f.date)}</td>
        <td>${f.pilot ?? "-"}</td>
        <td>${formatDuration(f.duration ?? 0)}</td>
        <td>${formatDuration(cumul)}</td>
        <td>${f.purpose ?? "-"}</td>
        <td>${f.comments ?? "-"}</td>
      </tr>`
    }).join("")

    if (isEditMode)
        attachRowListeners()
}

function attachRowListeners() {
    _tbody.querySelectorAll("tr[data-id]").forEach(row => {
        const flightId = parseInt(row.dataset.id)

        row.querySelectorAll(".detail-input").forEach(input => {
            input.addEventListener("change", async () => {
                const pilot = row.querySelector(".edit-pilot").value
                const duration = row.querySelector(".edit-duration").value
                const purpose = row.querySelector(".edit-purpose").value
                const comments = row.querySelector(".edit-comments").value

                const parts = duration.split(":").map(Number)
                const seconds = (parts[0] * 3600) + (parts[1] * 60) + (parts[2] ?? 0)

                await updateFlight(_droneId, flightId, { pilot, duration: seconds, purpose, comments })

                // Refresh local data
                _flights = await getFlights(_droneId)
            })
        })
    })
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

async function addFlight(content) {
    const pilot = content.querySelector(".flight-pilot").value
    const duration = content.querySelector(".flight-duration").value
    const purpose = content.querySelector(".flight-purpose").value
    const comments = content.querySelector(".flight-comments").value

    const parts = duration.split(":").map(Number)
    const seconds = (parts[0] * 3600) + (parts[1] * 60) + (parts[2] ?? 0)

    await createFlight(_droneId, { pilot, duration: seconds, purpose, comments })

    _flights = await getFlights(_droneId)
    renderRows(false)
}