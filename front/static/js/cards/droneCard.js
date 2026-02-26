function statusClass(status) {
    if (status === 1) return "status-ok"
    if (status === 0) return "status-warning"
    if (status === -1) return "status-error"
    return ""
}

function renderDroneCard(drone) {
    const template = document.getElementById("drone-card-template")
    const clone = template.content.cloneNode(true)

    const card = clone.querySelector(".drone-card")
    const dot = clone.querySelector(".drone-status")
    const cls = statusClass(drone.status)

    card.classList.add(cls)
    dot.classList.add(cls)

    clone.querySelector(".drone-name").textContent = "Drone " + drone.name.toUpperCase()
    clone.querySelector(".drone-radio-ip .value").textContent = drone.ip ?? "Unknown"
    clone.querySelector(".drone-radio-mesh .value").textContent = drone.mesh ?? ""
    clone.querySelector(".drone-radio-waterproof .value").checked = Boolean(drone.is_waterproof)
    clone.querySelector(".drone-details").textContent = drone.details ?? ""
    clone.querySelector(".drone-ready-to-fly").style.display = (drone.status === 1 ? "" : "none")
    console.log(clone.querySelector(".drone-ready-to-fly").style.display, drone.status)

    return clone
}
function renderDrones(drones) {
    const grid = document.getElementById("drone-grid")
    grid.innerHTML = ""

    for (const drone of drones)
        grid.appendChild(renderDroneCard(drone))
}
