export async function getDrones() {
    const res = await fetch("/drones")

    if (!res.ok)
        throw new Error("Failed to get drones")
    return res.json()
}

export async function deleteDrone(id) {
    const res = await fetch(`/drones/${id}`, { method: "DELETE" })

    if (!res.ok)
        throw new Error("Failed to delete drone")
}

export async function updateDrone(id, data) {
    const res = await fetch(`/drones/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })

    if (!res.ok)
        throw new Error("Failed to update drone")

    return res.json()
}

export async function getFlights(droneId) {
    const res = await fetch(`/drones/${droneId}/flights`)

    if (!res.ok)
        throw new Error("Failed to get flights")
    return res.json()
}

export async function createFlight(droneId, data) {
    const res = await fetch(`/drones/${droneId}/flights`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })

    if (!res.ok)
        throw new Error("Failed to create flight")
    return res.json()
}

export async function updateFlight(droneId, flightId, data) {
    const res = await fetch(`/drones/${droneId}/flights/${flightId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })

    if (!res.ok)
        throw new Error("Failed to update flight")
    return res.json()
}

export async function getOperations(droneId) {
    const res = await fetch(`/drones/${droneId}/operations`)
    if (!res.ok)
        throw new Error("Failed to get operations")
    return res.json()
}

export async function createOperation(droneId, data) {
    const res = await fetch(`/drones/${droneId}/operations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    if (!res.ok)
        throw new Error("Failed to create operation")
    return res.json()
}

export async function updateOperation(droneId, operationId, data) {
    const res = await fetch(`/drones/${droneId}/operations/${operationId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    if (!res.ok)
        throw new Error("Failed to update operation")
    return res.json()
}