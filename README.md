# thumbnail_generator
## Hackprinceton2023 spring

https://devpost.com/software/fabulous-5

## Use cases
<p>
    <img src="images/boy_gun.png" width="30%", height="30%">
    <img src="output/boy_gun.png" width="30%", height="30%">
</p>
<p>
    <img src="images/toad.png" width="30%", height="30%">
    <img src="output/toad.png" width="30%", height="30%">
</p>
<p>
    <img src="images/dora.png" width="30%", height="30%">
    <img src="output/dora.png" width="30%", height="30%">
</p>
<p>
    <img src="images/macaron.png" width="30%", height="30%">
    <img src="output/macaron.png" width="30%", height="30%">
</p>

## Getting started
1. `python3 -r requirements.txt`  
2. `pip3 install scikit-learn`  
3. `git clone https://github.com/xinntao/Real-ESRGAN.git`  
4. Comment out line 6 in `Real-ESRGAN/realesrgan/__init__.py`  
5. `rm -rf Real-ESRGAN/inputs/*`  

## Using the app
Create two terminals to run frontend and backend
1. `cd frontend; npm i; npx http-server`
    - Go to Features page
2. `python3 app.py`
