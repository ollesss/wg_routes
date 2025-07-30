import { useState } from 'react'

export default function App() {
  const [gateway, setGateway] = useState('0.0.0.0')
  const [file, setFile] = useState(null)
  const [extraIPs, setExtraIPs] = useState('')
  const [result, setResult] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    const formData = new FormData()
    if (file) formData.append('config', file)
    formData.append('gateway', gateway)
    formData.append('extra_ips', extraIPs)

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      setResult(data.bat_content)
    } catch (error) {
      console.error("Error:", error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold mb-6">WireGuard Route Generator</h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-2">WG Config File</label>
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block mb-2">Gateway</label>
            <input
              type="text"
              value={gateway}
              onChange={(e) => setGateway(e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="0.0.0.0"
            />
          </div>

          <div>
            <label className="block mb-2">Extra IPs (comma-separated)</label>
            <input
              type="text"
              value={extraIPs}
              onChange={(e) => setExtraIPs(e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="192.168.1.0/24,10.0.0.0/8"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
          >
            Generate BAT File
          </button>
        </form>

        {result && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-2">Result:</h2>
            <pre className="bg-gray-100 p-4 rounded overflow-x-auto">{result}</pre>
            <button
              onClick={() => navigator.clipboard.writeText(result)}
              className="mt-4 bg-green-600 text-white py-1 px-3 rounded hover:bg-green-700"
            >
              Copy to Clipboard
            </button>
          </div>
        )}
      </div>
    </div>
  )
}