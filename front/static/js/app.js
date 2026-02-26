async function init() {
    const drones = await getDrones()
    renderDrones(drones)
}

window.addEventListener("load", init)