#!/bin/bash

data_prefix='/home/work/Projects/workstudy/data/'
project_dir='/home/work/Projects/workstudy/facade-model/deep-photo-styletransfer/trials/'

while getopts "i:s:D:" OPTION
do
	case $OPTION in
		i)
			input_id=$OPTARGinput_id
			echo "using input id ${input_id}"
			;;
		s)
			style_id=$OPTARG
			echo "using style id ${style_id}"
			;;
		D)
			data_source=$OPTARG
			echo "using database ${data_source}"
			;;
	esac
done

if [ "$data_source" = "DPST" ]
then
	echo using DPST as the data source...
	data_dir=$data_prefix"DPST/"

	echo Copying input image ${input_id} from DPST...
	cp ${data_dir}"input/in"$input_id".png" ${project_dir}"input/"
	echo done

	echo Copying input image segmentation ${input_id} from DPST...
	cp ${data_dir}"input_seg/in"$input_id".seg.png" ${project_dir}"input_seg/"
	echo done

	echo Copying style image ${style_id} from DPST...
	cp ${data_dir}"style/tar"$style_id".png" ${project_dir}"style/"
	echo done

	echo Copying style image segmentation ${style_id} from DPST...
	cp ${data_dir}"style_seg/tar"$style_id".seg.png" ${project_dir}"style_seg/"
	echo done
fi

if [ "$data_source" = "CMP" ]
then
	echo CMP
	data_dir=$data_prefix"CMP/"

	echo Copying input image ${input_id} from CMP...
	cp ${data_dir}"input/in"$input_id".png" ${project_dir}"input/"
	echo done

	echo Copying input image segmentation ${input_id} from CMP...
	cp ${data_dir}"input_seg/in"$input_id".seg.png" ${project_dir}"input_seg/"
	echo done
fi
