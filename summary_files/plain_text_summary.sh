#================== WARNING: experimental stuff below

cat > list_commits.sh <<'EOF'
#!/bin/bash
git clone git@github.com:vulcanclimatemodeling/fv3core.git tmpdir
cd tmpdir 
git checkout master
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
cd -
rm -rf tmpdir
EOF
chmod 755 list_commits.sh
echo "========================================" | tee commits.txt
./list_commits.sh $1 | tee -a commits.txt
echo "========================================" | tee -a commits.txt

mkdir -p html
echo "<html><body><pre>" > html/index.html
cat commits.txt >> html/index.html
echo "</pre></body></html>" >> html/index.html


exit 0