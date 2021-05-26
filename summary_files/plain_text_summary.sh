#================== WARNING: experimental stuff below
ROOT_DIR=`pwd`
git clone git@github.com:vulcanclimatemodeling/fv3core.git tmpdir
cd tmpdir 
git checkout master
cat > list_commits.sh <<'EOF'
#!/bin/bash
echo "                    timings file |  git hash |     mainloop per timestep"
echo "---------------------------------|-----------|--------------------------"
for f in `/bin/ls -1d $1/*_summary.json | grep -v memory_usage | tac` ; do
  filename=`basename "${f}"`
  grep -q "${experiment}" ${f} || continue
  hash=`grep '"hash":' ${f} | sed 's/.* "//g' | sed 's/".*//g'`
  branch=`git branch master --contains ${hash} 2>/dev/null | cut -c3-`
  mainloop=`sed -n /mainloop/,/total/p ${f} | grep mean_of_medians | awk '{print $2}' | sed 's/,.*//g'`
  if [ "${branch}" == "master" ] ; then
    if [ -n "${previous_hash}" ] ; then
      git log --oneline ${hash}..${previous_hash} 2>/dev/null | sed 's/^/  /'
    fi
    previous_hash=${hash}
  else
    echo "  <not on master>"
  fi
  short_hash=`git rev-parse --short ${hash}`
  mainloop=`printf %10.3f ${mainloop}`
  echo "${filename} |   ${short_hash} | ${mainloop}s"
done
EOF
chmod 755 list_commits.sh
echo "========================================" | tee commits.txt
./list_commits.sh $1 | tee -a commits.txt
echo "========================================" | tee -a commits.txt
mkdir -p html
echo "<html><body><pre>" > $ROOT_DIR/html/performance_history.html
cat commits.txt >> $ROOT_DIR/html/performance_history.html
echo "</pre></body></html>" >> $ROOT_DIR/html/performance_history.html
cd -
rm -rf tmpdir
exit 0