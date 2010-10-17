EPYDOC := epydoc

python-kltk-apidoc: lib/python2.6/kltk epydoc-kltk.conf
	$(EPYDOC) --config epydoc-kltk.conf

