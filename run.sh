source ~/anaconda3/etc/profile.d/conda.sh

conda activate tf

killall xterm
cd dialog
xterm -hold -e "python grounder.py" &
xterm -hold -e "python dialog.py" &
xterm -hold -e "python android_interface_node.py" &
xterm -hold -e "python dummySentenceInput.py" &
sleep 15
xterm -hold -e "python ODsimulator.py" & # for loading saved images
cd probFoil
xterm -hold -e "python main.py" &

conda deactivate
rosbag record -a
echo "Oops, SYSTEM IS RUNNING!"
