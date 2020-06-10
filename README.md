# text2img-master
only used to learn attngan .
cloned from [text2img](https://github.com/bcserna/text2img)

we changed dataset to Oxford102 flowers dataset

----
the result only training 1 epoch , looks like a flower
![image](https://github.com/Rajahn/text2img-master/blob/master/text2img-master/607.jpg)

-----

This is an implementation of the [AttnGAN](https://arxiv.org/abs/1711.10485) in PyTorch, with some experimental additions and changes.

### Dataset

- The model is currently trained on the Oxford102 flowers dataset
Download the images from [here](http://www.robots.ox.ac.uk/~vgg/data/flowers/102/) and save them to /src/Flowers102/image
Also download the captions from [this link](https://drive.google.com/file/d/0B0ywwgffWnLLcms2WWJQRFNSWXM/view).
Extract the archive, copy the file to /Flowers102

### Experimenting

* To train a DAMSM model, use the `python -m src.main train-damsm <EPOCHS> <NAME> [OPTIONS]` command. `EPOCHS` sets the number of training epochs, `NAME` is the name the model is going to be saved with and further referenced by. Options include:
  * Set patience for early stopping: `--patience=20`
  * Set device: `--device=cuda:0`

* To train the GAN, use `python -m src.main train-gan <EPOCHS> <NAME> <DAMSM> [OPTIONS]`. `EPOCHS` and `NAME` are the number of training epochs and the name of the model respectively. `DAMSM` is the name of the DAMSM model to be used for text-encoding and auxiliary DAMSM-loss. Options include:
  * Continue training of a saved model: `--gan=ExampleModelName`
  * Set device: `--device=cuda:1`

* To generate an image for each sample in the test set, use `python -m src.main validate-gan GAN DAMSM SAVEDIR [OPTIONS]`. `GAN` and `DAMSM` are the names of the models to be used. `SAVEDIR` is the output directory. Options include:
  * Set device: `--device=cuda:2`

For different hyperparameters, change values in `config.py`.
