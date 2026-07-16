$port = 5000
$endpoint = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any, $port)
$udpServer = New-Object System.Net.Sockets.UdpClient($port)

Write-Host "UDP Server listening on port $port... Press CTRL+C to stop."

try {
    while ($true) {
        $bytes = $udpServer.Receive([ref]$endpoint)
        $message = [System.Text.Encoding]::ASCII.GetString($bytes)
        Write-Host -NoNewline "Received from $($endpoint.Address):$($endpoint.Port) -> $message"
    }
} finally {
    Write-Host "Stopping..."
    $udpServer.Close()
}