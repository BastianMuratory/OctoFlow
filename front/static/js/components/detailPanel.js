import { getTemplate } from "../templateLoader.js"

let overlay, panel, body, title, description

export function initDetailPanel() {
    overlay = document.getElementById("panel-overlay")
    panel = document.getElementById("detail-panel")
    body = document.getElementById("detail-body")
    title = document.getElementById("detail-title")
    description = document.getElementById("detail-description")

    // Close panel when clicking the "close" button or when clicking outside of the panel
    document.getElementById("btn-detail-close").addEventListener("click", closeDetailPanel)
    overlay.addEventListener("click", closeDetailPanel)
}

export function openDetailPanel(type, data) {
    title.textContent = data.name ?? type.toUpperCase()
    description.textContent = data.details ?? ""

    if(type === "drone") {
        const droneContent = getTemplate("droneDetail")
        fillDroneDetails(droneContent, data)
        
        body.innerHTML = ""
        body.appendChild(droneContent)
    }

    overlay.classList.remove("hidden")
    panel.classList.remove("hidden")
}

export function closeDetailPanel() {
    overlay.classList.add("hidden")
    panel.classList.add("hidden")
}

function fillDroneDetails(container, drone) {
    let status = ""
    let encryptionType = ""

    // Fill some variables first
    if(drone.status !== 0 && drone.status !== 1)
        status = "Non opérationel"
    else
        status = (drone.status === 0 ? "Problème" : "Opérationel")

    if(drone.status !== 1 && drone.status !== 2)
        encryptionType = "Pas de chiffrement"
    else
        encryptionType = (drone.status === 1 ? "AES128" : "AES256")


    // System
    container.querySelector("#waterproof").checked = Boolean(drone.is_waterproof)
    container.querySelector("#status").textContent = status
    container.querySelector("#pix").checked = Boolean(drone.has_pix_double_layer_support)
    container.querySelector("#ce").checked = Boolean(drone.is_c5_c6_compliant)

    // Radio
    container.querySelector("#ip").textContent = drone.ip ?? ""
    container.querySelector("#mesh").textContent = drone.mesh ?? ""
    container.querySelector("#password").value = drone.encryption_key ?? ""
    container.querySelector("#aes").textContent = encryptionType
    container.querySelector("#model").textContent = drone.model ?? ""
    container.querySelector("#frequency").textContent = `${drone.min_frequency ?? ""}GHz - ${drone.max_frequency ?? ""}GHz`

    // Payload
    container.querySelector("#encoder").checked = Boolean(drone.has_encoder)
    container.querySelector("#eo").checked = Boolean(drone.has_eo)
    container.querySelector("#ir").checked = Boolean(drone.has_ir)
    container.querySelector("#sd").checked = Boolean(drone.has_encoder_sd_card)
    container.querySelector("#encoder-version").textContent = drone.encoder_version ?? ""
    container.querySelector("#eo-info").textContent = drone.eo_info ?? ""
    container.querySelector("#ir-info").textContent = drone.ir_info ?? ""
    container.querySelector("#payload-mount").textContent = drone.reverse_mounting ? "Oui" : "Non"
}