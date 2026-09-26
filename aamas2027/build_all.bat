@echo off
REM ===========================================================================
REM MASGym -- AAMAS 2027 build
REM
REM Produces TWO PDFs:
REM   main.pdf             the 8-page main-track paper (main content only)
REM   main_supplement.pdf  appendices, uploaded as separate supplementary material
REM
REM AAMAS allows at most 8 pages of main content plus any number of *reference*
REM pages, so the appendices must NOT live inside main.pdf.
REM
REM main.aux must exist before main_supplement.tex is compiled: the supplement
REM makes ~57 cross-references into the main paper via xr/externaldocument.
REM ===========================================================================
setlocal
cd /d "%~dp0"

echo === [1/4] main.pdf (pass 1) ===
pdflatex -interaction=nonstopmode main.tex > nul || goto :fail
bibtex main > nul

echo === [2/4] main.pdf (pass 2) ===
pdflatex -interaction=nonstopmode main.tex > nul || goto :fail

echo === [3/4] main_supplement.pdf ===
pdflatex -interaction=nonstopmode main_supplement.tex > nul || goto :fail
bibtex main_supplement > nul

echo === [4/4] finalising cross-references ===
pdflatex -interaction=nonstopmode main.tex > nul || goto :fail
pdflatex -interaction=nonstopmode main_supplement.tex > nul || goto :fail
pdflatex -interaction=nonstopmode main_supplement.tex > nul || goto :fail

echo.
echo === DONE ===
for %%F in (main.pdf main_supplement.pdf) do (
  if exist %%F (
    for %%A in (%%F) do echo   %%~nxA  %%~zA bytes
  ) else (
    echo   MISSING: %%F
  )
)
echo.
echo Page counts (verify main content is <= 8 pages before references):
pdfinfo main.pdf 2^> nul | findstr /C:"Pages"
pdfinfo main_supplement.pdf 2^> nul | findstr /C:"Pages"
goto :eof

:fail
echo.
echo *** BUILD FAILED -- see main.log / main_supplement.log ***
exit /b 1
