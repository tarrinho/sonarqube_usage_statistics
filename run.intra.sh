echo `date`
echo $SONARQUBE_URL
current_file="sonarqube.extract.intra.csv"
new_file="sonarqube.extract.intra.csv.tmp"

sonarqube_stats.intra.py >> "$new_file" 

new_size=$(ls -la "$new_file" | awk '{print $5}' )
current_size=$(ls -la "$current_file" | awk '{print $5}' )

if (( $new_size > $current_size )) ; then
    echo "New file is bigger, will substitute it!"
    $(cp "$new_file" "$current_file")
else
    echo "No changes!"
fi
