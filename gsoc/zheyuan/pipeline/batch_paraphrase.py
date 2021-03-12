import argparse
import os

import tensorflow as tf

tf.compat.v1.enable_eager_execution()
from paraphrase_questions import paraphrase_questions, prepare_model,set_seed,pick_final_sentence, pick_final_sentence_advanced
from constant import Constant
from bert_classifier import load_model

const = Constant()
seperator = "\t"

const.URL = "https://datascience-models-ramsri.s3.amazonaws.com/t5_paraphraser.zip"

def batch_paraphrase(templates_path, model_dir):
    # folder_path = get_pretrained_model(const.URL)

    set_seed(42)
    t5_tokenizer, device, t5_model = prepare_model()
    bert_model, bert_tokenizer = load_model(model_dir, device)
    dir = os.path.realpath(templates_path)
    with open(dir, "r") as lines:
        with open(dir + "_paraphrased", "w") as w:
            for line in lines:
                prop = line.strip("\n").split(seperator)
                question = prop[3]
                paraphrased_candidates = paraphrase_questions(t5_tokenizer, device, t5_model, question)
                paraphrased = pick_final_sentence(question, paraphrased_candidates)
                if model_dir:
                    advanced = pick_final_sentence_advanced(device, bert_model, bert_tokenizer, question, paraphrased_candidates)
                w.write(line)
                print("Original", line)
                # for i, candidate in enumerate(paraphrased_candidates):
                #     new_prop = prop[:-1]
                #     new_prop[3] = candidate
                #     new_prop.append("Paraphrased {}\n".format(i))
                #     print(new_prop)
                #     new_line = seperator.join(new_prop)
                #
                #     w.write(new_line)
                if paraphrased:
                    new_prop = prop[:-1]
                    new_prop[3] = paraphrased
                    new_prop.append("Paraphrased \n")
                    new_line = seperator.join(new_prop)
                    w.write(new_line)

                print("Paraphrase", new_line)
                if model_dir and advanced:
                    new_prop = prop[:-1]

                    new_prop[3] = advanced
                    new_prop.append("Paraphrased advanced\n")
                    new_line = seperator.join(new_prop)
                    w.write(new_line)
                    w.flush()
                    print("Advanced", new_line)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--templates', dest='templates', metavar='templates file',
                               help='templates file', required=True)
    requiredNamed.add_argument('--model', dest='model', metavar='model_dir',
                               help='path of directory of the fine-tuned model', required=True)


    args = parser.parse_args()
    templates_path = args.templates
    model_dir = args.model
    batch_paraphrase(templates_path, model_dir)
