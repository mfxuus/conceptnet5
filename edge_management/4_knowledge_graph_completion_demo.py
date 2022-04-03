import os
import argparse

from pykeen.pipeline import pipeline
from pykeen.models import predict
import torch
from pykeen.datasets import get_dataset


def link_prediction(dataset, model, dir, is_training=False):
    """
    Check detailed instruction on https://pykeen.readthedocs.io/en/latest/tutorial/making_predictions.html
    """

    # TODO: could be buggy
    model, training = None, None
    if is_training:
        # Run the pipeline
        # result = pipeline(dataset='ConceptNet', model='TransE')
        result = pipeline(dataset=dataset, model=model)
        # save the model
        result.save_to_directory(os.path.join(dir, f'{dataset}_{model}'))
        model = result.model
        training = result.training
    else:
        model = torch.load(os.path.join(dir, f'{dataset}_{model}', 'trained_model.pkl'))
        training = get_dataset(dataset=dataset).training

    # Predict tails
    predicted_tails_df = predict.get_tail_prediction_df(
        model, 'brazil', 'intergovorgs', triples_factory=training,
    )
    # Predict relations
    predicted_relations_df = predict.get_relation_prediction_df(
        model, 'brazil', 'uk', triples_factory=training,
    )
    # Predict heads
    predicted_heads_df = predict.get_head_prediction_df(model, 'conferences', 'brazil', triples_factory=training)
    # Score all triples (memory intensive)
    predictions_df = predict.get_all_prediction_df(model, triples_factory=training)
    # Score top K triples
    top_k_predictions_df = predict.get_all_prediction_df(model, k=150, triples_factory=training)
    # Score a given list of triples
    score_df = predict.predict_triples_df(
        model=model,
        triples=[('brazil', 'conferences', 'uk'), ('brazil', 'intergovorgs', 'uk')],
        triples_factory=training,
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    '''
    python 4_knowledge_graph_completion_demo.py
    python 4_knowledge_graph_completion_demo.py --train
    '''
    parser.add_argument(
        '--train',
        action='store_true',
        default=False,
        help='Train a model',
    )
    parser.add_argument(
        '--dataset',
        default='ConceptNet',
        help='Used dataset',
    )
    parser.add_argument(
        '--model',
        default='ConvE',
        help='Link prediction model',
    )
    parser.add_argument(
        '--dir',
        default='model',
        help='Model folder',
    )

    args = parser.parse_args()

    link_prediction(args.dataset, args.model, args.dir, args.train)


