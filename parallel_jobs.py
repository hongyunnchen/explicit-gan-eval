import os, datetime
from numpy import floor
from subprocess import call

hidden_dims = [
                '32',
                '64',
                '128',
                '256',
                '512',
                ]

batch_sizes = [
              '128',
              '256',
              '512',
              '1024',
              ]

learning_rates = [
                  '2e-1',
                  '2e-2',
                  '2e-3',
                  ]

data_type = 'multivariate'
trials = '1'
dimensions = '32'
epochs = '25'
samples = '100000'

device = 0
jobs_per_gpu = 8

start_time = datetime.datetime.now().strftime("%Y-%m-%d-%s")

for hdim in hidden_dims:
    for bsize in batch_sizes:
        for lr in learning_rates:
            # Only allow certain number of jobs per GPU
            device += (1/jobs_per_gpu)

            # TMUX session name
            tmux_name = 'GPU.{7}-{0}-{1}-samples-{2}-dims-{3}-{4}-{5}-{6}'.format(data_type, samples, dimensions,
                                                                          trials, lr, bsize, hdim, int(floor(device)))
            # Launch TMUX session
            call(['echo', 'tmux', 'new', '-d', '-s', tmux_name])

            # Sent the job to that session
            call(['echo', 'tmux', 'send', '-t', tmux_name+'.0',
                  "CUDA_VISIBLE_DEVICES={0}".format(int(floor(device))),
                  "python3 ", "mini_main.py ",
                  data_type, ' ', trials, ' ', dimensions, ' ', hdim,
                  ' ', epochs, ' ', samples, ' ', bsize, ' ', lr, ' ', start_time,
                  'ENTER'])

            # Send another command to kill the tmux session once it's done running
            # (easier to track progress using 'tmux ls')
            call(['echo', 'tmux', 'send', '-t', tmux_name+'.0',
                  'kill-session ', '-t ', tmux_name, 'ENTER'])