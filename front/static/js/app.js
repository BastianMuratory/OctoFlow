import { preloadTemplates } from "./templateLoader.js"
import { getDrones } from "./api.js"
import { renderDrones } from "./cards/droneCard.js"
import { initDetailPanel } from "./components/detailPanel.js"

async function loadDrones() {
    const drones = await getDrones()
    renderDrones(drones)
}

async function init() {
    // Pre-load templates to prevent redundant loading times
    await preloadTemplates()

    initDetailPanel()
    loadDrones()    

    window.addEventListener("drone-updated", async () => {
        loadDrones()
  })
}

window.addEventListener("load", init)