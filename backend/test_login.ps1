# PowerShell script to test the login endpoint
# Run this after the database tables are created

Write-Host "Testing login endpoint..." -ForegroundColor Yellow

# Test with the admin user
$loginData = @{
    email = "admin@plasticsurg.com"
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" -Method POST -ContentType "application/json" -Body $loginData
    Write-Host "✓ Login successful!" -ForegroundColor Green
    Write-Host "Access Token: $($response.access_token)" -ForegroundColor Cyan
    Write-Host "User Info:" -ForegroundColor Cyan
    Write-Host "  Name: $($response.user.name)" -ForegroundColor White
    Write-Host "  Email: $($response.user.email)" -ForegroundColor White
    Write-Host "  Role: $($response.user.role)" -ForegroundColor White
} catch {
    Write-Host "✗ Login failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    # Try to get more details from the error response
    if ($_.Exception.Response) {
        $errorStream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorStream)
        $errorBody = $reader.ReadToEnd()
        Write-Host "Response body: $errorBody" -ForegroundColor Red
    }
}

Write-Host "`nFrontend login request format check:" -ForegroundColor Yellow
Write-Host "Expected format: POST /api/auth/login" -ForegroundColor White
Write-Host "Content-Type: application/json" -ForegroundColor White
Write-Host "Body: {`"email`": `"user@domain.com`", `"password`": `"password`"}" -ForegroundColor White
