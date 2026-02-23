async function init() {
    const drones = await getDrones()
    renderDrones(drones, handleDelete)
}

async function handleDelete(id) {
    await deleteDrone(id)
    init()
}

init()