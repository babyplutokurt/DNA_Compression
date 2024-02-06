Sort FastQ based on entry ID: \
gzcat test_1000_small_lossless.fastq.gz | paste - - - - | sort -k1,1 -S 3G | tr '\t' '\n' | gzip > Sorted_test_1000_small_lossless.fastq.gz \
FaStore: \
./scripts/fastore_compress.sh --lossy --in test_1000.fq --out COMP --threads 8 \
