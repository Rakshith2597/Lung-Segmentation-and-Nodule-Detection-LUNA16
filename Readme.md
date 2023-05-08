﻿# Lung Segmentation and Nodule Detection in Computed Tomography Scan using a Convolutional Neural Network Trained Adversarially using Turing Test Loss

> _Also available in [OpenVINO Toolkit](https://github.com/openvinotoolkit/training_extensions/tree/misc/misc/pytorch_toolkit/lung_nodule_detection)_ 

Lung cancer is the most common form of cancer found worldwide with a high mortality rate. Early detection of pulmonary nodules by screening with a low-dose computed tomography (CT) scan is crucial for its effective clinical management. Nodules which are symptomatic of malignancy occupy about 0.0125 - 0.025% of volume in a CT scan of a patient. Manual screening of all slices is a tedious task and presents a high risk of human errors. To tackle this problem we propose a computationally efficient two-stage framework. In the first stage, a convolutional neural network (CNN) trained adversarially using Turing test loss segments the lung region.
In the second stage, patches sampled from the segmented region are then classified to detect the presence of nodules. The proposed method is experimentally validated on the LUNA16 challenge dataset with a dice coefficient of **0.984 ± 0.0007** for 10-fold cross-validation.


>**Paper** : R. Sathish, R. Sathish, R. Sethuraman and D. Sheet, **"Lung Segmentation and Nodule Detection in Computed Tomography Scan using a Convolutional Neural Network Trained Adversarially using Turing Test Loss"** ,2020 42nd Annual International Conference of the IEEE Engineering in Medicine & Biology Society (EMBC), 2020. </br> 

> _Access the paper via_ 
[IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/9175649) [ArXiv](https://arxiv.org/abs/2006.09308).

BibTeX reference to cite, if you use it:

```bibtex
@INPROCEEDINGS{9175649,
  author={Sathish, Rakshith and Sathish, Rachana and Sethuraman, Ramanathan and Sheet, Debdoot},
  booktitle={2020 42nd Annual International Conference of the IEEE Engineering in Medicine & Biology Society (EMBC)}, 
  title={Lung Segmentation and Nodule Detection in Computed Tomography Scan using a Convolutional Neural Network Trained Adversarially using Turing Test Loss}, 
  year={2020},
  volume={},
  number={},
  pages={1331-1334},
  doi={10.1109/EMBC44109.2020.9175649}}
```
## Dataset used

 The proposed method is experimentally validated by performing 10-fold cross-validation on the LUNA16 challenge dataset. 
 >Dataset download page: [https://luna16.grand-challenge.org/](https://luna16.grand-challenge.org/) 

The dataset consists of CT volumes from 880 subjects, provided as ten subsets for 10-fold cross-validation. In each fold of the experiment, eight subsets from the dataset were used for training and one each for validation and testing. The annotations provided includes binary masks for lung segmentation and, coordinates and spherical diameter of nodules present in each slice. LIDC-IDRI dataset from which LUNA16 is derived has nodule annotations in the form of contours which preserves its actual shape. Therefore, we use annotations from LUNA dataset only in Stage 1. The annotations for the nodules from the LIDC dataset is used in Stage 2 (nodule detection) to determine the presence of nodules in image patches.
> Dataset download page: [https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI](https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI)

The ground truth annotations were marked in a two-phase image annotation process performed by four experienced thoracic radiologists. Systematic sampling of slices from the CT volumes was performed to ensure equal distribution of slices with and without the presence of nodules.

>**Note**: Systematically sampled slice numbers/images to be used are given in the repository inside the data preparation folder.

>**License**: Both the datasets are published by the creators under [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/)


## Code and Directory Organization

lung_nodule_detection/
	src/
      utils/
        data_prep/
            create_folds.py
            generate_patches.py
            generate_slices.py
            visualize.py
        downloader.py
        data_loader.py
        exporter.py
        get_config.py
        models.py
        infer_stage1.py
        infer_stage2.py
        train_stage1.py
        train_stage2.py
        utils.py
      export.py
      inference.py
      train.py
      prepare_data.py
	configs/
      stage1_config.json
      stage2_config.json
      download_config.json
  media/
	tests/
      test_export.py
      test_inference.py
      test_train.py
	init_venv.sh
	README.md
	requirements.txt
	setup.py

## System Specifications

The code and models were tested on system with the following hardware and software specifications.
- Ubuntu* 16.04
- Python* 3.6
- NVidia* GPU for training
- 16GB RAM for inference

# Using the code

## Creating Virtual Environment
Create a virtual environment with all dependencies using 
```
sh init_venv.sh
```
The network used in stage 1, lung segmentation relies on MaxUnpool2D operation. This operation is not supported for ONNX and IR conversions in its current versions. As a work around we use [openvino_pytorch_layers](https://github.com/dkurt/openvino_pytorch_layers) and [max_unpool2d_decomposition.py](https://github.com/openvinotoolkit/openvino/pull/11400/files).

After creating the virtual environment, users need to keep the `openvino_pytorch_layers` in the `src/utils/` directory and `max_unpool2d_decomposition.py` in `venv/lib/python3.9/site-packages/openvino/tools/mo/front/onnx/` directory.

Thanks to [@dkurt](https://github.com/dkurt) for the solution. Users can follow the entire discussion [here](https://github.com/dkurt/openvino_pytorch_layers/issues/40).

>**Note** This is needed only for exporting and inferencing the ONNX and IR model.

## Data Preparation
Follow the below steps to prepare and organise the data for training.
> Details about the arguments being passed and its purpose is explained within the code. To see the details run `python prepare_data.py -h`

> Make sure the dataset has been properly downloaded and extracted before proceeding.

1. ` python prepare_data.py  --genslices --masktype <type> --datasetpath <path> --save_path <path>  `
	This step extracts induvidual CT slices from the CT volumes provided in the dataset. Each of these slices are saved seperately as npy files with filename in the format `[series_uid]_slice[sliceno].npy`.
	Perform the above step for masktype nodule and lung seperately before proceeding to the next step.

2. `python prepare_data.py --createfolds --datapath <path> --savepath <path>
--datasetpath <path> `
	The above step first classifies the slices into two categories, positive and negative based on the presence of nodules in them. On completion, the dataset which consists of CT volumes from 880 subjects, provided as ten subsets are divided into 10-folds for cross-validation. In each fold of the experiment, eight subsets from the dataset are separated for training and one each for validation and testing. A balanced dataset consisting of an equal number (approx.) of positive and negative slices is identified for each fold. Filenames of these slices of each fold are stored in separate JSON files.

3. `python prepare_data.py --genpatch --jsonpath <path> --foldno <int> --category <type> --data_path <path> --lungsegpath <path> --savepath <path> --patchtype <type> `
	The above step generates patches which are used to train the classifier network.

4. `python prepare_data.py --visualize --seriesuid <str> --sliceno <int> --datapath <path> --savepath <path>`
	To visualize a particular slice use the above line. 

## Training

> Details about the arguments being passed and its purpose is explained within the code. To see the details run `python train_network.py -h`

To train the lung segmentation network without the discriminator execute the following line of code.
`python train_network.py --lungseg --foldno <int> --savepath <path> --jsonpath <path> --datapath <path> --lungsegpath <path> --network <str> --epochs <int:optional> `

To train the lung segmentation network with discrimator and turing test loss, execute 
`python train_network.py --lungsegadv --foldno <int> --savepath <path> --jsonpath <path> --datapath <path> --lungsegpath <path> --network <str> --epochs <int:optional> `

To train the patch classifier network execute
`python patch_classifier --savepath <path> --imgpath <path> --epochs <int:optional> `


## Evaluation

> Details about the arguments being passed and its purpose is explained within the code. To see the details run `python inference.py -h`

To evaluate the segmentation models execute
 `python inference.py --lunseg --foldno <int> --savepath <path> --jsonpath <path> --network <str>`

To evaluate the classifier network execute
`python inference.py --patchclass --savepath <path> --imgpath <path>`

## Pre-trained Models

Pretrained models for inference are available [here](http://kliv.iitkgp.ac.in/projects/miriad/model_weights/bmi11/model_weights.zip). Users can also use the `downloader.py` script in utils directory to download the model.

## Run Tests

Necessary unit tests have been provided in the tests directory. The sample/toy dataset to be used in the tests can also be downloaded from [here](http://kliv.iitkgp.ac.in/projects/miriad/sample_data/bmi11/test_data.zip).

>**Note**: Unit tests for inference using ONNX model is commented/disabled at the moment as MaxUnpool2D operation is yet to be supported in onnxruntime. 

## Acknowledgement

 This work is undertaken as part of Intel India Grand Challenge 2016 Project MIRIAD: Many Incarnations of Screening of Radiology for High Throughput Disease Screening via Multiple Instance Reinforcement Learning with Adversarial Deep Neural Networks, sponsored by Intel Technology India Pvt. Ltd., Bangalore, India.

**Principal Investigators**

<a href="https://www.linkedin.com/in/debdoot/">Dr Debdoot Sheet</a>,<a href="http://www.iitkgp.ac.in/department/EE/faculty/ee-nirmalya"> Dr Nirmalya Ghosh (Co-PI) </a></br>
Department of Electrical Engineering,</br>
Indian Institute of Technology Kharagpur</br>
email: debdoot@ee.iitkgp.ac.in, nirmalya@ee.iitkgp.ac.in

<a href="https://www.linkedin.com/in/ramanathan-sethuraman-27a12aba/">Dr Ramanathan Sethuraman</a>,</br>
Intel Technology India Pvt. Ltd.</br>
email: ramanathan.sethuraman@intel.com

**Contributor**

The codes/model was contributed by

<a href="https://github.com/Rakshith2597"> Rakshith Sathish</a>,</br>
Advanced Technology Development Center,</br>
Indian Institute of Technology Kharagpur</br>
email: rakshith.sathish@kgpian.iitkgp.ac.in</br>
Github username: Rakshith2597

## References

<div id="densenet">
<a href="#abs">[1]</a> R. Sathish, R. Sathish, R. Sethuraman, D. Sheet.Lung Segmentation and Nodule Detection in Computed Tomography Scan using a Convolutional Neural Network Trained Adversarially using Turing Test Loss. In Proceedings of 42nd Annual International Conference of the IEEE Engineering in Medicine & Biology Society (EMBC), 2020. <a href="https://ieeexplore.ieee.org/abstract/document/9175649"> (link) </a> 
</div>
