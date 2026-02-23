function renderDroneCard(drone, onDelete) {
    const template = document.getElementById("drone-card-template")
    const clone = template.content.cloneNode(true)

    clone.querySelector(".drone-name").textContent = drone.name
    clone.querySelector(".btn-delete").addEventListener("click", () => onDelete(drone.id))

    return clone
}

function renderDrones(drones, onDelete) {
    const grid = document.getElementById("drone-grid")
    grid.innerHTML = ""

    for (const drone of drones)
        grid.appendChild(renderDroneCard(drone, onDelete))
}