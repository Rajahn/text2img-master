import pickle

import click

from config import DEVICE
from data import  Flowers
from damsm import DAMSM
from evaluation import IS_FID_Evaluator
from gan import AttnGAN


@click.group()
def main():
    pass


@main.command()
@click.argument('epochs', type=int)
@click.argument('name')
@click.argument('damsm')
@click.option('--gan', default=None)
@click.option('--device', default=DEVICE)
def train_gan(epochs, name, gan, damsm, device):
    dataset = Flowers()
    # with open('./datafile.pickle', 'wb') as p:
    #     dataset =pickle.load(p.read)

    with open('./datafile.pickle', 'wb') as p:
        str=pickle.dumps(dataset)
        p.write(str)
        p.close()

    damsm_model = DAMSM.load(damsm, device=device)
    if gan is None:
        print('train new gan')
        gan = AttnGAN(damsm_model, device)

    else:
        print('load gan')
        gan = AttnGAN.load(gan, damsm_model, device=device)

    metrics = gan.train(dataset, epochs, evaluator=IS_FID_Evaluator)
    gan.save(name, metrics=metrics)
    return gan, metrics


@main.command()
@click.argument('gan')
@click.argument('damsm')
@click.argument('save_dir')
@click.option('--device', default=DEVICE)
def validate_gan(gan, damsm, save_dir, device):
    dataset = Flowers()
    damsm_model = DAMSM.load(damsm, device=device)
    gan_model = AttnGAN.load(gan, damsm_model, device=device)
    gan_model.validate_test_set(dataset, save_dir=save_dir)


@main.command()
@click.argument('epochs', type=int)
@click.argument('name')
@click.option('--patience', type=int, default=20)
@click.option('--device', default=DEVICE)
def train_damsm(epochs, name, patience, device):
    dataset = Flowers()
    damsm = DAMSM(len(dataset.train.vocab), device=device)
    metrics = damsm.train(dataset, epochs, patience=patience)
    damsm.save(name, metrics=metrics)
    return damsm, metrics


if __name__ == '__main__':
    main()
