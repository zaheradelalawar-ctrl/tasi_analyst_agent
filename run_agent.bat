@echo off
TITLE TASI 19-Institution Consensus and Ranking Agent
color 0A

echo =================================================================
echo   TASI 19-INSTITUTION CONSENSUS AND RANKING AGENT RUNNER
echo =================================================================
echo.

:: Navigate to the script directory
cd /d "%~dp0"

:: Run the Python agent and store the filename in a variable or capture latest
for /f "tokens=*" %%i in ('python -c "from datetime import datetime; print(f'TASI_19_Institutions_Ranked_{datetime.now().strftime(\"%%Y%%m%%d_%%H%%M\")}.xlsx')"' ) do set EXCEL_FILE=%%i

echo Running ingestion and aggregation pipeline...
python main.py --out "%EXCEL_FILE%"

echo.
echo =================================================================
echo   EXECUTION COMPLETE. OPENING EXCEL REPORT...
echo =================================================================

:: Automatically launch the generated Excel workbook
start "" "%EXCEL_FILE%"

pause