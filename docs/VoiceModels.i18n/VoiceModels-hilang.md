__CODE_ब्लॉक_0__
सीडी मॉडल
wget -q --show-progress https://alphacephai.com/vosk/models/vosk-model-small-de-0.15.zip
अनज़िप -क्यू वोस्क-मॉडल-स्मॉल-डी-0.15.ज़िप
आरएम वोस्क-मॉडल-स्मॉल-डी-0.15.ज़िप
सीडी ..
__CODE_ब्लॉक_1__
इको "vosk-model-small-de-0.15" > config/model_name.txt
__CODE_ब्लॉक_2__
PRELOAD_MODELS = ["वोस्क-मॉडल .. "]
__CODE_ब्लॉक_3__
सुडो स्वैपऑफ -ए
सुडो फैलोकेट -एल 8जी/स्वैपफाइल
सुडो चामोद 600 /स्वैपफ़ाइल
sudo mkswap /swapfile
सुडो स्वैपॉन/स्वैपफ़ाइल
इको '/स्वैपफ़ाइल कोई नहीं स्वैप स्व 0 0' | सुडो टी -ए /etc/fstab
__CODE_ब्लॉक_4__
sysctl vm.swapusage
__कोड_ब्लॉक_5__