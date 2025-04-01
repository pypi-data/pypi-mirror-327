from argparse import ArgumentParser
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from factory_sdk.dto.adapter import AdapterArgs, TrainArgs
import os
import warnings
import transformers
from transformers.utils.logging import disable_progress_bar
import json
from factory_sdk.fast.eval.run import run_eval
from tempfile import TemporaryDirectory
from factory_sdk.dto.evaluation import EvalArgs
from factory_sdk.utils.model import load_model_for_training

warnings.filterwarnings("ignore")

transformers.logging.set_verbosity_error()
disable_progress_bar()


arg_parser = ArgumentParser()
arg_parser.add_argument('--dataset_path', type=str, default='data', help='Directory containing the data')
arg_parser.add_argument('--model_paths', type=str, default='model', help='Dictionary containing the model paths')
arg_parser.add_argument('--adapter_paths', type=str, default='adapter', help='Dictionary containing the adapter paths')
arg_parser.add_argument('--recipe_path', type=str, default='recipe', help='Directory containing the recipe')
arg_parser.add_argument('--client_params', type=str, default='{}', help='Client parameters')
arg_parser.add_argument('--eval_name', type=str, default='eval', help='Evaluation name')
arg_parser.add_argument('--local_rank', type=int, default=0, help='Local rank of the process')
arg_parser.add_argument('--eval_args', type=str, default='{}', help='Evaluation arguments')

args=arg_parser.parse_args()

model_paths = json.loads(args.model_paths)
adapter_paths = json.loads(args.adapter_paths)
eval_args = EvalArgs.model_validate_json(args.eval_args)

def get_model(id,revision):
    for model in model_paths:
        if model['id']==id and model['revision']==revision:
            return model


for adapter in adapter_paths:
    model=get_model(adapter['model']['id'],adapter['model']['revision'])
    
    with TemporaryDirectory() as tmp_dir:
        run_eval(tmp_dir,eval_args,args.dataset_path,model,adapter,args.recipe_path,json.loads(args.client_params),args.eval_name)