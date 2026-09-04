__代码_块_0__
CD型号
wget -q --show-progress https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
解压 -q vosk-model-small-de-0.15.zip
rm vosk-model-small-de-0.15.zip
光盘 ..
__代码_块_1__
echo "vosk-model-small-de-0.15" > config/model_name.txt
__代码_块_2__
PRELOAD_MODELS = ["vosk-模型 .."]
__代码_块_3__
sudo swapoff -a
sudo fallocate -l 8G /交换文件
须藤 chmod 600 /交换文件
须藤 mkswap /交换文件
须藤交换/交换文件
echo '/swapfile 无 交换 sw 0 0' | sudo tee -a /etc/fstab
__代码_块_4__
sysctl 虚拟机交换
__代码_块_5__