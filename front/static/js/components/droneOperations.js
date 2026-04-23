import { getOperations, createOperation, updateOperation } from "../api.js"
import { getTemplate } from "../templateLoader.js"

let _counter, _tbody, _droneId, _operations

export async function fillDroneOperations(parentBody, droneId) {
    const content = getTemplate("droneOperations")
    parentBody.appendChild(content)

    _counter = content.querySelector(".operations-count")
    _tbody = content.querySelector(".operations-body")
    _droneId = droneId

    _operations = await getOperations(droneId)
    renderRows(false)

    content.querySelector(".btn-add-operation").addEventListener("click", () => addOperation(content))
}

export async function setOperationsEditMode(editable) {
    if (!editable)
        await saveAllRows()
    renderRows(editable)
}

async function saveAllRows() {
    const rows = _tbody.querySelectorAll("tr[data-id]")

    for (const row of rows) {
        const opId = parseInt(row.dataset.id)
        const type = row.querySelector(".edit-type").value
        const description = row.querySelector(".edit-description").value
        const done_by = row.querySelector(".edit-done-by").value
        const validated_by = row.querySelector(".edit-validated-by").value
        const material_cost = parseFloat(row.querySelector(".edit-cost").value) || null
        const comments = row.querySelector(".edit-comments").value

        await updateOperation(_droneId, opId, { type, description, done_by, validated_by, material_cost, comments })
    }
    
    _operations = await getOperations(_droneId)
}

function renderRows(isEditMode) {
    _counter.textContent = `${_operations.length} opération(s)`

    _tbody.innerHTML = _operations.map(op => {
        const cost = op.material_cost != null ? `${op.material_cost} €` : "-"

        if (isEditMode) {
            return `
            <tr data-id="${op.id}">
                <td>${formatDate(op.date)}</td>
                <td><input class="detail-input edit-type" value="${op.type ?? ""}" /></td>
                <td><textarea class="detail-input edit-description">${op.description ?? ""}</textarea></td>
                <td><input class="detail-input edit-done-by" value="${op.done_by ?? ""}" /></td>
                <td><input class="detail-input edit-validated-by" value="${op.validated_by ?? ""}" /></td>
                <td><input class="detail-input edit-cost" type="number" step="0.01" min="0" value="${op.material_cost ?? ""}" /></td>
                <td><textarea class="detail-input edit-comments">${op.comments ?? ""}</textarea></td>
            </tr>`
        }

        return `
        <tr>
            <td>${formatDate(op.date)}</td>
            <td>${op.type ?? "-"}</td>
            <td>${op.description ?? "-"}</td>
            <td>${op.done_by ?? "-"}</td>
            <td>${op.validated_by ?? "-"}</td>
            <td>${cost}</td>
            <td>${op.comments ?? "-"}</td>
        </tr>`
    }).join("")
}

function formatDate(ts) {
    return new Date(ts * 1000).toLocaleDateString("fr-FR")
}

async function addOperation(content) {
    const type = content.querySelector(".op-type").value
    const description = content.querySelector(".op-description").value
    const done_by = content.querySelector(".op-done-by").value
    const validated_by = content.querySelector(".op-validated-by").value
    const material_cost = parseFloat(content.querySelector(".op-cost").value) || null
    const comments = content.querySelector(".op-comments").value
    await createOperation(_droneId, { type, description, done_by, validated_by, material_cost, comments })

    _operations = await getOperations(_droneId)
    renderRows(false)
}