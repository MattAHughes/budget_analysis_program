# budget_analysis_program
A program written in Python that allows the input of a basic budget and creates a quick pdf report (requires miktex for compilation)

The video contains a packaged executable version of the same app.

![visuals](trial_video.gif)

V.1.2 contains small quality of life upgrades to the original program including sorted tabulated and plotted data for ease of interpretation and moves the report generation functionality to its own class to simplify reading of the program.

V 1.4 involves significant changes, including changing the reports to excel, pdf, and html formats, however the wkhtmltopdf.zip file in the .\pdf_creation_dependancy\wkhtmltox-0.12.4_msvc2015-win64\bin folder requires extraction to the bin folder, being too large to upload uncompressed (~27 mb). This change removes the LaTeX dependancy soremoves the need to install that.

V 1.5 improves speed from V 1.4, and removes the need to extract further programs (works in a self-contained manner). The new functionality is as below.

![visuals](new_trial.gif)
