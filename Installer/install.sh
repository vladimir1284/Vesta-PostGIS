#!/bin/bash
#
# Install vesta-postgis on Centos5 
# Run as CODE user
# 

echo
echo "Vesta|Postgis "$(inst/version.sh)
echo 

if [[ $HOME == "/root" ]]; then
  echo "please run as CODE user (not root) !! "
  echo
  exit 1
fi

# set working directories
dist_dir=`pwd`

# Switch RDA and comm config files
rm $HOME/cfg/comms_link.conf
rm $HOME/cfg/tcp.conf
mnttsk_switch_orda -t orda
cp inst/comms_link.conf $HOME/cfg 
cp inst/tcp.conf $HOME/cfg 
cp inst/vesta_postgis.dat $HOME/cfg

# Get radar ID
radar_id=$(grep rpg_name $HOME/cfg/site_info.dea | awk '{print $2;}')
echo
echo "Radar ID: "$radar_id
echo 

# Executables files
postgis_file="run_vesta_postgis2.sh"
run_postgis_file=$HOME"/tools/bin/lnux_x86/"$postgis_file
sed -e "s|\$radar|$radar_id|g" inst/$postgis_file > $run_postgis_file
chmod +x $run_postgis_file

rpg_file="run_vesta_rpg2.sh"
run_rpg_file=$HOME"/tools/bin/lnux_x86/"$rpg_file
cp inst/$rpg_file $run_rpg_file
chmod +x $run_rpg_file

# Task to rc.local
while [[ $(grep $rpg_file /etc/rc.local) == "" ]]; do
  echo "Please enter root password to modify rc.local"
  su -c "( echo su $USER -c \'$rpg_file -b\' >> /etc/rc.local; )"
  echo
done

# Copying binaries
bin_files_dir=$HOME/"vesta_postgis"

if [[ ! -e $bin_files_dir ]]; then
    mkdir $bin_files_dir
else 
    rm -r $bin_files_dir
    mkdir $bin_files_dir
fi

cp vesta_postgis $bin_files_dir
cp -r Binary_Packages $bin_files_dir
cp -r Phenomenon $bin_files_dir
cp -r ProductBlocks $bin_files_dir
cp -r palettes $bin_files_dir
cp Vesta-PostGIS.py $bin_files_dir
cp Vesta-PostGIS.py $bin_files_dir
cp SiteConfiguration.py $bin_files_dir
cp products_properties.xml $bin_files_dir
cp ProductProperties.py $bin_files_dir
cp Palette.py $bin_files_dir
cp ImageUpload.py $bin_files_dir
cp GraphicProduct.py $bin_files_dir
cp runolds.py $bin_files_dir
# Create images dirs
mkdir $bin_files_dir/images
mkdir $bin_files_dir/images/CLBJ
mkdir $bin_files_dir/images/CCSB
mkdir $bin_files_dir/images/CPDE
mkdir $bin_files_dir/images/CPSJ
mkdir $bin_files_dir/images/CCMW
mkdir $bin_files_dir/images/CPLN
mkdir $bin_files_dir/images/CHLG
mkdir $bin_files_dir/images/CGPD


