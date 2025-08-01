# AI Blog Generator Runner for PowerShell
# Usage: .\generate_blog.ps1 "your blog topic here"

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Topic
)

Write-Host "🚀 Starting AI Blog Generator..." -ForegroundColor Green
Write-Host "Topic: $Topic" -ForegroundColor Cyan

try {
    python blog_generator.py $Topic
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n🎉 Blog generation completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Blog generation failed with exit code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "`n💥 An error occurred: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
