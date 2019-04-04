import hparams
from model.wavenet_model import *
from model.timbre_training import *

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = WaveNetModel(hparams.create_harmonic_hparams(), device).to(device)
print('model: ', model)
print('receptive field: ', model.receptive_field)
print('parameter count: ', model.parameter_count())
trainer = ModelTrainer(model=model,
                       data_folder='data/timbre_model',
                       lr=0.0001,
                       weight_decay=0.0,
                       snapshot_path='./snapshots/harmonic',
                       snapshot_name='harm',
                       snapshot_interval=2000,
                       device=device,
                       temperature=0.05)


def exit_handler():
    trainer.save_model()
    print("exit from keyboard")


#atexit.register(exit_handler)

#epoch = trainer.load_checkpoint('/home/sean/pythonProj/torch_npss/snapshots/harmonic/best_harmonic_model_1649_2019-03-31_17-43-00')

print('start training...')
trainer.train(batch_size=1024,
              epochs=3000)
