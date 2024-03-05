#FILTERS = --lua-filter pandoc-proofs.lua --filter pandoc-xnos --filter pandoc-eqnos --filter pandoc-secnos
FILTERS = --lua-filter pandoc-proofs.lua #--filter pandoc-xnos --filter pandoc-eqnos --filter pandoc-secnos 

PD=pandoc --standalone --from markdown -V linkcolor:red \
    $(MACROS) $(FILTERS) --citeproc $(META)

CSS_DEFAULT = ../assets/default.css

MJ=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js

VPATH = .:pacing:resources:problem-sets:lectures:Exams:practicum:Exam-review:working

notebooks = $(wildcard notebooks-pending/*.md)
notebooks_j =$(notebooks:.md=.ipynb)

working = $(wildcard working/*.md)
working_html = $(working:.md=.html)
working_pdf = $(working:.md=.pdf)

problems = $(wildcard problem-sets/*.md)

all: $(notebooks_j) working

working: $(working_html) $(working_pdf)

%.ipynb: %.md
	$(PD) $< -o $@

%.html: %.md
	$(PD) $(META) $< --css=$(CSS_DEFAULT)  --mathjax=$(MJ) --to html  -o $@


%.pdf: %.md
	$(PD) $(META) $<  --resource-path=working --extract-media=. --pdf-engine=xelatex  --to pdf -o $@



.PHONY = echoes

echoes:
	@echo Content: $(content_json) $(content_pdf) $(content_md)
	@echo Logistics: $(logistics)

.PHONY = clean

clean: clean_work

clean_work:
	-rm -f $(working_html) $(working_pdf)
