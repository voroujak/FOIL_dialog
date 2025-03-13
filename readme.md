## Dialog system with visual and auditory perceptions of Pepper robot

This repo is the implmentation of a dialog system for a robot with visual and auditory perception, with probFOIL, in ROS. The system is described in the paper: "Towards abstract relational learning in human robot interaction", see the citation. 
It requires ROS, an anaconda environment with Python 2.7 for naoqi, and Python 3+ for all other modules. 
For running the code, you can run run.sh. It automatically activate virtual environments, and create 6 terminals for different create multiple terminal, in two anaconda virtual environments of Python 2.7 and 3.+. 


##Notes: 
1. In this repo, images are from saved images from Pepper robot, and audito perception is through ROS_android_interface. To run the code with bridge of auditory and visual perception to Pepper robot, you should use PepperBridge repository. Particularly, you feed ROS nodes of "/iFoil/OD" and "/naoqi_TTS/replyBack" and "/naoqi_ASR/bestSpeechHypothesis" from the Pepper Bridge. 

2. In run.sh, only Python 3 virtual environment with tensorflow is activated. Python 2.7 is required by the robot in PepperBridge repo.


## Structure of this project:

In the root, can find an example interaction, run.sh and all object category labels. There are five folder, as following:

- dialog: This is the main folder that has all the modules required for the dialog. In this folder the main code is dialog.py, where it run and call modules and ROS nodes, wait for input speech, and give a response. 
- croppedImage and images: some example images of the images recorded by the Pepper robot. 
- probFOIL: It creates nodes that listen to the scene model on ROS, create a probFOIL problem, and compute a logical formula that describes the latent relationships between attribute of objects.
- retinaNet: Download the keras retinaNet model and extract it in this folder.


## Citation:
If you use this project in your work, please cite: 

@article{faridghasemnia2020towards,
  title={Towards abstract relational learning in human robot interaction},
  author={Faridghasemnia, Mohamadreza and Nardi, Daniele and Saffiotti, Alessandro},
  journal={arXiv preprint arXiv:2011.10364},
  year={2020}
}

@inproceedings{faridghasemnia2019capturing,
  title={Capturing frame-like object descriptors in human augmented mapping},
  author={Faridghasemnia, Mohamadreza and Vanzo, Andrea and Nardi, Daniele},
  booktitle={AI* IA 2019--Advances in Artificial Intelligence: XVIIIth International Conference of the Italian Association for Artificial Intelligence, Rende, Italy, November 19--22, 2019, Proceedings 18},
  pages={392--404},
  year={2019},
  organization={Springer}
}
