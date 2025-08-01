@echo off
REM AI Blog Generator Runner for Windows
REM Usage: generate_blog.bat "your blog topic here"

if "%~1"=="" (
    echo Usage: generate_blog.bat "your blog topic here"
    echo Example: generate_blog.bat "Drake Cutlass Red medical ship guide"
    pause
    exit /b 1
)

echo Starting AI Blog Generator...
python blog_generator.py "%~1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Blog generation failed. Check the error messages above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Blog generation completed successfully!
pause
