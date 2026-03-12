import { updateDrone } from "../api.js"
import { getTemplate } from "../templateLoader.js"

let overlay, panel, body, title, description
let isEditMode = false
let currentContainer = null
let currentType = null
let currentData = null
let currentDroneId = null
let activeTab = "details"

export function initDetailPanel() {
    overlay = document.getElementById("panel-overlay")
    panel = document.getElementById("detail-panel")
    body = document.getElementById("detail-body")
    title = document.getElementById("detail-title")
    description = document.getElementById("detail-description")

    document.getElementById("btn-detail-close").addEventListener("click", handleCloseAttempt)
    overlay.addEventListener("click", handleCloseAttempt)

    document.querySelectorAll(".detail-tab").forEach(btn => {
        btn.addEventListener("click", () => {
            if (isEditMode) return
            showTab(btn.dataset.tab)
        })
    })
}

export function openDetailPanel(type, data) {
    currentType = type
    currentData = data

    currentDroneId = data.id
    title.textContent = data.name ?? type.toUpperCase()
    description.textContent = data.details ?? ""

    isEditMode = false
    renderFooter()
    showTab("details")

    overlay.classList.remove("hidden")
    panel.classList.remove("hidden")
}

export function closeDetailPanel() {
    overlay.classList.add("hidden")
    panel.classList.add("hidden")

    isEditMode = false
    currentContainer = null
    currentType = null
    currentData = null
    activeTab = "details"
}

// Tabs
function showTab(tabId) {
    activeTab = tabId
    body.innerHTML = ""

    document.querySelectorAll(".detail-tab").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.tab === tabId)
        btn.classList.toggle("disabled", isEditMode && btn.dataset.tab !== tabId)
    })

    if (currentType === "drone") {
        if (tabId === "details") {
            const content = getTemplate("droneDetail")
            fillDroneDetails(content, currentData)
            body.appendChild(content)
            currentContainer = content
            if (isEditMode) setFieldsEditable(true)

            // Password toggle
            const passwordInput = content.querySelector("#password")
            const toggleBtn = content.querySelector("#toggle-password")
            toggleBtn.addEventListener("click", () => {
                const isHidden = passwordInput.type === "password"
                passwordInput.type = isHidden ? "text" : "password"
                toggleBtn.querySelector("i").className = isHidden ? "bi bi-eye-slash" : "bi bi-eye"
            })
        } else if (tabId === "flights") {
            body.innerHTML = `
                <div class="tab-placeholder">
                    <i class="bi bi-airplane"></i>
                    <p>Aucun vol enregistré</p>
                </div>`
        } else if (tabId === "operations") {
            body.innerHTML = `
                <div class="tab-placeholder">
                    <i class="bi bi-diagram-3"></i>
                    <p>Aucune opération enregistrée</p>
                </div>`
        }
    }
    // else ... for other types
}

// Footer
function renderFooter() {
    const footer = document.getElementById("detail-footer")
    footer.innerHTML = ""

    if (isEditMode) {
        footer.innerHTML = `
            <div class="footer-edit-mode">
                <button class="btn-save">Sauvegarder</button>
                <button class="btn-cancel-edit">Annuler</button>
            </div>
        `
        footer.querySelector(".btn-save").addEventListener("click", saveChanges)
        footer.querySelector(".btn-cancel-edit").addEventListener("click", cancelEditMode)
    } else {
        footer.innerHTML = `
            <button class="btn-edit">Éditer</button>
            <button class="btn-delete">Supprimer</button>
        `
        footer.querySelector(".btn-edit").addEventListener("click", enterEditMode)
    }
}

// Edit mode
function enterEditMode() {
    isEditMode = true
    setFieldsEditable(true)
    updateTabsLock()
    renderFooter()
}

function cancelEditMode() {
    isEditMode = false
    showTab(activeTab)
    updateTabsLock()
    renderFooter()
}

async function saveChanges() {
    try {
        const data = collectFormValues()
        await updateDrone(currentDroneId, data)

        isEditMode = false
        setFieldsEditable(false)
        updateTabsLock()
        renderFooter()

        // Refresh list
        window.dispatchEvent(new CustomEvent("drone-updated"))
    } catch (error) {
        console.error("Failed to save:", error)
    }
}

