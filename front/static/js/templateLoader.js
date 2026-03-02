const templates = {} // List of all pre-loaded templates

export async function preloadTemplates() {
    const templatesNames = ["droneCard", "droneDetail"]

    for (const template of templatesNames) {
        const res = await fetch(`/static/templates/${template}.html`)
        const html = await res.text()

        // Convert plain text into a DOM element
        const parser = new DOMParser()
        const doc = parser.parseFromString(html, "text/html")

        // Get the root of the DOM element
        const templateRoot = doc.body.firstElementChild
        if (!templateRoot)
            throw new Error(`Template empty: ${template}`)

        templates[template] = templateRoot
    }
}

// Clone a fetched template
export function getTemplate(type) {
    const template = templates[type]

    if (!template)
        throw new Error(`Template not preloaded: ${type}`)

    return template.cloneNode(true)
}