const API = "http://localhost:5000"

export async function getDrones() {
    const res = await fetch(`${API}/drones`)

    if (!res.ok)
        throw new Error("Failed to get drones")
    return res.json()
}

export async function deleteDrone(id) {
    const res = await fetch(`${API}/drones/${id}`, { method: "DELETE" })

    if (!res.ok)
        throw new Error("Failed to delete drone")
}

export async function updateDrone(id, data) {
    const res = await fetch(`${API}/drones/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })

    if (!res.ok)
        throw new Error("Failed to update drone")

    return res.json()
}