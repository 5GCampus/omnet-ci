echo "#maingit" >> gitinfo.txt 
git rev-parse --abbrev-ref HEAD >> gitinfo.txt 2>&1
git rev-parse --verify HEAD >> gitinfo.txt 2>&1
echo "#submodules" >> gitinfo.txt
git submodule status >> gitinfo.txt 2>&1
echo "###Gitinfo###"
echo "#maingit"
git rev-parse --abbrev-ref HEAD  
git rev-parse --verify HEAD 
echo "#submodules"
git submodule status 
