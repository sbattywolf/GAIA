param(
  [Parameter(Mandatory=$true)]
  [string]$Token,
  [string]$Endpoint = 'https://api.github.com/user'
)

try {
  $headers = @{ Authorization = "token $Token"; 'User-Agent' = 'gaia-smoke-check' }
  $resp = Invoke-RestMethod -Uri $Endpoint -Headers $headers -Method Get -ErrorAction Stop
  Write-Output "Smoke check OK: received response with properties: $($resp.PSObject.Properties.Name -join ', ')"
  exit 0
} catch {
  Write-Error "Smoke check failed: $($_.Exception.Message)"
  exit 3
}
