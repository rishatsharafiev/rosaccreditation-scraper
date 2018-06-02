# rosaccreditation-scraper

### Linux distribution
Ubuntu 17/18

### Install basic requirements
```
sudo apt-get install git nano \
  build-essential libssl-dev libffi-dev uuid-dev libcap-dev libpcre3-dev \
  python3-pip python3.6 python3.6-dev -y
```

### Install tesseract
```
sudo add-apt-repository ppa:alex-p/tesseract-ocr
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-rus
```

### Install pipenv
```
sudo pip3 install pipenv
```

### Initialize virtualenv
```
pipenv shell --python 3.6
```

### Install python requirements
```
pipenv install
```
