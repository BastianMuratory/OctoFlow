function renderDroneCard(drone, onDelete) {
    const template = document.getElementById("drone-card-template")
    const clone = template.content.cloneNode(true)

    clone.querySelector(".drone-name").textContent = "Drone " + drone.name.toUpperCase()
    clone.querySelector(".drone-radio-ip").textContent = "IP: " + drone.ip ?? "Unknown ip"
    clone.querySelector(".drone-radio-mesh").textContent = "Mesh: " + drone.mesh ?? ""
    clone.querySelector(".drone-radio-model").textContent = "Model radio: " + drone.model ?? "Unknown model"

    clone.querySelector(".btn-delete").addEventListener("click", () => onDelete(drone.id))
    return clone
}

function renderDrones(drones, onDelete) {
    const grid = document.getElementById("drone-grid")
    grid.innerHTML = ""

    for (const drone of drones)
        grid.appendChild(renderDroneCard(drone, onDelete))
}