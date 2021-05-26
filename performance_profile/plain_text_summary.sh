#!/bin/bash

# generate simple profile listing
cat > ./profile.py <<EOF
#!/usr/bin/env python3
import pstats
stats = pstats.Stats("$1/fv3core_${experiment}_${backend}_0.prof")
stats.strip_dirs()
print('=================================================================')
stats.sort_stats('time')
stats.print_stats(200)
print('=================================================================')
stats.sort_stats('cumulative')
stats.print_stats(200)
print('=================================================================')
stats.sort_stats('calls')
stats.print_stats(200)
print('=================================================================')
EOF
chmod 755 ./profile.py
./profile.py > profile.txt

# convert to html
mkdir -p html
echo "<html><body><pre>" > html/profile_overview.html
cat profile.txt >> html/profile_overview.html
echo "</pre></body></html>" >> html/profile_overview.html
