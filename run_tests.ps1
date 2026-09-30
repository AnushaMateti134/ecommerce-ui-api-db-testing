Write-Host "========================================="
Write-Host " E-COMMERCE QA AUTOMATION TEST RUN"
Write-Host "========================================="

Write-Host ""
Write-Host "Starting test execution..."
Write-Host ""

pytest -v --html=reports/test-report.html --self-contained-html

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "========================================="
Write-Host " TEST EXECUTION COMPLETED"
Write-Host "========================================="

if ($exitCode -eq 0) {
    Write-Host "All tests passed."
}
else {
    Write-Host "Some tests failed."
}

Write-Host ""
Write-Host "HTML Report:"
Write-Host "reports/test-report.html"

Write-Host ""
Write-Host "Excel Report:"
Write-Host "ecommerce_QA_master_test_cases.xlsx"

exit $exitCode