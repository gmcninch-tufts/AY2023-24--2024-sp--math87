
CMD=/home/george/.local/bin/course report

PD=pandoc --from markdown -V linkcolor:red 
GC = google-chrome --headless 

TEX=pdflatex

SLIDEOUS=assets/slideous

CSS_DEFAULT="assets/default.css"
CSS_PANDOC="assets/pandoc.css"

VPATH = .:pacing:resources:problem-sets:notebooks

content_dirs=notebooks problem-sets
logistic_dirs=resources pacing

contents=$(wildcard *md,$(foreach fd, $(content_dirs), $(fd)/*.md))

contents_nb=$(contents:.md=.ipynb)
contents_html=$(contents:.md=.html)
contents_pdf=$(contents:.md=.pdf)

logistics=$(wildcard *md,$(foreach fd, $(logistic_dirs), $(fd)/*.md))
logistics_pdf=$(logistics:.md=.pdf)
logistics_html=$(logistics:.md=.html)

pacing_md = $(wildcard pacing/*.md)

notebooks = $(patsubst %.md,%.ipynb,$(wildcard notebooks/*.md)) 


all: contents logistics

logistics: logistics_pdf logistics_html
contents: $(contents_nb) $(contents_html) $(contents_pdf)

MJ=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js
# MJ=http://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML

RP=.:problem-sets:lecture-summaries:exam1:exam2

pacing/%.md: Math135-AY2023-spring.dhall topics/lectures.dhall topics/recitations.dhall topics/assignments.dhall
	$(CMD) $<	


%.html: %.md
	$(PD) $<  --standalone --css=$(CSS_DEFAULT) --mathjax=$(MJ) --to html  -o $@

%.pdf: %.md
	$(PD) --self-contained --pdf-engine=xelatex  $<  -o $@


# problem-sets/%.html: %.md
# 	$(PD)  --citeproc --self-contained --to html --resource-path=$(RP) -t latex $<  -o $@


# problem-sets/%.pdf: %.md
# 	$(PD)  --citeproc --self-contained --pdf-engine=xelatex --resource-path=$(RP) -t latex $<  -o $@


notebooks/%.ipynb: %.md
	$(PD) $< --to ipynb  -o $@


.PHONY: echoes

echoes:
	@echo $(contents_nb)
	@echo $(contents_html)
	@echo $(contents_pdf)
#	@echo $(lectures2)
#	@echo $(PDF)


.PHONY = clean

clean: clean_nb clean_pdf clean_html

clean_nb:
	-rm -f $(contents_nb)

clean_pdf:
	-rm -f $(logistics_pdf) $(contents_pdf)

clean_html:
	-rm -f $(logistics_html) $(contents_html)

