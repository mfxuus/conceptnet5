import os
import argparse

from pykeen.pipeline import pipeline
from pykeen.models import predict
import torch
from pykeen.datasets import get_dataset

from config import (
    KGC_CSV,
    KGC_EDGES_CSV,
    EMPTY_CSV
)


def link_prediction(dataset, model, dir, evaluation_only=True, epochs=0):
    """
    Check detailed instruction on https://pykeen.readthedocs.io/en/latest/tutorial/making_predictions.html
    """

    if not evaluation_only and epochs > 0:
        # Run the pipeline
        result = pipeline(dataset=dataset,
                          training=KGC_CSV if not dataset else None,
                          testing=EMPTY_CSV if not dataset else None,
                          validation=EMPTY_CSV if not dataset else None,
                          model=model,
                          epochs=epochs)
        # save the model
        result.save_to_directory(os.path.join(dir, f'kgc_{model}'))
        model = result.model
        training = result.training
    else:
        model = torch.load(os.path.join(dir, f'kgc_{model}', 'trained_model.pkl'))
        training = get_dataset(dataset=dataset,
                               training=KGC_CSV if not dataset else None,
                               testing=EMPTY_CSV if not dataset else None,
                               validation=EMPTY_CSV if not dataset else None,
                               ).training

    # Score top K triples
    top_k_predictions_df = predict.get_all_prediction_df(model,
                                                         k=25000,  # manually get top k predictions
                                                         triples_factory=training,
                                                         remove_known=True,  # only get novel predictions
                                                         )
    print(top_k_predictions_df)
    top_k_predictions_df.to_csv(KGC_EDGES_CSV, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    '''
    python 4_knowledge_graph_completion_demo.py
    python 4_knowledge_graph_completion_demo.py --train
    '''
    parser.add_argument(
        '--eval',
        action='store_true',
        default=False,
        help='Evaluation only',
    )
    parser.add_argument(
        '--dataset',
        # default='ConceptNet',
        help='Used dataset',
    )
    parser.add_argument(
        '--model',
        # default='TransE',
        default='ConvE',
        help='Link prediction model',
    )
    parser.add_argument(
        '--dir',
        default='model',
        help='Model folder',
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=20,
        help='Set training epochs',
    )

    args = parser.parse_args()

    link_prediction(args.dataset, args.model, args.dir, args.eval, args.epochs)


