const API = "http://localhost:5000"

async function getDrones() {
    const res = await fetch(`${API}/drones`)
    
    if (!res.ok)
        throw new Error("Server error")
    return res.json()
}

async function deleteDrone(id) {
    const res = await fetch(`${API}/drones/${id}`, { method: "DELETE" })

    if (!res.ok)
        throw new Error("Failed to delete drone")
}