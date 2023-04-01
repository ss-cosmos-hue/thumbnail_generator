from paddleclas import PaddleClas

clas = PaddleClas(model_name='PP-ShiTuV2')
infer_imgs='images/fairy.png'
result=clas.predict(infer_imgs)
print(next(result))