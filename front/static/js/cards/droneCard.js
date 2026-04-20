import { getTemplate } from "../templateLoader.js"
import { openPanel } from "../components/detailPanel.js"

export function renderDrones(drones) {
    const grid = document.getElementById("drone-grid")
    grid.innerHTML = ""

    drones.forEach((drone, index) => {
        const card = renderDroneCard(drone)
        grid.appendChild(card)
        setTimeout(() => card.classList.add("visible"), index * 50) // Show cards one by one, every 50ms
    })
}

function renderDroneCard(drone) {
    // Get the HTML components
    const card = getTemplate("droneCard")
    const dot = card.querySelector(".drone-status")
    const status = statusClass(drone.status)

    // Update cards colors based on drone's status
    card.classList.add(status)
    dot.classList.add(status)

    // Fill the card with drone informations
    card.querySelector(".drone-name").textContent = "Drone " + drone.name.toUpperCase()
    card.querySelector(".drone-radio-ip .value").textContent = drone.ip ?? "Unknown"
    card.querySelector(".drone-radio-mesh .value").textContent = drone.mesh ?? ""
    card.querySelector(".drone-radio-waterproof .value").checked = Boolean(drone.is_waterproof)
    card.querySelector(".drone-details").textContent = drone.details ?? ""
    card.querySelector(".drone-ready-to-fly").style.display = (drone.status === 1 ? "" : "none")

    // Send event to open the panel when button is clicked
    card.querySelector(".btn-details").addEventListener("click", () => {
        openPanel("drone", drone)
    })

    card.querySelector(".btn-flights").addEventListener("click", () => {
        openPanel("drone", drone, "flights")
    })

    card.querySelector(".btn-operations").addEventListener("click", () => {
        openPanel("drone", drone, "operations")
    })

    return card
}

function statusClass(status) {
    if (status === 1) return "status-ok"
    if (status === 0) return "status-warning"
    if (status === -1) return "status-error"
    return ""
}
