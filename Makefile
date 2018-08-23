CHECKPOINT_EXPERIMENTS=

WRITE_CP=--write-files
NO_WRITE_CP=--no-write-files

CODE_FILES=run-intervals.sh async_experiment.py

plots: plot_checkpoint_sizes.pdf plot_orders.pdf

plot_checkpoint_sizes.pdf: results-2-1600.txt results-2-16000.txt results-2-160000.txt baseline-2.txt make_graph.py
	python make_graph.py -f results-2-1600.txt 1600 -f results-2-16000.txt 16000 -f results-2-160000.txt 160000 -t "Slowdown attributed to checkpointing for differing checkpoint sizes" -x "interval" -b baseline-2.txt -o plot_checkpoint_sizes.pdf

plot_orders.pdf: results-2-16000.txt results-4-16000.txt results-8-16000.txt results-16-16000.txt baseline-2.txt baseline-4.txt baseline-8.txt baseline-16.txt make_graph.py
	python make_graph.py -f results-2-16000.txt "Order 2" -b baseline-2.txt -f results-4-16000.txt "Order 4" -b baseline-4.txt -f results-8-16000.txt "Order 8" -b baseline-8.txt -f results-16-16000.txt "Order 16" -b baseline-16.txt -t "Slowdown attributed to checkpointing for different stencil orders (computational intensity)" -o plot_orders.pdf


results-2-%.txt: $(CODE_FILES)
	sh run-intervals.sh 2 $* $(WRITE_CP) | tee $@

results-4-%.txt: $(CODE_FILES)
	sh run-intervals.sh 4 $* $(WRITE_CP) | tee $@

results-8-%.txt: $(CODE_FILES)
	sh run-intervals.sh 8 $* $(WRITE_CP) | tee $@

results-16-%.txt: $(CODE_FILES)
	sh run-intervals.sh 16 $* $(WRITE_CP) | tee $@

baseline-%.txt: $(CODE_FILES)
	sh run-intervals.sh $* 0 $(NO_WRITE_CP) | tee $@

clean:
	rm -rf tmp
	mkdir tmp
