
#FILTERS = --lua-filter pandoc-proofs.lua --filter pandoc-xnos --filter pandoc-eqnos --filter pandoc-secnos --filter pandoc-theoremnos

FILTERS = --lua-filter pandoc-proofs.lua --filter pandoc-xnos --filter pandoc-eqnos --filter pandoc-secnos 

MACROS=assets/latex-macros.md

CMD=/home/george/.local/bin/course report

META=--metadata-file=assets/metadata.yaml
BEAMER_META=--metadata-file=assets/beamer-metadata.yaml

PD=pandoc --standalone --from markdown -V linkcolor:red \
    $(MACROS) $(FILTERS) --citeproc $(META)

PD_BEAMER=pandoc --standalone --from markdown --number-sections -V linkcolor:red \
    $(MACROS) $(FILTERS) --citeproc $(BEAMER_META)


YQ=yq -n '[inputs] | add'

CSS_DEFAULT="/home/george/Classes/AY2023-24--2023-fa--math51/assets/default.css"

VPATH = .:pacing:resources:problem-sets:lectures:Exams:practicum:Exam-review

logistic_dirs = resources pacing

logistics=$(wildcard *md,$(foreach fd, $(logistic_dirs), $(fd)/*.md))
logistics_pdf=$(logistics:.md=.pdf)
logistics_html=$(logistics:.md=.html)


lectures = $(wildcard lectures/*.md)
lectures_pdf = $(lectures:.md=.pdf)
lectures_html = $(lectures:.md=.html)
lectures_slides = $(lectures:.md=-slides.pdf)

problems_dirs = problem-sets Exams Exam-review practicum

content=$(foreach fd, $(problems_dirs), $(wildcard $(fd)/*.yaml))
content_json = $(content:.yaml=.json)
content_md = $(content_json:.json=.md) $(content_json:.json=--solutions.md)
content_pdf = $(content_md:.md=.pdf) 
content_tex = $(content_md:.md=.tex)

pacing = $(wildcard pacing/*.md)

all: pacing content lectures logistics 

pacing: $(pacing)

logistics: $(logistics_html) $(pacing_md) $(logistics_pdf) 

content: $(content_json) $(content_md) $(content_pdf) $(content_tex)

lectures:   $(lectures_html) $(lectures_slides) $(lectures_pdf)

MJ=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js
# MJ=http://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML

RP=.:problem-sets:lectures:exam1:pacing

%.json: %.yaml
	$(YQ) $< > $@

%--solutions.md: %.json
	problems -s $<

%.md: %.json
	problems $<

pacing/%.md: $(dhall)
	$(CMD) $(PWD)/Math051-AY2023-fall.dhall

resources/%.html: resources/%.md
	$(PD) $(META) $< --css=$(CSS_DEFAULT) --mathjax=$(MJ) --to html  -o $@

pacing/%.html: pacing/%.m
	$(PD) $(META) $< --css=$(CSS_DEFAULT) --mathjax=$(MJ) --to html  -o $@

%.html: %.md
	$(PD) $(META) $< assets/biblio.md --css=$(CSS_DEFAULT) --mathjax=$(MJ) --to html  -o $@

resources/%.pdf: resources/%.md
	$(PD) $(META) $< --pdf-engine=xelatex --resource-path=$(RP) --to pdf -o $@

pacing/%.pdf: pacing/%.md
	$(PD) $(META) $< --pdf-engine=xelatex --resource-path=$(RP) --to pdf -o $@

practicum/%.pdf: %.md
	$(PD) $(PRACTICUM_META) $< assets/biblio.md --pdf-engine=xelatex --resource-path=$(RP) --to pdf -o $@

practicum/%.tex: %.md
	$(PD) $(PRACTICUM_META) $< assets/biblio.md --resource-path=$(RP) --to latex -o $@

%.pdf: %.md
	$(PD) $(META) $< assets/biblio.md --pdf-engine=xelatex --resource-path=$(RP) --to pdf -o $@

%.tex: %.md
	$(PD) $(META) $< assets/biblio.md --resource-path=$(RP) --to latex -o $@

%-slides.pdf: %.md
	$(PD) $(BEAMER_META) $< assets/biblio.md --pdf-engine=xelatex -t beamer --incremental --resource-path=$(RP) -o $@


.PHONY = echoes

echoes:
	@echo Content: $(content_json) $(content_pdf) $(content_md)
	@echo Logistics: $(logistics)

.PHONY = clean

clean: clean_content clean_logistics clean_lectures

clean_content:
	-rm -f $(content_json) $(content_pdf)  $(content_md) $(content_tex)

clean_logistics:
	-rm -f $(logistics_html) $(pacing_md) $(logistics_pdf)

clean_lectures:
	-rm -f $(lectures_slides) $(lectures_pdf)  $(lectures_html)
