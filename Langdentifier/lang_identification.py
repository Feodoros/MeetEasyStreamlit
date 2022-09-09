SAMPLING_RATE = 16000

import torch
import subprocess

torch.set_num_threads(1)

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_lang_detector',
                              force_reload=False,
                              onnx=False)

get_language, read_audio = utils
