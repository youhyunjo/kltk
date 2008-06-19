EPYDOC := epydoc

apidoc: kltk epydoc-kltk.conf
	$(EPYDOC) --config epydoc-kltk.conf

