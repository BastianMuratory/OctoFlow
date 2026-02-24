function statusClass(status) {
    if (status === 1) return "status-ok"
    if (status === 0) return "status-warning"
    if (status === -1) return "status-error"
    return ""
}

function renderDroneCard(drone, onDelete) {
    const template = document.getElementById("drone-card-template")
    const clone = template.content.cloneNode(true)

    const card = clone.querySelector(".drone-card")
    const dot = clone.querySelector(".drone-status")
    const cls = statusClass(drone.status)

    card.classList.add(cls)
    dot.classList.add(cls)

    clone.querySelector(".drone-name").textContent = "Drone " + drone.name.toUpperCase()
    clone.querySelector(".drone-radio-ip").textContent = "IP: " + (drone.ip ?? "Unknown")
    clone.querySelector(".drone-radio-mesh").textContent = "Mesh: " + (drone.mesh ?? "")
    clone.querySelector(".drone-radio-model").textContent = "Model radio: " + (drone.model ?? "Unknown")

    clone.querySelector(".btn-delete").addEventListener("click", () => onDelete(drone.id))

    return clone
}
function renderDrones(drones, onDelete) {
    const grid = document.getElementById("drone-grid")
    grid.innerHTML = ""

    for (const drone of drones)
        grid.appendChild(renderDroneCard(drone, onDelete))
}
