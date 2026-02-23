async function getResources() {
  const res = await fetch("http://localhost:5000/resources")
  
  if (!res.ok)
    throw new Error("Server error")

  return res.json()
}