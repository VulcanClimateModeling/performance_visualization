#!/bin/bash
gprof2dot -f pstats ${1}/fv3core_${experiment}_${backend}_0.prof > profile.dot
dot -Tpng profile.dot -o profile.png
dot -Tpdf profile.dot -o profile.pdf