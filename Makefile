
CMD=/home/george/.local/bin/course report

PD=pandoc --from markdown -V linkcolor:red 
GC = google-chrome --headless 

TEX=pdflatex

SLIDEOUS=assets/slideous

CSS_DEFAULT="assets/default.css"
CSS_PANDOC="assets/pandoc.css"

VPATH = .:pacing:resources:problem-sets:notebooks

resources = $(patsubst %.md,%.html,$(wildcard resources/*.md)) \
            $(patsubst %.md,%.pdf,$(wildcard resources/*.md)) \

pacing_md   = $(wildcard pacing/*.md)

pacing_html = $(patsubst %.md,%.html,$(wildcard pacing/*.md)) 
pacing_pdf  = $(patsubst %.md,%.pdf,$(wildcard pacing/*.md)) 

psets = $(patsubst %.md,%.html,$(wildcard problem-sets/*.md)) \
        $(patsubst %.md,%.pdf, $(wildcard problem-sets/*.md)) 



notebooks = $(patsubst %.md,%.ipynb,$(wildcard notebooks/*.md)) 


all: pacing resources psets notebooks

pacing: $(pacing_md) $(pacing_html) $(pacing_pdf)
resources: $(resources)
psets: $(psets)
notebooks: $(notebooks)

MJ=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js
# MJ=http://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML

RP=.:problem-sets:lecture-summaries:exam1:exam2

pacing/%.md: Math135-AY2023-spring.dhall topics/lectures.dhall topics/recitations.dhall topics/assignments.dhall
	$(CMD) $<	


pacing/%.html resources/%.html: %.md
	$(PD) $<  --standalone --css=$(CSS_DEFAULT) --mathjax=$(MJ) --to html  -o $@

pacing/%.pdf resources/%.pdf: %.md
	$(PD) --self-contained --pdf-engine=xelatex  $<  -o $@


problem-sets/%.html: %.md
	$(PD)  --citeproc --self-contained --to html --resource-path=$(RP) -t latex $<  -o $@


problem-sets/%.pdf: %.md
	$(PD)  --citeproc --self-contained --pdf-engine=xelatex --resource-path=$(RP) -t latex $<  -o $@


notebooks/%.ipynb: %.md
	$(PD) $< --to ipynb  -o $@


problem-sets/%.html  lecture-summaries/%.html: %.md
	$(PD) $<  --citeproc  --standalone --css=$(CSS_DEFAULT) --mathjax=$(MJ) --to html  -o $@

.PHONY = clean

clean: clean_pdf clean_resources clean_psets clean_lectures

clean_pacing:
	-rm -f $(pacing_html) $(pacing_pdf)

clean_psets:
	-rm -f $(psets)

clean_rep_thy:
	-rm -f $(rep_thy)

clean_resources:
	-rm -f $(resources)