function setFieldsEditable(editable) {
    if (!currentContainer) return
    currentContainer.querySelectorAll(".detail-input").forEach(input => {
        input.disabled = !editable
        input.classList.toggle("editable", editable)
    })
    currentContainer.querySelectorAll("input[type='checkbox']").forEach(cb => {
        cb.disabled = !editable
    })
}

function updateTabsLock() {
    document.querySelectorAll(".detail-tab").forEach(btn => {
        btn.classList.toggle("disabled", isEditMode && btn.dataset.tab !== activeTab)
    })
}

// Close guard
function handleCloseAttempt() {
    if (!isEditMode) {
        closeDetailPanel()
        return
    }
    showUnsavedDialog()
}

function showUnsavedDialog() {
    document.getElementById("unsaved-dialog")?.remove()

    const dialog = document.createElement("div")
    dialog.id = "unsaved-dialog"
    dialog.className = "unsaved-dialog"
    dialog.innerHTML = `
        <div class="unsaved-dialog-box">
            <p>Des modifications non sauvegardées seront perdues.</p>
            <div class="unsaved-dialog-actions">
                <button class="btn-action" id="dialog-stay">Continuer l'édition</button>
                <button class="btn-delete" id="dialog-leave">Quitter sans sauvegarder</button>
            </div>
        </div>
    `
    panel.appendChild(dialog)

    dialog.querySelector("#dialog-stay").addEventListener("click", () => dialog.remove())
    dialog.querySelector("#dialog-leave").addEventListener("click", () => {
        dialog.remove()
        closeDetailPanel()
    })
}

// Fill data
function fillDroneDetails(container, drone) {
    container.querySelector("#waterproof").checked = Boolean(drone.is_waterproof)
    container.querySelector("#status").value = drone.status
    container.querySelector("#pix").checked = Boolean(drone.has_pix_double_layer_support)
    container.querySelector("#ce").checked = Boolean(drone.is_c5_c6_compliant)

    container.querySelector("#ip").value = drone.ip ?? ""
    container.querySelector("#mesh").value = drone.mesh ?? ""
    container.querySelector("#password").value = drone.encryption_key ?? ""
    container.querySelector("#aes").value = drone.encryption_type
    container.querySelector("#model").value = drone.model ?? ""
    container.querySelector("#frequency").value = `${drone.min_frequency ?? ""}GHz - ${drone.max_frequency ?? ""}GHz`

    container.querySelector("#encoder").checked = Boolean(drone.has_encoder)
    container.querySelector("#eo").checked = Boolean(drone.has_eo)
    container.querySelector("#ir").checked = Boolean(drone.has_ir)
    container.querySelector("#sd").checked = Boolean(drone.has_encoder_sd_card)
    container.querySelector("#encoder-version").value = drone.encoder_version ?? ""
    container.querySelector("#eo-info").value = drone.eo_info ?? ""
    container.querySelector("#ir-info").value = drone.ir_info ?? ""
    container.querySelector("#payload-mount").value = Boolean(drone.reverse_mounting)
}

// Create a JSON from the current data
function collectFormValues() {
    return {
        // System
        waterproof: document.getElementById("waterproof").checked,
        status: parseInt(document.getElementById("status").value),
        pix: document.getElementById("pix").checked,
        ce: document.getElementById("ce").checked,

        // Radio
        ip: document.getElementById("ip").value,
        mesh: document.getElementById("mesh").value,
        password: document.getElementById("password").value,
        aes: parseInt(document.getElementById("aes").value),
        model: document.getElementById("model").value,
        frequency: document.getElementById("frequency").value,

        // Payload
        encoder: document.getElementById("encoder").checked,
        eo: document.getElementById("eo").checked,
        ir: document.getElementById("ir").checked,
        sd: document.getElementById("sd").checked,
        encoderVersion: document.getElementById("encoder-version").value,
        eoInfo: document.getElementById("eo-info").value,
        irInfo: document.getElementById("ir-info").value,
        payloadMount: document.getElementById("payload-mount").checked
    }
}