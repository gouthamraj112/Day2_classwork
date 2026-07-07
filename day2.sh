# 1. Create project directory structure
mkdir -p project/{src,docs,scripts,backup,archive}
 
# 2. Create required files
touch project/src/app.py
touch project/src/config.txt
touch project/docs/readme.md
touch project/scripts/deploy.sh
 
# 3. Copy files
cp project/src/config.txt project/backup/
 
# 4. Move files
mv project/docs/readme.md project/archive/
 
# 5. Rename files
mv project/src/app.py project/src/main.py
 
# 6. Search for specific files
find project -name "main.py"
find project -name "*.txt"
 
# 7. Set permissions on script
chmod 755 project/scripts/deploy.sh
 
# Verify permissions
ls -l project/scripts/deploy.sh
 
# 8. Compress project into a .tar.gz archive
tar -czvf project_backup.tar.gz project/
 
# 9. Extract archive to a new location
mkdir recovered_project
tar -xzvf project_backup.tar.gz -C recovered_project/
 
# 10. Verify final structure
tree recovered_project
 
# If tree is not installed
find recovered_project
