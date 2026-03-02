import { preloadTemplates } from "./templateLoader.js"
import { renderDrones } from "./cards/droneCard.js"
import { initDetailPanel } from "./components/detailPanel.js"

async function init() {
    // Pre-load templates to prevent redundant loading times
    await preloadTemplates()

    // Create the detail panel
    initDetailPanel()

    // Load drone cards
    const drones = await getDrones()
    renderDrones(drones)
}

window.addEventListener("load", init)