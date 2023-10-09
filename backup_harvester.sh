#!/bin/bash

cd ..

NOW_DATE=$(date +%Y%m%d%H)
FILE_NAME=${NOW_DATE}_harvesters.dat

# harvestフォルダが存在しない場合、作成
if [ ! -d "./harvest" ]; then
  mkdir ./harvest
fi

cp target/nodes/node/data/harvesters.dat ./harvest/${FILE_NAME}

#google driveへバックアップ
cd ./symbol-node-backup
python3 g_drive_upload.py "${FILE_NAME}"