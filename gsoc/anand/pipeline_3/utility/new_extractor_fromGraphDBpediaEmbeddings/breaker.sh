echo "Usage:    ./breaker.sh <size> <name of file to be split>" 
echo "Example:  ./breaker.sh 1000MB pageRank.txt" 
split -b $1  $2