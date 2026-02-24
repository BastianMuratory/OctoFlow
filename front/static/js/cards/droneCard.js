function renderDroneCard(drone, onDelete) {
    const template = document.getElementById("drone-card-template")
    const clone = template.content.cloneNode(true)

    clone.querySelector(".drone-name").textContent = drone.name
    clone.querySelector(".drone-radio-ip").textContent = drone.ip ?? "Unknown ip"
    clone.querySelector(".drone-radio-mesh").textContent = drone.mesh ?? ""
    clone.querySelector(".drone-radio-model").textContent = drone.model ?? "Unknown model"

    clone.querySelector(".btn-delete").addEventListener("click", () => onDelete(drone.id))
    return clone
}

function renderDrones(drones, onDelete) {
    const grid = document.getElementById("drone-grid")
    grid.innerHTML = ""

    for (const drone of drones)
        grid.appendChild(renderDroneCard(drone, onDelete))
}