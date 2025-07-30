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

    const response = await fetch('/api/generate', {
      method: 'POST',
      body: formData
    })

    const data = await response.json()
    setResult(data.bat_content)
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">WireGuard Route Generator</h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">WG Config File</label>
            <div className="mt-1 flex items-center">
              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Gateway</label>
            <input
              type="text"
              value={gateway}
              onChange={(e) => setGateway(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
              placeholder="0.0.0.0"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Extra IPs (comma-separated)</label>
            <input
              type="text"
              value={extraIPs}
              onChange={(e) => setExtraIPs(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
              placeholder="192.168.1.0/24,10.0.0.0/8"
            />
          </div>

          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Generate BAT File
          </button>
        </form>

        {result && (
          <div className="mt-6">
            <h2 className="text-lg font-medium text-gray-900 mb-2">Result:</h2>
            <pre className="bg-gray-50 p-4 rounded-md overflow-x-auto text-sm">{result}</pre>
            <button
              onClick={() => navigator.clipboard.writeText(result)}
              className="mt-2 inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded shadow-sm text-white bg-green-600 hover:bg-green-700"
            >
              Copy to Clipboard
            </button>
          </div>
        )}
      </div>
    </div>
  )
}